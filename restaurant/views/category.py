from rest_framework import generics, status, views
from django.http.response import JsonResponse

from ..models.category import Category
from ..serializers.category import CategorySerializer

from utilities import is_jsonable, IsOwnerOrReadOnly, IsLogged, save_object_to_cache, get_object_from_cache

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

class CategoryGetAllActiveView(generics.ListAPIView):
    queryset = Category.objects.filter(isActive=True)
    serializer_class = CategorySerializer

# Get single category
class CategoryGetView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

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
