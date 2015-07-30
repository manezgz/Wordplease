from rest_framework.permissions import BasePermission

MY_SAFE_METHODS = ('HEAD', 'OPTIONS')

class UserPermission(BasePermission):

    def has_permission(self, request, view):

        if request.method == "POST":
            return True
        elif request.user.is_superuser:
            return True
        elif view.action != 'list' and request.user.is_authenticated():
            return True

    def has_object_permission(self, request, view, obj):

        if request.method in MY_SAFE_METHODS:
            return True
        if request.method == "POST":
            return True
        elif request.user.is_superuser:
            return True
        if request.method == 'GET' and view.action == 'list':
            return False
        return request.user == obj
