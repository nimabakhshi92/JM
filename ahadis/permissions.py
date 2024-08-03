from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticatedOrReadOnly, IsAuthenticated, \
    IsAdminUser
from .models import *
from env import checker_admin_id

MODIFY_METHODS = ('DELETE', 'PATCH', 'PUT')


def is_superuser(user):
    return user.is_superuser


def is_admin(user):
    return user.is_staff


def is_only_admin(user):
    return is_admin(user) and not is_superuser(user)


def is_checker_admin(user):
    return user.id == checker_admin_id


def is_a_non_checker_admin(user):
    return is_admin(user) and not is_checker_admin(user)


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


class SharedNarrationsPermission(BasePermission):
    def has_permission(self, request, view):
        request_user = request.user
        if (view.action in ('update', 'partial_update')
                and ('narration_id' in request.data or 'receiver_id' in request.data or 'sender_id' in request.data)):
            return False

        if is_checker_admin(request_user) and view.action == 'create':
            return False

        if is_checker_admin(request_user):
            return True

        narration_id = request.data.get('narration_id')

        if is_a_non_checker_admin(request_user) and view.action == 'create':
            narration = Narration.objects.get(pk=narration_id)
            if narration.owner != request_user:
                return False

        if is_a_non_checker_admin(request_user) and view.action in ('list', 'create', 'partial_update'):
            return True

        return False


class DuplicateNarrationPermission(BasePermission):
    def has_permission(self, request, view):
        request_user = request.user
        return is_checker_admin(request_user)
