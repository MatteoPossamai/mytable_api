from rest_framework import generics, status
from django.http.response import JsonResponse

from restaurant.models.restaurant import Restaurant

from ..models.order import Order
from ..serializers.order import OrderSerializer

from ..models.takes import Take
from utilities import IsRestaurantOwner, IsLogged, IsAdminUser
from restaurant.models import Item


class OrderCreateView(generics.ListAPIView):
    """
    Description: handles the creation of an order
    """
    permission_classes = [IsLogged]

    def post(self, request, format=None):
        try:
            # Collection of data from the request
            items = request.data['items']
            restaurant_id = request.data['restaurant_id']
            payment_method = request.data['payment_method']
            payment_status = request.data['payment_status']
            note = request.data['note']

            # Create the order
            restaurant = Restaurant.objects.get(id=restaurant_id)
            
            order = Order.objects.create(
                restaurant=restaurant,
                payment_method=payment_method,
                payment_status=payment_status,
                order_status="pending",
                note=note,
            )
            order.save()

            # Create the takes
            for i in range(len(items)):
                item = Item.objects.get(pk=int(items[i].get('id')))
                take = Take.objects.create(
                    order=order,
                    item=item,
                    quantity=items[i].get('quantity'),
                    batch=1,
                )

                take.save()

            serializer = OrderSerializer(order)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


class OrderGetAllView(generics.ListAPIView):
    """
    Description: handles the retrieval of all orders
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsLogged, IsRestaurantOwner]


class OrderGetView(generics.RetrieveAPIView):
    """
    Description: handles the retrieval of a single order
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsLogged, IsRestaurantOwner]


class OrderPutView(generics.RetrieveUpdateDestroyAPIView):
    """
    Description: handles the update of an order
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsLogged, IsRestaurantOwner]


class OrderUpdateStatusView(generics.RetrieveUpdateDestroyAPIView):
    """
    Description: handles the update of an order status
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsLogged, IsRestaurantOwner]

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
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


class OrderUpdatePaymentStatusView(generics.RetrieveUpdateDestroyAPIView):
    """
    Description: handles the update of an order payment status
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsLogged, IsRestaurantOwner]

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
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


class OrderDeleteView(generics.DestroyAPIView):
    """
    Description: handles the deletion of an order
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsLogged, IsRestaurantOwner]


class OrderDeleteAll(generics.DestroyAPIView):
    """
    Description: handles the deletion of all orders
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, format=None):
        try:
            # Delete all orders
            Order.objects.all().delete()
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)