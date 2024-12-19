from django.urls import path
from . import views, admin_views

app_name = 'jobs'

urlpatterns = [
    path('', views.JobListView.as_view(), name='job-list'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('<int:pk>/apply/', views.JobApplicationView.as_view(), name='apply'),
    path('<int:pk>/delete/', views.JobDeleteView.as_view(), name='job-delete'),
    path('review/<int:user_id>/', views.ReviewCreateView.as_view(), name='create-review'),
    path('application/<int:pk>/update/', views.ApplicationUpdateView.as_view(), name='application-update'),
    path('applications/', views.ApplicationListView.as_view(), name='application-list'),

    # Административные URL-паттерны
    path('admin/jobs/', 
         admin_views.AdminJobListView.as_view(), 
         name='admin-jobs'),
    
    path('admin/jobs/create/', 
         admin_views.AdminJobCreateView.as_view(),
         name='admin-job-create'),
    
    path('admin/jobs/<int:job_id>/applications/',
         admin_views.AdminApplicationListView.as_view(), 
         name='admin-job-applications'),
    
    path('admin/job/<int:job_id>/delete/',
         admin_views.AdminJobDeleteView.as_view(), 
         name='admin-job-delete'),
]