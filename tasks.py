
import os
import tempfile
import itertools
import shutil
import re

from invoke import task, run

from subprocess import call

import semver

VERSION_TEMPLATE = '''
# This file is generated programatically.

# Version of the Python package
__version__ = '{version_string}'

# Version of the JS client. This must match the version field in package.json.
CLIENT_VERSION = '{version_string}'
'''

RELEASE_NOTES_TEMPLATE = '''# Write the release notes here
# Delete the version title to cancel
Version {version_string}
{underline}
'''

GMAPS_DIR = os.path.dirname(os.path.realpath(__file__))


@task(help={'version': 'Version number to release'})
def prerelease(ctx, version):
    '''
    Release a pre-release version

    Running this task will:
     - Bump the version number
     - Push a release to pypi and npm
    '''
    set_pyversion(version)
    set_jsversion(version)
    run('python setup.py sdist upload')
    os.chdir(os.path.join(GMAPS_DIR, 'js'))
    try:
        run('npm publish')
    finally:
        os.chdir(GMAPS_DIR)


@task(help={'version': 'Version number to release'})
def release(ctx, version):
    '''
    Release a new version

    Running this task will:
     - Prompt the user for a changelog and write it to
       the release notes
     - Commit the release notes
     - Bump the version number
     - Push a release to pypi and npm
    '''
    release_notes_lines = get_release_notes(version)

    if release_notes_lines is None:
        print('No release notes: exiting')
        exit()

    update_release_notes(version, release_notes_lines)
    with open('changelog.tmp', 'w') as f:
        f.writelines(release_notes_lines)

    run('git add docs/source/release_notes.rst')
    run('git commit -m "Add release notes for version {}"'.format(version))
    set_pyversion(version)
    set_jsversion(version)
    run('python setup.py sdist bdist upload')
    os.chdir(os.path.join(GMAPS_DIR, 'js'))
    try:
        run('npm publish')
    finally:
        os.chdir(GMAPS_DIR)


@task(help={
    'version': 'Version number to finalize. Must be '
               'the same version number that was used in the release.'
})
def postrelease(ctx, version):
    '''
    Finalise the release

    Running this task will:
     - commit the version changes to source control
     - tag the commit
     - push changes to master
    '''
    run('git add gmaps/_version.py')
    run('git add js/package.json')
    run('git commit -m "Bump version to {}"'.format(version))
    run('git tag -a v{} -F changelog.tmp'.format(version))
    run('git push origin master --tags')
    new_version = semver.bump_patch(version) + '-dev'
    set_pyversion(new_version)
    set_jsversion(new_version)
    run('git add gmaps/_version.py')
    run('git add js/package.json')
    run('git commit -m "Back to dev"')
    run('git push origin master')


@task(help={
    'version': 'Version number to finalize. Must be '
               'the same version number that was used in the release.'
})
def release_conda(ctx, version):
    """
    Open a PR for the new release in conda-forge.
    """
    sha256 = get_file_sha256('dist/gmaps-{}.tar.gz'.format(version))
    print('Release SHA256 hash: {}'.format(sha256))
    tempdir = tempfile.mkdtemp()
    try:
        print('Cloning gmaps-feedstock to {}'.format(tempdir))
        os.chdir(tempdir)
        run('git clone git@github.com:pbugnion/gmaps-feedstock.git')
        os.chdir('gmaps-feedstock')
        run('git remote add upstream git@github.com:conda-forge/gmaps-feedstock.git')
        run('git pull --rebase upstream master')
        branch_name = 'release-version-{}'.format(version)
        run('git checkout -b {}'.format(branch_name))
        update_conda_recipe(version, sha256)
        run('git add recipe/meta.yaml')
        run('git commit -m "Release version {}"'.format(version))
        run('git push origin {}'.format(branch_name))
        print('URL: https://github.com/conda-forge/gmaps-feedstock')
    finally:
        print('Deleting temporary directory {}'.format(tempdir))
        shutil.rmtree(tempdir)


def update_release_notes(version, new_lines):
    release_notes_path = os.path.join(
        GMAPS_DIR, 'docs', 'source', 'release_notes.rst')
    with open(release_notes_path) as f:
        current_release_notes_lines = f.readlines()
    current_release_notes_lines = itertools.dropwhile(
        lambda line: 'Version' not in line,
        current_release_notes_lines
    )
    new_release_notes_lines = [
        '\n',
        'Release notes\n',
        '-------------\n',
        '\n'
    ] + new_lines + list(current_release_notes_lines)
    with open(release_notes_path, 'w') as f:
        f.writelines(new_release_notes_lines)


def get_release_notes(version):
    version_info = semver.parse_version_info(version)
    version_string = semver.format_version(*version_info)
    underline = '=' * len('Version {}'.format(version_string))
    initial_message = RELEASE_NOTES_TEMPLATE.format(
        version_string=version_string, underline=underline)
    lines = open_editor(initial_message)
    non_commented_lines = [line for line in lines if not line.startswith('#')]
    changelog = ''.join(non_commented_lines)
    if version_string in changelog:
        if not non_commented_lines[-1].isspace():
            non_commented_lines.append('\n')
        return non_commented_lines
    else:
        return None


def set_pyversion(version):
    version_info = semver.parse_version_info(version)
    version_string = semver.format_version(*version_info)
    with open(os.path.join(GMAPS_DIR, 'gmaps', '_version.py'), 'w') as f:
        f.write(VERSION_TEMPLATE.format(version_string=version_string))


def set_jsversion(version):
    version_info = semver.parse_version_info(version)
    version_string = semver.format_version(*version_info)
    package_json_path = os.path.join(GMAPS_DIR, 'js', 'package.json')
    with open(package_json_path) as f:
        package_json = f.readlines()
    for iline, line in enumerate(package_json):
        if '"version"' in line:
            package_json[iline] = '  "version": "{}",\n'.format(version_string)
    with open(package_json_path, 'w') as f:
        f.writelines(package_json)


def update_conda_recipe(version, sha256):
    with open('recipe/meta.yaml') as f:
        lines = [line.rstrip() for line in f]
    updated_lines = replace_line(
        lines,
        'set version = ',
        '{{% set version = "{}" %}}'.format(version)
    )
    updated_lines = replace_line(
        updated_lines,
        'set sha256 = ',
        '{{% set sha256 = "{}" %}}'.format(sha256)
    )
    with open('recipe/meta.yaml', 'w') as f:
        f.writelines([line + '\n' for line in updated_lines])


def get_file_sha256(path):
    sha256_output = run(
        'shasum -a 256 {}'.format(path),
        hide=True
    )
    if not sha256_output.ok:
        print('Error getting sha256.')
        print(sha256_output.stdout)
        exit()
    else:
        sha256 = sha256_output.stdout.split(' ', 1)[0]
        return sha256


def open_editor(initial_message):
    editor = os.environ.get('EDITOR', 'vim')
    tmp = tempfile.NamedTemporaryFile(suffix='.tmp')
    fname = tmp.name

    with open(fname, 'wb') as f:
        f.write(initial_message)
        f.flush()

    call([editor, fname], close_fds=True)

    with open(fname, 'rb') as f:
        lines = f.readlines()

    return lines


def replace_line(lines, regexp, new_line):
    """
    Replace a line that matches 'regexp'
    """
    for (iline, line) in enumerate(lines):
        match_result = re.search(regexp, line)
        if match_result is not None:
            break
    updated_lines = lines[:]
    updated_lines[iline] = new_line
    return updated_lines
