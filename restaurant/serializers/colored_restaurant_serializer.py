from rest_framework import serializers

from restaurant.models import Restaurant

class ColoredRestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = (
            'id',
            'name',
            'color_palette',
            'border',
        )