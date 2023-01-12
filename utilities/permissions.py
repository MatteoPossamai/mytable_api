from rest_framework import permissions

from .tasks import save_user_token_to_redis, is_token_valid, delete_user_token_from_redis

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

    def has_permission(self, request, view):
        # Read in header the token and user, and if it corresponds, 
        # return True, else return False
        return is_token_valid(request.headers.get('token'), request.data.get('user'))
