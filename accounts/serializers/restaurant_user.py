from rest_framework import serializers

from accounts.models import RestaurantUser
from restaurant.models import Restaurant

class RestaurantUserSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(many=True, queryset=Restaurant.objects.all()) # ? 
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = RestaurantUser
        fields = (
            'id',
            'username',
            'email',
            'restaurants',
            'owner',
            'level',
        )