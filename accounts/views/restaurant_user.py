from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from rest_framework import generics, status, views
from restaurant.models.restaurant import Restaurant
from utilities.tasks import save_user_token_to_redis, is_token_valid, delete_token_from_redis
import jwt
from django.db import IntegrityError
from datetime import datetime
import stripe

from ..models.restaurant_user import RestaurantUser
from ..serializers.restaurant_user import RestaurantUserSerializer
from utilities import Encryptor, IsLogged, valid_password, valid_username
from mytable.settings import JWT_SECRET
from mytable.settings import STRIPE_SECRET

Encryptor = Encryptor()
stripe.api_key = STRIPE_SECRET


class RestaurantUserCreateView(views.APIView):
    """
    Description: handles user creation and signup
    """
    queryset = RestaurantUser.objects.all()
    serializer_class = RestaurantUserSerializer

    def post(self, request, format=None):
        data = request.data
        try:
            # Check if the password is valid
            password = data.get('password')
            password_check, error = valid_password(password)
            if not password_check:
                return JsonResponse({'error': password_check[1]}, status=status.HTTP_400_BAD_REQUEST)

            # Create the user
            user = RestaurantUser.objects.create(
                email=data.get('email'),
                username=data.get('email'),
                password=Encryptor.encrypt(password),
            )

            # Create the stripe customer if the call is not for the test user
            if data.get('email') != "test@test.com" and data.get('email') != "test123@test.com":
                customer = stripe.Customer.create(
                    email=data.get('email'),
                    name=data.get('username'),
                )

                user.stripe_customer_id = customer.id

            # Save the user
            user.save()

            # Create the token
            token = jwt.encode({'user': user.pk, 'date': str(datetime.now())}, JWT_SECRET, algorithm='HS256')
            # Save the token to redis
            save_user_token_to_redis(token)

            # Return the success, and the token itself
            return JsonResponse({'token': token}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            print(e)
            return JsonResponse({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            
            return JsonResponse({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantUserGetAllView(generics.ListAPIView):
    """
    Description: returns all user instance
    """
    queryset = RestaurantUser.objects.all()
    serializer_class = RestaurantUserSerializer


class RestaurantUserGetView(generics.RetrieveAPIView):
    """
    Description: returns a single user instance
    """
    
    def get(self, request, email, format=None):
        try:
            user = RestaurantUser.objects.get(email=email)
            serializer = RestaurantUserSerializer(user)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            
            return JsonResponse({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantUserPutUser(views.APIView):
    """
    Description: handles username and passowrd changes
    """
    permission_classes = [IsLogged]

    def put(self, request, format=None):
        try:

            token = request.headers.get('token')
            decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user_pk = decoded['user'] 

            # Get the user email from the request
            new_username = request.data.get('username')
            new_password = request.data.get('password')

            # Get the user to modify
            user = RestaurantUser.objects.get(id=user_pk)

            # Handle username change
            valid, error = valid_username(new_username)
            if new_username and valid:
                user.username = new_username
            elif new_username:
                return JsonResponse({'error': error}, status=status.HTTP_400_BAD_REQUEST)

            # Handle password change
            valid, error = valid_password(new_password)
            if new_password and valid:
                user.password = Encryptor.encrypt(new_password)
            elif new_password:
                return JsonResponse({'error': error}, status=status.HTTP_400_BAD_REQUEST)

            # Save modifications
            user.save()

            # Return the success deletion
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return JsonResponse({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            
            return JsonResponse({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
    

class RestaurantUserDeleteView(views.APIView):
    """
    Description: handles the user deletion
    """
    permission_classes = [IsLogged]
    
    def delete(self, request, format=None):
        try:      

            token = request.headers.get('token')
            decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user_pk = decoded['user']    

            # Delete the user itself
            user = RestaurantUser.objects.get(id=user_pk)
            user.delete()

            # Return the success deletion
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            
            return JsonResponse({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantUserLoginView(views.APIView):  
    """
    Description: logs in a user
    """
    
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
            
            # Get the restaurant of the user
            restaurant = Restaurant.objects.filter(owner=user)

            # Check if the password is correct
            if not Encryptor.check_password(password, user.password):
                return JsonResponse({'error': 'Incorrect password given'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create a new token
            token = jwt.encode({'user': user.pk, 'hash': str(datetime.now())}, JWT_SECRET, algorithm='HS256')

            # Save the token to redis
            save_user_token_to_redis(token)

            # Return the success, and the token itself
            return JsonResponse({'token': token, 'restaurant_id': restaurant[0].id}, status=status.HTTP_200_OK)

        # If user does not exists
        except ObjectDoesNotExist as e:
            print(e)
            return JsonResponse({'error': 'User does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return JsonResponse({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST) 
            

class RestaurantUserLogged(views.APIView):
    """
    Description: check if user is logged
    """
    permission_classes = [IsLogged]

    def post(self, request, format=None):
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)


class RestaurantUserLogoutView(views.APIView):
    """
    Description: Handles logout in the user flow
    """
    permission_classes = [IsLogged]
    
    def post(self, request, format=None):
        try:
            token = request.headers.get('token')
            # Delete the token from redis and return success
            delete_token_from_redis(token)
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
        except:
            return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_403_FORBIDDEN)


class GetRestaurantUserByRestaurant(views.APIView):
    """
    Description: returns a single user instance
    """
    
    def get(self, request, restaurant_id, format=None):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            user = RestaurantUser.objects.get(id=restaurant.owner.id)
            serializer = RestaurantUserSerializer(user)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            
            return JsonResponse({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)