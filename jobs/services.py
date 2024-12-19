# jobs/services.py
import requests
from .models import ExternalInternship

class ExternalJobService:
    @staticmethod
    def fetch_external_jobs():
        # Интеграция с API партнеров
        # Пример с LinkedIn API
        response = requests.get('partner_api_url')
        jobs = response.json()
        
        for job in jobs:
            ExternalInternship.objects.create(
                title=job['title'],
                company=job['company'],
                description=job['description'],
                location=job['location'],
                url=job['url'],
                deadline=job['deadline']
            )