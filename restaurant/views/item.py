from rest_framework import generics, status, views
from django.http.response import JsonResponse

from ..models.item import Item
from ..models.category import Category
from ..models.restaurant import Restaurant
from ..serializers.item import ItemSerializer

from utilities import is_jsonable, IsOwnerOrReadOnly, IsLogged, save_object_to_cache, get_object_from_cache, delete_object_from_cache

# CREATE
# Create the item
class ItemCreateView(views.APIView):
    permission_classes = [IsLogged]
    
    def post(self, request, format=None):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            save_object_to_cache('item_' + str(serializer.data['id']), serializer.data)
            delete_object_from_cache(f'item_a_r_{serializer.data["restaurant"]}')
            delete_object_from_cache(f'item_a_a_{serializer.data["restaurant"]}')
            delete_object_from_cache(f'item_a_c_{serializer.data["category"]}')
            delete_object_from_cache(f'item_a_ac_{serializer.data["category"]}')
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# READ
# Get the item list
class ItemGetAllView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# Get single item
class ItemGetView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def get(self, request, pk, format=None):
        try:
            item = get_object_from_cache('item_' + str(pk))
            if item is None:
                item = Item.objects.get(id=pk)
                item = ItemSerializer(item).data
                save_object_to_cache('item_' + str(pk), item)
            return JsonResponse(item, status=status.HTTP_200_OK)

        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        except:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

class ItemGetByRestaurantView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def get(self, request, pk, format=None):
        try: 
            restaurant_item = get_object_from_cache(f'item_a_r_{pk}')
            if restaurant_item is not None:
                return JsonResponse(restaurant_item, status=status.HTTP_200_OK, safe=False)

            restaurant_item = []
            items = Item.objects.filter(restaurant=pk)
            for item in items:
                item = ItemSerializer(item).data
                restaurant_item.append(item)
            save_object_to_cache(f'item_a_r_{pk}', {'items' : restaurant_item})
            return JsonResponse({'items' : restaurant_item}, status=status.HTTP_200_OK, safe=False)

        except Restaurant.DoesNotExist:
            return JsonResponse({'error': 'Restaurant does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

class ItemGetByRestaurantActiveView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def get(self, request, pk, format=None):
        try: 
            restaurant_item = get_object_from_cache(f'item_a_a_{pk}')
            if restaurant_item is not None:
                return JsonResponse(restaurant_item, status=status.HTTP_200_OK, safe=False)

            restaurant_item = []
            items = Item.objects.filter(restaurant=pk)
            for item in items:
                if item.isActive:
                    item = ItemSerializer(item).data
                    restaurant_item.append(item)
            save_object_to_cache(f'item_a_a_{pk}', {'items' : restaurant_item})
            return JsonResponse({'items' : restaurant_item}, status=status.HTTP_200_OK, safe=False)

        except Restaurant.DoesNotExist:
            return JsonResponse({'error': 'Restaurant does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

class ItemGetByCategoryView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def get(self, request, pk, format=None):
        try: 
            category_item = get_object_from_cache(f'item_a_c_{pk}')
            if category_item is not None:
                return JsonResponse(category_item, status=status.HTTP_200_OK)

            category_item = []
            items = Item.objects.filter(category=pk)
            for item in items:
                item = ItemSerializer(item).data
                category_item.append(item)
            save_object_to_cache(f'item_a_c_{pk}', {'items' : category_item})
            return JsonResponse({'items' : category_item}, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

class ItemGetByCategoryActiveView(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]

    def get(self, request, pk, format=None):
        try: 
            category_item = get_object_from_cache(f'item_a_ac_{pk}')
            if category_item is not None:
                return JsonResponse(category_item, status=status.HTTP_200_OK)

            category_item = []
            items = Item.objects.filter(category=pk)
            for item in items:
                if item.isActive:
                    item = ItemSerializer(item).data
                    category_item.append(item)
            save_object_to_cache(f'item_a_ac_{pk}', {'items' : category_item})
            return JsonResponse({'items' : category_item}, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

# UPDATE
# Retrieve the item
class ItemPutView(views.APIView):
    def put(self, request, pk, format=None):
        try:
            item = request.data
            instance = Item.objects.get(id=pk)
            instance.name = item['name']
            instance.description = item['description']
            instance.price = item['price']
            instance.iconId = item['iconId']
            instance.facts = item['facts']
            instance.number = item['number']
            instance.isActive = item['isActive']
            instance.save()
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'success': 'Item updated'}, status=status.HTTP_200_OK)

class ItemsChangeNumberView(views.APIView):
    def put(self, request, format=None):
        try:
            items = request.data.get('items')
            for item in items:
                instance = Item.objects.get(id=item['id'])
                instance.number = item['number']
                instance.save()
        except:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'success': 'Number changed'}, status=status.HTTP_200_OK)
        

class ItemsChangeActiveView(views.APIView):
    def put(self, request, format=None):
        try:
            items = request.data.get('items')
            for item in items:
                instance = Item.objects.get(id=item['id'])
                instance.isActive = item['isActive']
                instance.save()
        except:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'success': 'Active changed'}, status=status.HTTP_200_OK)

class ItemsBulkUpdate(views.APIView):
    permission_classes = [IsLogged, IsOwnerOrReadOnly]
    

# DELETE
# Delete the item
class ItemDeleteView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]
    