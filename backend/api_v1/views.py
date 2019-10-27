from django.views.generic import TemplateView


class SwaggerView(TemplateView):
    template_name = 'api_v1/swagger-ui.html'

