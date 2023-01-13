from rest_framework import generics, status, views
from django.http.response import JsonResponse

from ..models.item import Item
from ..serializers.item import ItemSerializer

from utilities import is_jsonable, IsOwnerOrReadOnly, IsLogged, save_object_to_cache, get_object_from_cache

# CREATE
# Create the item
class ItemCreateView(views.APIView):
    permission_classes = [IsLogged]
    
    def post(self, request, format=None):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            save_object_to_cache('item_' + str(serializer.data['id']), serializer.data)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# READ
# Get the item list
class ItemGetAllView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemGetAllActiveView(generics.ListAPIView):
    queryset = Item.objects.filter(isActive=True)
    serializer_class = ItemSerializer

# Get single item
class ItemGetView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

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


# DELETE
# Delete the item
class ItemDeleteView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsLogged, IsOwnerOrReadOnly]
    