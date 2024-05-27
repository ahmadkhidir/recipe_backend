from django.urls import path
from recipes import consumers

urlpatterns = [
    path('<recipe_id>/discussions/', consumers.DiscussionConsumer.as_asgi(), name='discussions'),
]
