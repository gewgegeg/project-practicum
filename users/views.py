from django.views.generic import DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect  # Добавляем импорт redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from jobs.models import Application

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    
    def get_object(self):
        return self.request.user

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user == self.object:
            # Получаем все заявки пользователя
            context['applications'] = Application.objects.filter(
                applicant=self.request.user
            ).select_related('job').order_by('-created_at')
            
            # Добавляем статистику по заявкам
            context['applications_stats'] = {
                'total': context['applications'].count(),
                'pending': context['applications'].filter(status='PENDING').count(),
                'reviewing': context['applications'].filter(status='REVIEWING').count(),
                'accepted': context['applications'].filter(status='ACCEPTED').count(),
                'rejected': context['applications'].filter(status='REJECTED').count(),
            }
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile_edit.html'
    fields = ['first_name', 'last_name', 'email']

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return reverse_lazy('users:profile-detail', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Ваш профиль был успешно обновлен!')
        return response

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 
            'Регистрация успешно завершена! Теперь вы можете войти в систему.'
        )
        return response

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    if self.request.user == self.object:
        applications = Application.objects.filter(
            applicant=self.request.user
        ).select_related('job').order_by('-created_at')
        
        context['applications'] = applications
        context['applications_stats'] = {
            'total': applications.count(),
            'pending': applications.filter(status='PENDING').count(),
            'reviewing': applications.filter(status='REVIEWING').count(),
            'accepted': applications.filter(status='ACCEPTED').count(),
            'rejected': applications.filter(status='REJECTED').count(),
        }
    return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'Вы уже зарегистрированы и вошли в систему.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)