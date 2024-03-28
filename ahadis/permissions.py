from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticatedOrReadOnly, IsAuthenticated, \
    IsAdminUser
from .models import *

MODIFY_METHODS = ('DELETE', 'PATCH', 'PUT')


def is_superuser(user):
    return user.is_superuser


def is_superuser_and_empty_owner(user, owner):
    return is_superuser(user) & (owner is None)


class PublicContentPermission(BasePermission):
    def has_permission(self, request, view):
        return IsAuthenticatedOrReadOnly().has_permission(request, view)


class NarrationPermission(BasePermission):
    def has_permission(self, request, view):
        if not IsAuthenticated().has_permission(request, view):
            return False

        user_id = int(request.query_params.get('user_id', -1))
        request_user = request.user
        if request.method in SAFE_METHODS:
            if user_id != -1:
                return user_id == request_user.id
            return IsAuthenticated().has_permission(request, view)
        if request.method == 'POST':
            return IsAdminUser().has_permission(request, view)
        if view.action in ('retrieve', 'destroy', 'update', 'partial_update'):
            pk = view.kwargs.get('pk')
            narration = Narration.objects.get(id=pk)
            content_owner = narration.owner
            return (request_user == content_owner) | is_superuser_and_empty_owner(request_user, content_owner)
        return False


class NarrationRelatedFieldPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return NarrationPermission().has_permission(request, view)

        request_user = request.user
        if request.method == 'POST':
            narration_id = request.data.get('narration')
            narration = Narration.objects.get(id=narration_id)
            content_owner = narration.owner
            return (request_user == content_owner) | is_superuser_and_empty_owner(request_user, content_owner)

        if view.action in ('update', 'partial_update'):
            narration_id = request.data.get('narration')
            if narration_id:
                return False
        if view.action in ('update', 'partial_update', 'destroy'):
            pk = view.kwargs.get('pk')
            requested_object = view.queryset.get(id=pk)
            content_owner = requested_object.narration.owner
            return (request_user == content_owner) | is_superuser_and_empty_owner(request_user, content_owner)
        return False


class BookmarkPermission(BasePermission):
    def has_permission(self, request, view):
        if not IsAuthenticated().has_permission(request, view):
            return False
        if request.method in ('GET', 'POST'):
            return True
        if request.method == 'DELETE':
            pk = view.kwargs.get('pk')
            bookmark = Bookmark.objects.get(id=pk)
            return bookmark.user == request.user
