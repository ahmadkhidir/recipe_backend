from . import websocket
from channels.auth import get_user, login


class AbstractWSPermission:
    async def has_permission(self, consumer:'websocket.WSAsyncConsumer') -> bool:
        return True


class WSIsAuthenticated(AbstractWSPermission):
    async def has_permission(self, consumer:'websocket.WSAsyncConsumer') -> bool:
        user = consumer.scope['user']
        # user = await get_user(consumer.scope) # Later (backend.get_user)
        return user.is_authenticated
    