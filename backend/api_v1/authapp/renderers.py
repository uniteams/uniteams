from api_v1.renderers import ApiJSONRenderer


class UserJSONRenderer(ApiJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        token = data.get('access_token', None)

        if token is not None and isinstance(token, bytes):
            data['access_token'] = token.decode('utf-8')

        return super(UserJSONRenderer, self).render(data)
