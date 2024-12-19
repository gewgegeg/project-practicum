from rest_framework import serializers
from .models import Job, Application, Review
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'description',
            'company',
            'location',
            'job_type',
            'created_at',
            'deadline',
            'is_active'
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'job',
            'applicant',
            'status',
            'created_at'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    reviewed = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'reviewer',
            'reviewed',
            'rating',
            'comment',
            'created_at'
        ]
