from api_v1.renderers import ApiJSONRenderer


class UserJSONRenderer(ApiJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        return super(UserJSONRenderer, self).render(data)


class RegistrationJSONRenderer(ApiJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # print(data)
        token = data.get('token', None)
        # print(token)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        return super(RegistrationJSONRenderer, self).render(data)