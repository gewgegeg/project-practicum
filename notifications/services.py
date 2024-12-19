from django.contrib.contenttypes.models import ContentType
from .models import Notification

class NotificationService:
    @staticmethod
    def create_notification(recipient, notification_type, title, message, related_object=None):
        notification = Notification(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message
        )
        
        if related_object:
            notification.content_type = ContentType.objects.get_for_model(related_object)
            notification.object_id = related_object.id
            
        notification.save()
        return notification

    @staticmethod
    def mark_as_read(notification_id, user):
        notification = Notification.objects.get(id=notification_id, recipient=user)
        notification.is_read = True
        notification.save()