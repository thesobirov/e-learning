from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_superuser



class IsSuperUserOrTeacherOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser or request.user.groups.filter(name="Teacher").exists():
            return True

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_superuser

class IsTeacherOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.groups.filter(name="Teacher").exists()


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="User").exists() and request.method == 'GET'
