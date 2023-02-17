from rest_framework import generics, status, views
from django.http.response import JsonResponse
import jwt
import stripe
from django.conf import settings

from ..models.restaurant import Restaurant
from ..serializers.restaurant import RestaurantSerializer
from accounts.models import RestaurantUser

from utilities import IsOwnerOrReadOnly, IsLogged
from mytable.settings import JWT_SECRET


class RestaurantCreateView(views.APIView):
    """
    Description: handle the creation of a new Restaurant
    """
    permission_classes = [IsLogged]

    def post(self, request, format=None):
        token = request.headers.get('token')
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = RestaurantUser.objects.get(pk=decoded['user'])

        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantGetAllView(generics.ListAPIView):
    """
    Description: returns all the restaurants
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsOwnerOrReadOnly]


class RestaurantGetView(generics.RetrieveAPIView):
    """
    Description: returns a single restaurant
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get(self, request, pk, *args, **kwargs):
        restaurant = self.get_object()
        serializer = RestaurantSerializer(restaurant)

        # Get the owner of the restaurant
        owner = restaurant.owner.stripe_customer_id
        
        # Get the subscription
        subscription = stripe.Subscription.list(customer=owner)

        prices = []
        products = []

        for sub in subscription.data:
            if sub.status == 'active' or sub.status == 'trialing' or sub.status == 'incomplete_expired':
                items = stripe.SubscriptionItem.list(
                    subscription=sub.id,
                )

                for item in items.data:
                    prices.append(item.price.id)
                    products.append(item.price.product)

        data = {
            "base_menu": True if settings.BASIC_MENU in products else False, 
            "image_menu": True if settings.IMAGE_MENU in products else False,
            "client_order": True if settings.CLIENT_ORDER in products else False,
            "waiter_order": True if settings.WAITER_ORDER in products else False,
        }

        return JsonResponse({"restaurant":serializer.data, "auth": data}, status=status.HTTP_200_OK)


class RestaurantPutView(generics.RetrieveUpdateDestroyAPIView):
    """
    Description: update a restaurant
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]


class RestaurantDeleteView(generics.DestroyAPIView):
    """
    Description: delete a restaurant
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]
