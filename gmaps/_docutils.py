
def doc_subst(snippets):
    """ Substitute format strings in class or function docstring """
    def decorator(cls_or_func):
        # Strip the snippets to avoid trailing new lines and whitespace
        stripped_snippets = {
            key: snippet.strip() for (key, snippet) in snippets.items()
        }
        cls_or_func.__doc__ = cls_or_func.__doc__.format(**stripped_snippets)
        return cls_or_func
    return decorator
