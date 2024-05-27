from rest_framework import serializers
from . import models


class GeneralNotificationSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = models.GeneralNotification
        fields = '__all__'
    

    def get_type(self, obj):
        return "general"