from rest_framework import generics, status
from rest_framework.response import Response

from ..models.order import Order
from ..serializers.order import OrderSerializer

from ..models.takes import Take

from restaurant.models import Item

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

# Update the order status
class OrderUpdateStatusView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def put(self, request, pk, format=None):
        try:
            # Get the order
            order = Order.objects.get(id=pk)
            # Get the order status
            order_status = request.data['order_status']
            # Update the order status
            order.order_status = order_status
            order.save()
            # Return the order
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

# Update the order payment status
class OrderUpdatePaymentStatusView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def put(self, request, pk, format=None):
        try:
            # Get the order
            order = Order.objects.get(id=pk)
            # Get the payment status
            payment_status = request.data['payment_status']
            # Update the payment status
            order.payment_status = payment_status
            order.save()
            # Return the order
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

# DELETE
# Delete the order
class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
