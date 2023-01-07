from rest_framework import generics, status, views
from rest_framework.response import Response

from ..models.order import Order
from ..serializers.order import OrderSerializer

from ..models.takes import Take
from ..serializers.takes import TakeSerializer

from restaurant.models import Item
from restaurant.serializers.item import ItemSerializer


# Create
# Create Take
class TakesCreateView(generics.CreateAPIView):
    queryset = Take.objects.all()
    serializer_class = TakeSerializer

    def post(self, request, format=None):
        try:
            # Get the order
            order_id = request.data['order_id']
            order = Order.objects.get(id=order_id)
            # Get the item
            item_id = request.data['item_id']
            item = Item.objects.get(id=item_id)
            # Get the quantity
            quantity = request.data['quantity']
            # Create the take
            take = Take.objects.create(order=order, item=item, quantity=quantity)
            serializer = TakeSerializer(take)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

# READ
# Get the takes list
class TakesGetAllView(generics.ListAPIView):
    queryset = Take.objects.all()
    serializer_class = TakeSerializer

# Get all all the takes by order
class TakesGetAllByOrder(generics.ListAPIView):

    def get(self, request, order_pk, format=None):
        try:
            takes = Take.objects.filter(order_id=order_pk)
            serializer = TakeSerializer(takes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

# Get single take by id
class TakesGetSingleView(generics.ListAPIView):
    
        def get(self, request, format=None):
            try:
                take_id = request.GET['take_id']
                take = Take.objects.get(id=take_id)
                serializer = TakeSerializer(take)
                return Response(serializer.data, status=status.HTTP_200_OK)
    
            except Exception as e:
                return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

# PUT
# Update take
class TakesUpdateView(generics.UpdateAPIView):
    queryset = Take.objects.all()
    serializer_class = TakeSerializer

# DELETE
# Delete take
class TakesDeleteView(generics.DestroyAPIView):
    queryset = Take.objects.all()
    serializer_class = TakeSerializer

# Delete all the takes by order
class TakesDeleteAllByOrder(generics.DestroyAPIView):
    
        def delete(self, request, order_pk, format=None):
            try:
                takes = Take.objects.filter(order_id=order_pk)
                takes.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
    
            except Exception as e:
                return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

# Delete all the takes by restaurant
class TakesDeleteAllByRestaurant(generics.DestroyAPIView):
        
            def delete(self, request, restaurant_pk, format=None):
                try:
                    takes = Take.objects.filter(restaurant_id=restaurant_pk)
                    takes.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
        
                except Exception as e:
                    return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)