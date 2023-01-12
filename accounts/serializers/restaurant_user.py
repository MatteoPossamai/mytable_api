from rest_framework import serializers

from accounts.models import RestaurantUser
from restaurant.models import Restaurant

class RestaurantUserSerializer(serializers.ModelSerializer):
    restaurants = serializers.PrimaryKeyRelatedField(many=True, queryset=Restaurant.objects.all(),
        allow_null=True, default=None)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = RestaurantUser
        fields = (
            'id',
            'username',
            'email',
            'password',
            'owner',
            'restaurants',
        )