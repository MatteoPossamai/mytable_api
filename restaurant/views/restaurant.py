from rest_framework import generics, status, views
from django.http.response import JsonResponse
import jwt

from ..models.restaurant import Restaurant
from ..serializers.restaurant import RestaurantSerializer
from accounts.models import RestaurantUser

from utilities import is_jsonable, IsOwnerOrReadOnly, IsLogged
from mytable.settings import JWT_SECRET

# CREATE
# Create the restaurant
class RestaurantCreateView(views.APIView):
    permission_classes = [IsLogged]

    def post(self, request, format=None):
        token = request.headers.get('token')
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = RestaurantUser.objects.get(email=decoded['user'])

        serializer = RestaurantSerializer(data=request.data)
        serializer.owner = user
        if serializer.is_valid():
            serializer.save(owner=user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# READ
# Get the restaurant list
class RestaurantGetAllView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsOwnerOrReadOnly]

# Get single restaurant
class RestaurantGetView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

# UPDATE
# Retrieve the restaurant
class RestaurantPutView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

# Change the restaurant plan
class RestaurantChangePlan(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def put(self, request, pk, format=None):
        try:
            id = int(pk)
            instance = Restaurant.objects.get(id=id)
            plan = request.data.get('plan')
            if not is_jsonable(plan):
                return JsonResponse({'error': 'Plan must be JSON serializable'}, status=status.HTTP_400_BAD_REQUEST)
            instance.plan = plan
            instance.save()

            serializer = RestaurantSerializer(instance)

        except Restaurant.DoesNotExist:
            return JsonResponse({'error': 'Restaurant does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'success': 'Plan changed'}, status=status.HTTP_200_OK)

# DELETE
# Delete the restaurant
class RestaurantDeleteView(generics.DestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]
