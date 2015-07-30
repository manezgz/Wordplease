from rest_framework import permissions

MY_SAFE_METHODS = ('HEAD', 'OPTIONS')

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in MY_SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if request.method == 'GET' and view.action == 'list':
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user