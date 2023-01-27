from rest_framework import generics, status, views
from django.http.response import JsonResponse
import jwt

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
    permission_classes = [IsLogged, IsOwnerOrReadOnly]


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
