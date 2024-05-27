from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from restful_channels.helpers import WSRequest, WSResponse, WSjson


class DiscussionMixin:
    # Getters
    @database_sync_to_async
    def get_recipe(self):
        from .models import Recipe
        recipe = Recipe.objects.filter(id=self.room_name)
        return recipe.first()

    @database_sync_to_async
    def get_all_discussions(self, recipe):
        from .serializers import DiscussionSerializer
        from .models import Discussion
        discussions = Discussion.objects.filter(recipe=recipe).order_by("timestamp")
        DiscussionSerializer.get_is_liked = lambda _, obj: obj.is_liked(self.scope['user'])
        serializer = DiscussionSerializer(discussions, many=True)
        return WSjson.normalize(serializer.data)
    

    # Senders
    async def send_all_discussions(self):
        recipe = await self.get_recipe()
        if recipe != None:
            discussions = await self.get_all_discussions(recipe)
            # Beautiful init!
            response = WSResponse(
                data=discussions,
                action='discussions'
            )
            await self.send(text_data=response.stringify())
    
    async def send_message(self, event):
        data = event['message']['data']
        action = event['message']['action']
        response = WSResponse(
            data=data,
            action=action
        )
        await self.send(text_data=response.stringify())


    # Group Senders
    async def group_send_discussion(self, request: WSRequest):
        from .serializers import DiscussionSerializer
        DiscussionSerializer.get_is_liked = lambda _, obj: obj.is_liked(self.scope['user'])
        # TODO: Change data user to auth user
        request.data['user'] = self.scope['user'].id
        serializer = DiscussionSerializer(data=request.data)
        if await sync_to_async(serializer.is_valid)():
            await sync_to_async(serializer.save)()
            data = await sync_to_async(lambda: WSjson.normalize(serializer.data))()
            await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'send.message',
                            'message': {'data': data, 'action': request.action}
                        }
                    )
        else:
            error = WSResponse(
                action=request.action,
                error=True,
                error_data=serializer.errors
            )
            await self.send(text_data=error.stringify())


    async def group_send_like(self, request: WSRequest):
        from .models import Discussion
        from .serializers import DiscussionSerializer
        DiscussionSerializer.get_is_liked = lambda _, obj: obj.is_liked(self.scope['user'])
        try:
            instance = await Discussion.objects.aget(id=request.data['id'])
        except:
            error = WSResponse(
                action=request.action,
                error=True,
                error_data='Discussion not found'
            )
            await self.send(text_data=error.stringify())
            return
        else:
            await instance.likes.aadd(self.scope['user'])
            serializer = DiscussionSerializer(instance)
            data = await sync_to_async(lambda: WSjson.normalize(serializer.data))()
        
        await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'send.message',
                        'message': {'data': data, 'action': request.action}
                    }
                )
    
    async def group_send_unlike(self, request: WSRequest):
        from .models import Discussion
        from .serializers import DiscussionSerializer
        DiscussionSerializer.get_is_liked = lambda _, obj: obj.is_liked(self.scope['user'])
        try:
            instance = await Discussion.objects.aget(id=request.data['id'])
        except:
            error = WSResponse(
                action=request.action,
                error=True,
                error_data='Discussion not found'
            )
            await self.send(text_data=error.stringify())
            return
        else:
            await instance.likes.aremove(self.scope['user'])
            serializer = DiscussionSerializer(instance)
            data = await sync_to_async(lambda: WSjson.normalize(serializer.data))()
        
        await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'send.message',
                        'message': {'data': data, 'action': request.action}
                    }
                )
    
    async def group_send_delete(self, request: WSRequest):
        from .models import Discussion
        from .serializers import DiscussionSerializer
        DiscussionSerializer.get_is_liked = lambda _, obj: obj.is_liked(self.scope['user'])
        try:
            instance = await Discussion.objects.aget(id=request.data['id'])
        except:
            error = WSResponse(
                action=request.action,
                error=True,
                error_data='Discussion not found'
            )
            await self.send(text_data=error.stringify())
            return
        else:
            if await sync_to_async(lambda: instance.user)() != self.scope['user']:
                error = WSResponse(
                    action=request.action,
                    error=True,
                    error_data='You are not the author of this discussion'
                )
                await self.send(text_data=error.stringify())
                return
            await instance.adelete()
        
        await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'send.message',
                        'message': {'data': request.data, 'action': request.action}
                    }
                )
    
    async def group_send_edit(self, request: WSRequest):
        from .models import Discussion
        from .serializers import DiscussionSerializer
        DiscussionSerializer.get_is_liked = lambda _, obj: obj.is_liked(self.scope['user'])
        try:
            instance = await Discussion.objects.aget(id=request.data['id'])
        except:
            error = WSResponse(
                action=request.action,
                error=True,
                error_data='Discussion not found'
            )
            await self.send(text_data=error.stringify())
            return
        else:
            if await sync_to_async(lambda: instance.user)() != self.scope['user']:
                error = WSResponse(
                    action=request.action,
                    error=True,
                    error_data='You are not the author of this discussion'
                )
                await self.send(text_data=error.stringify())
                return
            instance.chat = request.data['chat']
            await instance.asave()
            serializer = DiscussionSerializer(instance)
            data = await sync_to_async(lambda: WSjson.normalize(serializer.data))()
        
        await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'send.message',
                        'message': {'data': data, 'action': request.action}
                    }
                )