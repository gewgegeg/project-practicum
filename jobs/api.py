from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Job, Application, Review
from .serializers import JobSerializer, ApplicationSerializer, ReviewSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        job = self.get_object()
        Application.objects.create(
            job=job,
            applicant=request.user,
            status='PENDING'
        )
        return Response({'status': 'application submitted'})


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Application.objects.all()
        return Application.objects.filter(applicant=self.request.user)
