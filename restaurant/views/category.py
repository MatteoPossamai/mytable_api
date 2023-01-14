from rest_framework import generics, status, views
from django.http.response import JsonResponse

from ..models.category import Category, Restaurant
from ..serializers.category import CategorySerializer

from utilities import IsOwnerOrReadOnly, IsLogged, save_object_to_cache, get_object_from_cache

# CREATE
# Create the category
class CategoryCreateView(views.APIView):
    permission_classes = [IsLogged]
    
    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            save_object_to_cache('category_' + str(serializer.data['id']), serializer.data)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# READ
# Get the category list
class CategoryGetAllView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryGetAllRestaurant(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def get(self, request, pk, format=None):
        try:  
            all_categories = get_object_from_cache(f'categories_a_r_{pk}')
            if all_categories is not None:
                return JsonResponse({"categories": all_categories}, status=status.HTTP_200_OK)
            
            categories = []
            restaurant = Restaurant.objects.get(id=pk)
            for category in restaurant.category_set.all():
                serialized = CategorySerializer(category)
                categories.append(serialized.data)
            
            save_object_to_cache(f'categories_a_r_{pk}', categories)
            
            return JsonResponse({'categories': categories}, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

class CategoryGetAllActiveView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]
    
    def get(self, request, pk, format=None):
        try:
            all_actives = get_object_from_cache(f'categories_a_a_{pk}')
            if all_actives is not None:
                return JsonResponse({"categories": all_actives}, status=status.HTTP_200_OK)
            categories = []
            restaurant = Restaurant.objects.get(id=pk)
            for category in restaurant.category_set.all():
                if category.isActive:
                    serialized = CategorySerializer(category)
                    categories.append(serialized.data)
            
            save_object_to_cache(f'categories_a_a_{pk}', categories)
            
            return JsonResponse({'categories': categories}, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

# Get single category
class CategoryGetView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def get(self, request, pk, format=None):
        try:
            category = get_object_from_cache('category_' + str(pk))
            if category is None:
                category = Category.objects.get(id=pk)
                save_object_to_cache('category_' + str(pk), category)
            return JsonResponse(category, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        except:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

# UPDATE
# Retrieve the category
class CategoryPutView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoriesChangeNumberView(views.APIView):
    def put(self, request, format=None):
        try:
            categories = request.data.get('categories')
            for category in categories:
                instance = Category.objects.get(id=category['id'])
                instance.number = category['number']
                instance.save()
        except:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'success': 'Number changed'}, status=status.HTTP_200_OK)

class CategoriesChangeActiveView(views.APIView):
    def put(self, request, format=None):
        try:
            categories = request.data.get('categories')
            for category in categories:
                instance = Category.objects.get(id=category['id'])
                instance.isActive = category['isActive']
                instance.save()
        except:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'success': 'Active changed'}, status=status.HTTP_200_OK)

# DELETE
# Delete the category
class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]
