import json

from rest_framework.renderers import JSONRenderer


class ApiJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'response'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        errors = None
        try:
            errors = data.get('error', None)
        except AttributeError:
            pass
        if errors is not None:
            print(errors)
            return super(ApiJSONRenderer, self).render(data)

        if not data:
            return ""

        return json.dumps({
            self.object_label: data
        })
