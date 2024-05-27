from django.urls import path
from notifications import consumers

urlpatterns = [
    path('', consumers.NotificationConsumer.as_asgi(), name='notifications'),
]