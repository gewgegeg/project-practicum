from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from .models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 10

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class MarkNotificationReadView(LoginRequiredMixin, UpdateView):
    model = Notification
    fields = ['is_read']
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.recipient == request.user:
            notification.mark_as_read()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=403)

class NotificationCountView(LoginRequiredMixin, View):
    def get(self, request):
        count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        return JsonResponse({'count': count})