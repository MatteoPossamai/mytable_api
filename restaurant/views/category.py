from rest_framework import generics, status, views
from django.http.response import JsonResponse

from ..models.category import Category, Restaurant
from ..serializers.category import CategorySerializer

from utilities import IsOwnerOrReadOnly, IsLogged


class CategoryCreateView(generics.CreateAPIView):
    """
    Description: handle the creation of a new Category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsLogged]


class CategoryGetAllView(generics.ListAPIView):
    """
    Description: returns all the categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryGetView(generics.RetrieveAPIView):
    """
    Description: returns a single category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]


class CategoryGetAllByRestaurant(views.APIView):
    """
    Description: returns all the categories of a restaurant
    """
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
    """
    Description: returns all the active categories of a restaurant
    """
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


class CategoryPutView(generics.RetrieveUpdateDestroyAPIView):
    """
    Description: handle the update of a single category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]


class CategoriesChangeNumberView(views.APIView):
    """
    Description: handle the update of the number of a set of categories
    """
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
    """
    Description: handle the update of the isActive attribute of a set of categories
    """
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
    """
    Description: handle the update of a set of categories
    """
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


class CategoryDeleteView(generics.DestroyAPIView):
    """
    Description: handle the deletion of a single category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]
