from rest_framework import generics, status, views
from rest_framework.response import Response

from ..models.order import Order
from ..serializers.order import OrderSerializer

from ..models.takes import Take
from ..serializers.takes import TakeSerializer

from restaurant.models import Item
from restaurant.serializers.item import ItemSerializer

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
            print(e)
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
                print(e)
                return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)