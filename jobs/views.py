from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Job, Application, Review
from notifications.services import NotificationService

class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True)
        job_type = self.request.GET.get('job_type')
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['applications'] = Application.objects.filter(
                applicant=self.request.user
            ).select_related('job').order_by('-created_at')
        return context

class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['has_applied'] = Application.objects.filter(
                job=self.object,
                applicant=self.request.user
            ).exists()
            if self.request.user.is_staff:
                context['applications'] = Application.objects.filter(
                    job=self.object
                ).select_related('applicant').order_by('-created_at')
        return context

class JobApplicationView(LoginRequiredMixin, CreateView):
    model = Application
    template_name = 'jobs/application_form.html'
    fields = ['cover_letter']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = get_object_or_404(Job, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        job = get_object_or_404(Job, pk=self.kwargs['pk'])
        form.instance.applicant = self.request.user
        form.instance.job = job
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Ваша заявка успешно отправлена!')
            
            # Уведомление для соискателя
            NotificationService.create_notification(
                recipient=self.request.user,
                notification_type='application_status',
                title='Заявка отправлена',
                message=f'Ваша заявка на вакансию {job.title} успешно отправлена.',
                related_object=self.object
            )
            
            # Уведомление для администраторов
            for admin in User.objects.filter(is_staff=True):
                NotificationService.create_notification(
                    recipient=admin,
                    notification_type='new_application',
                    title='Новая заявка',
                    message=f'Получена новая заявка на вакансию {job.title} от {self.request.user.username}',
                    related_object=self.object
                )
            
            return response
        except IntegrityError:
            messages.error(self.request, 'Вы уже подавали заявку на эту вакансию')
            return redirect('jobs:job-detail', pk=job.pk)

    def get_success_url(self):
        return reverse_lazy('jobs:job-detail', kwargs={'pk': self.kwargs['pk']})

class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('jobs:job-list')
    template_name = 'jobs/job_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Вакансия успешно удалена')
        return super().delete(request, *args, **kwargs)

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'jobs/review_form.html'
    fields = ['rating', 'comment']

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.reviewed = get_object_or_404(User, pk=self.kwargs['user_id'])
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Отзыв успешно добавлен!')
            return response
        except IntegrityError:
            messages.error(self.request, 'Вы уже оставляли отзыв этому пользователю')
            return redirect('users:profile', pk=self.kwargs['user_id'])

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.kwargs['user_id']})

class ApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    template_name = 'jobs/application_update.html'
    fields = ['status']

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        response = super().form_valid(form)
        application = self.object
        
        # Уведомление для соискателя об изменении статуса
        NotificationService.create_notification(
            recipient=application.applicant,
            notification_type='application_status',
            title='Статус заявки изменен',
            message=f'Статус вашей заявки на вакансию {application.job.title} изменен на {application.get_status_display()}',
            related_object=application
        )
        
        messages.success(self.request, 'Статус заявки успешно обновлен')
        return response

    def get_success_url(self):
        return reverse_lazy('jobs:job-detail', kwargs={'pk': self.object.job.pk})

class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'jobs/application_list.html'
    context_object_name = 'applications'
    paginate_by = 10

    def get_queryset(self):
        return Application.objects.filter(
            applicant=self.request.user
        ).select_related('job').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applications = self.get_queryset()
        context['applications_stats'] = {
            'total': applications.count(),
            'pending': applications.filter(status='PENDING').count(),
            'reviewing': applications.filter(status='REVIEWING').count(),
            'accepted': applications.filter(status='ACCEPTED').count(),
            'rejected': applications.filter(status='REJECTED').count(),
        }
        return context