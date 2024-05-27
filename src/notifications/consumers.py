from notifications.mixins import NotificationMixin
from restful_channels.websocket import WSAsyncConsumer
from restful_channels.permissions import WSIsAuthenticated
from restful_channels.helpers import WSRequest


class NotificationConsumer(WSAsyncConsumer, NotificationMixin):
    permission_classes = [WSIsAuthenticated]


    async def receive(self, text_data):
        request = WSRequest.parse(text_data)
        match request.action:
            case "all":
                await self.send_notification(request)