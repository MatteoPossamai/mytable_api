from rest_framework import serializers

from restaurant.models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    
    class Meta:
        model = Restaurant
        fields = (
            'id',
            'name',
            'plan',
            'location',
            'phone',
            'description',
            'payment_method',
            'licence_expiration',
            'owner'
        )