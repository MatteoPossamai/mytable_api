from rest_framework import permissions

from .tasks import is_token_valid

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # USE CELERY TO CHECK IF LOGGED AND IS THE CORRECT USER

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

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
