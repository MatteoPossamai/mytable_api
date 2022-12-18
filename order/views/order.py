from rest_framework import generics, status, views
from rest_framework.response import Response

from ..models.order import Order
from ..serializers.order import OrderSerializer

from ..models.takes import Take
from ..serializers.takes import TakeSerializer

from restaurant.models import Item
from restaurant.serializers.item import ItemSerializer

# CREATE
# Create the order
class OrderCreateView(generics.ListAPIView):
    def post(self, request, format=None):
        try:
            # Collection of data from the request
            items = request.data['items']
            quantity = request.data['quantity']
            restaurant_id = request.data['restaurant_id']
            payment_method = request.data['payment_method']
            payment_status = request.data['payment_status']
            note = request.data['note']

            # Create the order
            order = Order.objects.create()
            order.payment_method = payment_method
            order.payment_status = payment_status
            order.order_status = 'Received'
            order.note = note
            order.restaurant_id = restaurant_id
            order.save()

            # Create the takes
            for i in range(len(items)):
                item = Item.objects.get(id=items[i])
                take = Take.objects.create()
                take.order = order
                take.item = item
                take.quantity = quantity[i]
                take.batch = 0
                take.save()

            # Return the order
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

# READ
# Get the order list
class OrderGetAllView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# Get single order
class OrderGetView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# UPDATE
# Retrieve the order
class OrderPutView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# DELETE
# Delete the order
class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
