from rest_framework import permissions
import jwt

from .tasks import is_token_valid
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
        print(type(obj))
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return decoded['user'] == obj.owner.email

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
