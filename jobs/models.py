from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Job(models.Model):
    JOB_TYPES = [
        ('INTERNSHIP', 'Стажировка'),
        ('PART_TIME', 'Частичная занятость'),
        ('FULL_TIME', 'Полная занятость'),
    ]

    title = models.CharField('Название вакансии', max_length=200)
    description = models.TextField('Описание')
    company = models.CharField('Компания', max_length=200)
    location = models.CharField('Местоположение', max_length=200)
    job_type = models.CharField('Тип работы', max_length=50, choices=JOB_TYPES)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    deadline = models.DateTimeField('Срок подачи заявок')
    is_active = models.BooleanField('Активная', default=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} в {self.company}"

    def get_absolute_url(self):
        return reverse('jobs:job-detail', kwargs={'pk': self.pk})

class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'На рассмотрении'),
        ('REVIEWING', 'Рассматривается'),
        ('ACCEPTED', 'Принята'),
        ('REJECTED', 'Отклонена'),
    ]

    job = models.ForeignKey(Job, verbose_name='Вакансия', on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, verbose_name='Соискатель', on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField('Сопроводительное письмо', default='', blank=True)
    status = models.CharField('Статус', max_length=50, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField('Дата подачи', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        unique_together = ('job', 'applicant')
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка от {self.applicant.username} на {self.job.title}"

class Review(models.Model):
    reviewer = models.ForeignKey(User, verbose_name='Автор отзыва', related_name='given_reviews', on_delete=models.CASCADE)
    reviewed = models.ForeignKey(User, verbose_name='Получатель отзыва', related_name='received_reviews', on_delete=models.CASCADE)
    rating = models.IntegerField('Оценка', choices=[(i, f'{i} звезд') for i in range(1, 6)])
    comment = models.TextField('Комментарий')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('reviewer', 'reviewed')
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.reviewer.username} для {self.reviewed.username}"