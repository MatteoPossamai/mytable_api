from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework import permissions

from ..models.restaurant import Restaurant
from ..serializers.restaurant import RestaurantSerializer

from utilities import is_jsonable, IsOwnerOrReadOnly

# CREATE
# Create the restaurant
class RestaurantCreateView(generics.CreateAPIView):
    # https://www.youtube.com/watch?v=_nZygPQ3gmo&list=PLBKfJRrwXFBL4ty47nf4LXxvkL7Kf0huF&index=8
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# UPDATE
# Retrieve the restaurant
class RestaurantPutView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class RestaurantChangePlan(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def put(self, request, pk, format=None):
        try:
            id = int(pk)
            instance = Restaurant.objects.get(id=id)
            plan = request.data.get('plan')
            if not is_jsonable(plan):
                return Response({'error': 'Plan must be JSON serializable'}, status=status.HTTP_400_BAD_REQUEST)
            instance.plan = plan
            instance.save()
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Plan changed'}, status=status.HTTP_200_OK)

# DELETE
# Delete the restaurant
class RestaurantDeleteView(generics.DestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
