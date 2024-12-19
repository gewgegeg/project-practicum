from .models import Job
from django.db.models import Q

class JobRecommender:
    @staticmethod
    def get_recommendations(user):
        if not user.is_authenticated:
            return Job.objects.none()

        # Получаем типы работ, на которые пользователь уже подавал заявки
        applied_job_types = Job.objects.filter(
            applications__applicant=user  # Используем related_name 'applications'
        ).values_list('job_type', flat=True).distinct()

        # Получаем активные вакансии того же типа
        recommended_jobs = Job.objects.filter(
            is_active=True,
            job_type__in=applied_job_types
        ).exclude(
            applications__applicant=user  # Исключаем вакансии, на которые уже подана заявка
        )

        # Если нет рекомендаций на основе предыдущих заявок, 
        # возвращаем несколько последних активных вакансий
        if not recommended_jobs.exists():
            recommended_jobs = Job.objects.filter(
                is_active=True
            ).exclude(
                applications__applicant=user
            )[:5]

        return recommended_jobs