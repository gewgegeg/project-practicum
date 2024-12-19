from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Job, Application
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


from django.views.generic import View
from django.http import JsonResponse


@method_decorator(staff_member_required, name='dispatch')
class AdminJobDeleteView(View):
    def post(self, request, job_id):
        try:
            job = get_object_or_404(Job, id=job_id)
            job.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@method_decorator(staff_member_required, name='dispatch')
class AdminJobListView(ListView):
    model = Job
    template_name = 'jobs/admin/job_list.html'
    context_object_name = 'jobs'


@method_decorator(staff_member_required, name='dispatch')
class AdminJobCreateView(CreateView):
    model = Job
    template_name = 'jobs/admin/job_form.html'
    fields = ['title', 'description', 'company',
              'location', 'job_type', 'deadline', 'is_active']
    success_url = reverse_lazy('admin-jobs')


@method_decorator(staff_member_required, name='dispatch')
class AdminApplicationListView(ListView):
    model = Application
    template_name = 'jobs/admin/application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        job_id = self.kwargs.get('job_id')
        return Application.objects.filter(job_id=job_id)
