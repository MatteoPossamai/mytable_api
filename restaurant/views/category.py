from rest_framework import generics, status, views
from django.http.response import JsonResponse

from ..models.category import Category, Restaurant
from ..serializers.category import CategorySerializer

from utilities import IsOwnerOrReadOnly, IsLogged

# CREATE
# Create the category
class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsLogged]

# READ
# Get the category list
class CategoryGetAllView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Get single category
class CategoryGetView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

# Get all categories from a restaurant
class CategoryGetAllByRestaurant(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def get(self, request, pk, format=None):
        try:        
            categories = []
            restaurant = Restaurant.objects.get(id=pk)
            for category in restaurant.category_set.all():
                serialized = CategorySerializer(category)
                categories.append(serialized.data)
            
            return JsonResponse({'categories': categories}, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


class CategoryGetAllActiveByRestaurantView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]
    
    def get(self, request, pk, format=None):
        try:
            categories = []
            restaurant = Restaurant.objects.get(id=pk)
            for category in restaurant.category_set.all():
                if category.isActive:
                    serialized = CategorySerializer(category)
                    categories.append(serialized.data)
            
            return JsonResponse({'categories': categories}, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


# UPDATE
# Retrieve the category
class CategoryPutView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

class CategoriesChangeNumberView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def put(self, request, format=None):
        try:
            categories = request.data.get('categories')
            restaurant_pk = categories[0]['restaurant']
            for category in categories:
                restaurant_id = category['restaurant']
                if restaurant_id != restaurant_pk:
                    return JsonResponse({'error': 'Cannot modify from different restaurant'},
                     status=status.HTTP_400_BAD_REQUEST)

                instance = Category.objects.get(id=category['id'])
                instance.number = category['number']
                instance.save()

        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

class CategoriesChangeActiveView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def put(self, request, format=None):
        try:
            categories = request.data.get('categories')
            restaurant_pk = categories[0]['restaurant']
            for category in categories:
                restaurant_id = category['restaurant']
                if restaurant_id != restaurant_pk:
                    return JsonResponse({'error': 'Cannot modify from different restaurant'},
                     status=status.HTTP_400_BAD_REQUEST)

                instance = Category.objects.get(id=category['id'])
                instance.isActive = category['isActive']

                instance.save()
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

class CategoriesBulkUpdate(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def put(self, request, format=None):
        try:
            categories = request.data.get('categories')
            restaurant_pk = categories[0]['restaurant']
            for category in categories:
                restaurant_id = category['restaurant']
                if restaurant_id != restaurant_pk:
                    return JsonResponse({'error': 'Cannot modify from different restaurant'},
                     status=status.HTTP_400_BAD_REQUEST)

                instance = Category.objects.get(id=category['id'])
                instance.name = category['name']
                instance.number = category['number']
                instance.isActive = category['isActive']
                instance.save()

        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

# DELETE
# Delete the category
class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]
