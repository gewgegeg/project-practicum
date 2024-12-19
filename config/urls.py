from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import HomeView
from users import views as user_views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('jobs/', include('jobs.urls')),
    path('notifications/', include('notifications.urls')),
    path('users/', include('users.urls')),
    
    # Auth URLs
    path('login/', 
         auth_views.LoginView.as_view(template_name='registration/login.html'), 
         name='login'),
    
    # Обновленный путь для logout
    path('logout/', 
         auth_views.LogoutView.as_view(), 
         name='logout'),
    
    path('register/', 
         user_views.RegisterView.as_view(), 
         name='register'),
]