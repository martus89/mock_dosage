from rest_framework.permissions import BasePermission


class IsViewOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='view_only').exists():
            if view.action in ['create', 'update', 'partial_update', 'destroy']:
                return False
        return True
