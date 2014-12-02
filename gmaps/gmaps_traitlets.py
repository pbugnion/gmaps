
import IPython.utils.traitlets as traitlets

import utils

class CSSDimension(traitlets.TraitType):

    default_value = u'0'
    info_text = u'A CSS dimension'

    def validate(self, obj, value):
        value = utils.parse_css_dimension(value)
        return value
