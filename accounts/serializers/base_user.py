from rest_framework import serializers

from accounts.models import BaseUser

class BaseUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BaseUser
        fields = (
            'id',
            'email',
            'username',
            'language',
        )