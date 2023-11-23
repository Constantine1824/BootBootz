from rest_framework.permissions import BasePermission
from django.db.models.query import QuerySet

class IsVerified(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_verified)
    
class CanEditCart(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, QuerySet):
            return all(items.cart.user == request.user for items in obj)
        return bool(obj.cart.user == request.user)