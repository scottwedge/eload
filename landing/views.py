from django.views.generic.base import TemplateView


class IndexTemplateView(TemplateView):

    def get_template_names(self):
        return 'index-dev.html'
