from rest_framework import generics, status, views
from rest_framework.response import Response

from ..models.order import Order

from ..models.takes import Take
from ..serializers.takes import TakeSerializer

from restaurant.models import Item
from utilities import IsRestaurantOwner, IsLogged


class TakesCreateView(generics.CreateAPIView):
    """
    Description: Create a take
    """
    queryset = Take.objects.all()
    serializer_class = TakeSerializer
    permission_classes = []

    def post(self, request, format=None):
        try:
            # Get the order
            order_id = request.data['order']
            order = Order.objects.get(id=order_id)
            # Get the item
            item_id = request.data['item']
            item = Item.objects.get(id=item_id)
            # Get the quantity
            quantity = request.data['quantity']
            # Get the batch
            batch = request.data['batch']
            # Create the take
            take = Take.objects.create(order=order, item=item, quantity=quantity, batch=batch)
            serializer = TakeSerializer(take)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


class TakesGetAllView(generics.ListAPIView):
    """
    Description: Get all the takes
    """
    queryset = Take.objects.all()
    serializer_class = TakeSerializer
    permission_classes = [IsLogged, IsRestaurantOwner]


class TakesGetAllByOrder(generics.ListAPIView):
    """
    Description: Get all the takes by order
    """
    permission_classes = [IsLogged, IsRestaurantOwner]

    def get(self, request, order_pk, format=None):
        try:
            takes = Take.objects.filter(order_id=order_pk)
            serializer = TakeSerializer(takes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


class TakesGetSingleView(generics.ListAPIView):
    """
    Description: Get a single take
    """
    permission_classes = [IsLogged, IsRestaurantOwner]
    
    def get(self, request, pk, format=None):
        try:
            take = Take.objects.get(id=pk)
            serializer = TakeSerializer(take)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


class TakesUpdateView(generics.UpdateAPIView):
    """
    Description: Update a take
    """
    queryset = Take.objects.all()
    serializer_class = TakeSerializer
    permission_classes = [IsLogged, IsRestaurantOwner]


class TakesDeleteView(generics.DestroyAPIView):
    """
    Description: Delete a take
    """
    queryset = Take.objects.all()
    serializer_class = TakeSerializer
    permission_classes = [IsLogged, IsRestaurantOwner]


class TakesDeleteAllByOrder(generics.DestroyAPIView):
    """
    Description: Delete all the takes by order
    """    
    permission_classes = [IsLogged, IsRestaurantOwner]

    def delete(self, request, order_pk, format=None):
        try:
            takes = Take.objects.filter(order__id=order_pk)
            takes.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


class TakesDeleteAllByRestaurant(generics.DestroyAPIView):
    """
    Description: Delete all the takes by restaurant
    """
    permission_classes = [IsLogged, IsRestaurantOwner]

    def delete(self, request, restaurant_pk, format=None):
        try:
            takes = Take.objects.filter(order__restaurant__pk=restaurant_pk)
            takes.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
