from typing import Any, List
from channels.generic.websocket import AsyncWebsocketConsumer
from channels import exceptions
from . import permissions, authentication


class WSAsyncConsumer(AsyncWebsocketConsumer):
    permission_classes: List = []
    authentication_classes: List = [authentication.WSTokenAuthentication]

    async def get_permissions(self):
        return [permission() for permission in self.permission_classes]
    
    async def get_authenticators(self):
        return [auth() for auth in self.authentication_classes]

    async def validate_permissions(self) -> bool:
        for permission in await self.get_permissions():
            if not await permission.has_permission(self):
                return False
        return True
    
    async def validate_authentication(self):
        for auth in await self.get_authenticators():
            if await auth.authenticate(self):
                return True
        return False
    

    async def startup(self):
        pass

    async def teardown(self):
        pass

    async def connect(self):
        await self.validate_authentication()
        is_valid = await self.validate_permissions()
        if not is_valid:
            raise exceptions.DenyConnection()
        await self.startup()
        await self.accept()

    async def disconnect(self, close_code):
        try:
            await self.teardown()
        except:
            pass

    async def receive(self, text_data):
        pass