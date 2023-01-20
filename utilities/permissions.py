from rest_framework import permissions
import jwt

from accounts.models.restaurant_user import RestaurantUser

from .tasks import is_token_valid
from restaurant.models import Restaurant, Category, Item
from order.models import Order, Take
from mytable.settings import JWT_SECRET

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    message = {'error': 'You cannot access this resource'}

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        token = request.headers.get('token')
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        if isinstance(obj, Restaurant):
            return decoded['user'] == obj.owner.pk
        elif isinstance(obj, Category):
            return decoded['user'] == obj.restaurant.owner.pk
        elif isinstance(obj, Item):
            return decoded['user'] == obj.category.restaurant.owner.pk

class IsLogged(permissions.BasePermission):
    """
    Custom permission to only allow logged users to access the API.
    """
    message = {'error': 'Authorization denied'}

    def has_permission(self, request, view):
        """
        Description: Check if the user is logged by checking the token in headers
        """
        token = request.headers.get('token')
        return token is not None and is_token_valid(token)


class IsRestaurantOwner(permissions.BasePermission):
    """
    Custom permission to only allow restaurant owners to access the API.
    """
    message = {'error': 'Your restaurant do not own this order'}

    def has_object_permission(self, request, view, obj):
        """
        Description: Check if the user is logged by checking the token in headers
        """
        token = request.headers.get('token')
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user =  decoded['user']
        if isinstance(obj, Take):
            return user == obj.order.restaurant.owner.pk
        else:
            return user == obj.restaurant.owner.pk


class IsAdminUser(permissions.BasePermission):
    """
    Description: Custom permission to only allow admin users to access the API
    """

    def has_permission(self, request, view):
        token = request.headers.get('token')
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user =  decoded['user']
        user_obj = RestaurantUser.objects.get(pk=user)
        return user_obj.is_staff