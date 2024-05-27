from restful_channels.helpers import WSRequest
from restful_channels.websocket import WSAsyncConsumer
from restful_channels import permissions, authentication
from .permissions import RecipeExist
from . import mixins



class DiscussionConsumer(WSAsyncConsumer, mixins.DiscussionMixin):
    permission_classes = [permissions.WSIsAuthenticated, RecipeExist]

    async def startup(self):
        self.room_name = self.scope['url_route']['kwargs']['recipe_id']
        self.room_group_name = f"discussion_{self.room_name}"
        await self.channel_layer.group_add(
                        self.room_group_name,
                        self.channel_name
                    )
        
    async def teardown(self):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            print(f"Disconnected from {self.room_group_name} group.")

    async def connect(self):
        await super().connect()
        await self.send_all_discussions()
    
    async def receive(self, text_data):
        request = WSRequest.parse(text_data)
        match request.action:
            case 'discussion':
                await self.group_send_discussion(request)
            case 'like':
                await self.group_send_like(request)
            case 'unlike':
                await self.group_send_unlike(request)
            case 'delete':
                await self.group_send_delete(request)
            case 'edit':
                await self.group_send_edit(request)