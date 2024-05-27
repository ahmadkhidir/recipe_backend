from restful_channels.helpers import WSRequest, WSjson, WSResponse
from channels.db import database_sync_to_async
from datetime import datetime


class NotificationMixin:
    async def send_notification(self, request: WSRequest):
        timestamp = request.data.get('timestamp', None) if request.data else None
        notifications = await self.get_notifications(timestamp)
        response = WSResponse(
            data=notifications,
            action= request.action
        )
        await self.send(text_data=response.stringify())

    @database_sync_to_async
    def get_notifications(self, timestamp=None):
        from .models import GeneralNotification
        from .serializers import GeneralNotificationSerializer
        general_notification = GeneralNotification.objects.all()
        if timestamp:
            general_notification = general_notification.filter(created_at__gt=timestamp)
        general_notification = general_notification.order_by("-created_at").all()
        general_notification = GeneralNotificationSerializer(general_notification, many=True)
        return WSjson.normalize(general_notification.data)