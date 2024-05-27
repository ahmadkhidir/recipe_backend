from channels.db import database_sync_to_async
from channels.auth import get_user, login

class WSTokenAuthentication():
#     Simple token based authentication.
    async def authenticate(self, consumer):
        from rest_framework_simplejwt.tokens import AccessToken
        from django.contrib.auth import get_user_model
        User = get_user_model()
        backend = "rest_framework_simplejwt.backends.TokenBackend"
        try:
            access = dict(consumer.scope['headers'])[
                b'authorization'].decode('utf-8').split(' ')[1]
            token = AccessToken(access)
            user = await User.objects.aget(id=token.payload['user_id'])
            await login(consumer.scope, user, backend=backend)
            return True
        except Exception as e:
            print("Exception on Auth", e)
            return False