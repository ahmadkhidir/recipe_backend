from restful_channels import websocket
from restful_channels.permissions import AbstractWSPermission


class RecipeExist(AbstractWSPermission):
    async def has_permission(self, consumer: 'websocket.WSAsyncConsumer') -> bool:
        from .models import Recipe
        recipe_id = consumer.scope['url_route']['kwargs']['recipe_id']
        exists = await Recipe.objects.filter(id=recipe_id).aexists()
        return exists