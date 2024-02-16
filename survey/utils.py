class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        translate = {
            'redirect_to': self.request.path
        }
        return context | translate
