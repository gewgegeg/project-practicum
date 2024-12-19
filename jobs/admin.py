from django.contrib import admin
from .models import Job, Application, Review  # Убрали ExternalInternship

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'created_at', 'is_active')
    list_filter = ('job_type', 'is_active', 'created_at')
    search_fields = ('title', 'company', 'description')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'company', 'location')
        }),
        ('Описание вакансии', {
            'fields': ('description', 'job_type')
        }),
        ('Сроки', {
            'fields': ('deadline', 'is_active')
        }),
    )

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('job__title', 'applicant__username')
    date_hierarchy = 'created_at'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewed', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('reviewer__username', 'reviewed__username', 'comment')