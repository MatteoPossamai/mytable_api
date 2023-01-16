from rest_framework import generics, status, views
from django.http.response import JsonResponse

from ..models.item import Item
from ..models.category import Category
from ..models.restaurant import Restaurant
from ..serializers.item import ItemSerializer

from utilities import is_jsonable, IsOwnerOrReadOnly, IsLogged

# CREATE
# Create the item
class ItemCreateView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsLogged]

# READ
# Get the item list
class ItemGetAllView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# Get single item
class ItemGetView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

class ItemGetByRestaurantView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def get(self, request, pk, format=None):
        try: 
            restaurant_item = []
            
            items = Item.objects.filter(category__restaurant=pk)
            for item in items:
                item = ItemSerializer(item).data
                restaurant_item.append(item)

            return JsonResponse({'items': restaurant_item}, status=status.HTTP_200_OK, safe=False)

        except Restaurant.DoesNotExist:
            return JsonResponse({'error': 'Restaurant does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

class ItemGetByRestaurantActiveView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def get(self, request, pk, format=None):
        try: 
            restaurant_item = []
            items = Item.objects.filter(category__restaurant=pk)
            for item in items:
                if item.isActive:
                    item = ItemSerializer(item).data
                    restaurant_item.append(item)
            return JsonResponse({'items' : restaurant_item}, status=status.HTTP_200_OK, safe=False)

        except Restaurant.DoesNotExist:
            return JsonResponse({'error': 'Restaurant does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

class ItemGetByCategoryView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def get(self, request, pk, format=None):
        try:
            category_item = []
            items = Item.objects.filter(category=pk)
            for item in items:
                item = ItemSerializer(item).data
                category_item.append(item)
            return JsonResponse({'items' : category_item}, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

class ItemGetByCategoryActiveView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def get(self, request, pk, format=None):
        try: 
            category_item = []
            items = Item.objects.filter(category=pk)
            for item in items:
                if item.isActive:
                    item = ItemSerializer(item).data
                    category_item.append(item)
            return JsonResponse({'items' : category_item}, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

# UPDATE
# Retrieve the item
class ItemPutView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]


class ItemsChangeActiveView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def put(self, request, format=None):
        try:
            items = request.data.get('items')
            category_pk = items[0]['category']
            for item in items:
                category_id = item['category']
                if category_id != category_pk:
                    return JsonResponse({'error': 'Cannot modify elements of different categories'}, status=status.HTTP_400_BAD_REQUEST)
                
                instance = Item.objects.get(id=item['id'])
                instance.isActive = item['isActive']
                instance.save()
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'success': 'Active changed'}, status=status.HTTP_200_OK)


class ItemsChangeNumberView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def put(self, request, format=None):
        try:
            items = request.data.get('items')
            category_pk = items[0]['category']

            for item in items:
                category_id = item['category']
                if category_id != category_pk:
                    return JsonResponse({'error': 'Cannot modify elements of different categories'}, status=status.HTTP_400_BAD_REQUEST)
                
                instance = Item.objects.get(id=item['id'])
                instance.number = item['number']
                instance.save()
        except:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'success': 'Number changed'}, status=status.HTTP_200_OK)

class ItemsBulkUpdate(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def put(self, request, format=None):
        try:
            items = request.data.get('items')
            category_pk = items[0]['category']

            restaurant_id = Category.objects.get(id=category_pk).restaurant.id

            for item in items:
                category_id = item['category']
                if category_id != category_pk:
                    return JsonResponse({'error': 'Cannot modify elements of different categories'}, status=status.HTTP_400_BAD_REQUEST)
                
                instance = Item.objects.get(id=item['id'])
                instance.name = item['name']
                instance.description = item['description']
                instance.price = item['price']
                instance.iconId = item['iconId']
                instance.facts = item['facts']
                instance.number = item['number']
                instance.isActive = item['isActive']
                instance.save()
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'success': 'Number changed'}, status=status.HTTP_200_OK)
    

# DELETE
# Delete the item
class ItemDeleteView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]
    