from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from rest_framework import generics, status, views
from utilities.tasks import save_user_token_to_redis, is_token_valid, delete_user_token_from_redis
import jwt
from django.db import IntegrityError
from datetime import datetime

from ..models.restaurant_user import RestaurantUser
from ..serializers.restaurant_user import RestaurantUserSerializer
from utilities import Encryptor, valid_password, IsLogged

Encryptor = Encryptor()

# CREATE
# Create the restaurant user
class RestaurantUserCreateView(views.APIView):
    queryset = RestaurantUser.objects.all()
    serializer_class = RestaurantUserSerializer

    def post(self, request, format=None):
        data = request.data
        try:
            # Check if the password is valid
            password = data.get('password')
            password_check = valid_password(password)
            if not password_check[0]:
                return JsonResponse({'error': password_check[1]}, status=status.HTTP_400_BAD_REQUEST)

            # Create the user
            user = RestaurantUser.objects.create(
                username=data.get('username'),
                email=data.get('email'),
                password=Encryptor.encrypt(password),
            )

            # Save the user
            user.save()

            # Create the token
            token = jwt.encode({'user': user.email, 'hash': str(datetime.now())}, 'secret', algorithm='HS256')

            # Save the token to redis
            save_user_token_to_redis(user.email, token)

            # Return the success, and the token itself
            return JsonResponse({'token': token}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return JsonResponse({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

# READ
# Get the restaurant user list
class RestaurantUserGetAllView(generics.ListAPIView):
    queryset = RestaurantUser.objects.all()
    serializer_class = RestaurantUserSerializer

# Get single restaurant user
class RestaurantUserGetView(generics.RetrieveAPIView):
    queryset = RestaurantUser.objects.all()
    serializer_class = RestaurantUserSerializer

# UPDATE
# Retrieve the restaurant user
class RestaurantUserPutView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantUser.objects.all()
    serializer_class = RestaurantUserSerializer
    
# DELETE
# Delete the restaurant user
class RestaurantUserDeleteView(generics.DestroyAPIView):
    queryset = RestaurantUser.objects.all()
    serializer_class = RestaurantUserSerializer 

# Login
class RestaurantUserLoginView(views.APIView):  
    
    def post(self, request, format=None):
        data = request.data
        try:
            # Get the user and the token from the request
            user = request.headers.get('user')
            token = request.headers.get('token')
            password = data.get('password')

            # Check via redis if the token is still valid, checking if it is
            # in the cache, otherwise, it is time to create a new one
            if is_token_valid(token, user):
                return JsonResponse({'token': token}, status=status.HTTP_200_OK)
            
            # Get the user from the database
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_email = payload['user']
            user = RestaurantUser.objects.get(email=user_email)

            # Check if the password is correct
            if not Encryptor.check_password(password, user.password):
                return JsonResponse({'error': 'Incorrect password given'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Create a new token
            token = jwt.encode({'user': user.email, 'hash': str(datetime.now())}, 'secret', algorithm='HS256')

            # Save the token to redis
            save_user_token_to_redis(user_email, token)

            # Return the success, and the token itself
            return JsonResponse({'token': token}, status=status.HTTP_200_OK)

        # If user does not exists
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User does not exists'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status=status.HTTP_401_UNAUTHORIZED) 
            
# Logged
class RestaurantUserLogged(views.APIView):
    permission_classes = [IsLogged]

    def post(self, request, format=None):
        return JsonResponse({'Logged': 'True'}, status=status.HTTP_200_OK)

# Logout
class RestaurantUserLogoutView(views.APIView):
    permission_classes = [IsLogged]
    
    def post(self, request, format=None):
        try:
            # Get the user from the request
            user = request.data.get('user')

            # Delete the token from redis and return success
            delete_user_token_from_redis(user)

            return JsonResponse({'success': 'Logged out'}, status=status.HTTP_200_OK)
        
        except:
            return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
