""" Controller Mixins """
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class DataMixin: # pylint: disable=too-few-public-methods
    def get_user_context(self, **kwargs):
        context = kwargs
        translate = {
            'redirect_to': self.request.path
        }
        return context | translate
