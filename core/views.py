from django.views.generic import TemplateView
from jobs.recommendations import JobRecommender
from jobs.models import Job

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['recommended_jobs'] = JobRecommender.get_recommendations(
                self.request.user
            )
        return context
