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
            print(e)
            return JsonResponse({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

# READ
# Get the restaurant user list
class RestaurantUserGetAllView(generics.ListAPIView):
    queryset = RestaurantUser.objects.all()
    serializer_class = RestaurantUserSerializer

# Get single restaurant user
class RestaurantUserGetView(generics.RetrieveAPIView):
    
    def get(self, request, email, format=None):
        try:
            user = RestaurantUser.objects.get(email=email)
            serializer = RestaurantUserSerializer(user)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

# UPDATE
# Modify username
class RestaurantUserPutUserName(views.APIView):
    permission_classes = [IsLogged]

    def put(self, request, email, format=None):
        try:
            # Get the user email from the request
            user_email = request.data.get("user")
            new_username = request.data.get("username")

            if (new_username == None or new_username == "" or len(new_username) < 3 or len(new_username) > 20):
                return JsonResponse({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if the user that request the delete is the one that needs to be updated
            # otherwise, all fails
            if email != user_email:
                return JsonResponse({'error': 'You cannot request to update another user'},
                 status=status.HTTP_401_UNAUTHORIZED)

            # Delete the user itself
            user = RestaurantUser.objects.get(email=email)
            user.username = new_username
            user.save()

            # Return the success deletion
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return JsonResponse({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

# Modify Password
class RestaurantUserPutPassword(views.APIView):
    permission_classes = [IsLogged]

    def put(self, request, email, format=None):
        try:
            # Get the user email from the request
            user_email = request.data.get("user")
            new_password = request.data.get("password")
            
            # Check if the user that request the delete is the one that needs to be updated
            # otherwise, all fails
            if email != user_email:
                return JsonResponse({'error': 'You cannot request to update another user'},
                 status=status.HTTP_401_UNAUTHORIZED)

            valid, error = valid_password(new_password)
            if not valid:
                return JsonResponse({'error': error}, status=status.HTTP_400_BAD_REQUEST)

            # Delete the user itself
            user = RestaurantUser.objects.get(email=email)
            user.password = Encryptor.encrypt(new_password)
            user.save()

            # Return the success deletion
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    
# DELETE
# Delete the restaurant user
class RestaurantUserDeleteView(views.APIView):
    permission_classes = [IsLogged]
    
    def post(self, request, email, format=None):
        try:
            # Get the user email from the request
            user_email = request.data.get("user")
            
            # Check if the user that request the delete is the one that needs to be deleted
            # otherwise, all fails
            if email != user_email:
                return JsonResponse({'error': 'You cannot request to delete another user'},
                 status=status.HTTP_401_UNAUTHORIZED)

            # Delete the user itself
            user = RestaurantUser.objects.get(email=email)
            user.delete()

            # Return the success deletion
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

# Login
class RestaurantUserLoginView(views.APIView):  
    
    def post(self, request, format=None):
        data = request.data
        try:
            # Get the user and the token from the request
            token = request.headers.get('token')
            user = data.get('email')
            password = data.get('password')

            # Check via redis if the token is still valid, checking if it is
            # in the cache, otherwise, it is time to create a new one
            if token is not None and is_token_valid(token, user):
                return JsonResponse({'token': token}, status=status.HTTP_200_OK)
            
            # Get the user from the database
            user = RestaurantUser.objects.get(email=user)

            # Check if the password is correct
            if not Encryptor.check_password(password, user.password):
                return JsonResponse({'error': 'Incorrect password given'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create a new token
            token = jwt.encode({'user': user.email, 'hash': str(datetime.now())}, 'secret', algorithm='HS256')

            # Save the token to redis
            save_user_token_to_redis(user, token)

            # Return the success, and the token itself
            return JsonResponse({'token': token}, status=status.HTTP_200_OK)

        # If user does not exists
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST) 
            
# Logged
class RestaurantUserLogged(views.APIView):
    permission_classes = [IsLogged]

    def post(self, request, format=None):
        return JsonResponse({'Logged': True}, status=status.HTTP_200_OK)

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
            return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_403_FORBIDDEN)
