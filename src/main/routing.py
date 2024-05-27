from django.urls import path
from channels.routing import URLRouter
from recipes.routing import urlpatterns as recipes_routing
from notifications.routing import urlpatterns as notifications_routing

urlpatterns = [
    path('ws/recipes/', URLRouter(recipes_routing)),
    path('ws/notifications/', URLRouter(notifications_routing)),
]