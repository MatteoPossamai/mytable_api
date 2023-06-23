from rest_framework import generics, status, views
from django.http.response import JsonResponse
import jwt
import stripe
from django.conf import settings

from ..models.restaurant import Restaurant
from ..serializers.restaurant import RestaurantSerializer
from ..serializers.colored_restaurant_serializer import ColoredRestaurantSerializer
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
        try:
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

            palette = [restaurant.color_palette[i] for i in range(len(restaurant.color_palette)) ]
            border = restaurant.border

            data = {
                "base_menu": True if settings.BASIC_MENU in products else False, 
                "image_menu": True if settings.IMAGE_MENU in products else False,
                "client_order": True if settings.CLIENT_ORDER in products else False,
                "waiter_order": True if settings.WAITER_ORDER in products else False,
            }

            palette_data = {
                "primary": str(palette[0]),
                "secondary": str(palette[1]),
                "box": str(palette[2]),
                "bg": str(palette[3]),
                "text": str(palette[4]),
            }

            return JsonResponse({"restaurant":serializer.data, "auth": data, "palette": palette_data, "border": border}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RestaurantPutView(generics.RetrieveUpdateDestroyAPIView):
    """
    Description: update a restaurant
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]


class RestaurantPutColorView(generics.RetrieveUpdateDestroyAPIView):
    """
    Description: update a restaurant
    """
    queryset = Restaurant.objects.all()
    serializer_class = ColoredRestaurantSerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def put(self, request, pk, *args, **kwargs):
        print(request.data)
        try:
            restaurant = self.get_object()
            if len(request.data['data']['colors']) == len(restaurant.color_palette):
                restaurant.color_palette = request.data['data']['colors']
                border = int(request.data['data']['border'])
                restaurant.border = border
                restaurant.save()
                return JsonResponse({"Status":"Changed"}, status=status.HTTP_200_OK)
            return JsonResponse("Unvalid Input data: number of color is uncorrect", 
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantDeleteView(generics.DestroyAPIView):
    """
    Description: delete a restaurant
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]
