from django.db import models


def filter_out_forbidden_queryset_items(queryset, request_user_id, query_params_user_id):
    if request_user_id == query_params_user_id:
        queryset = queryset.filter(models.Q(owner__id=query_params_user_id))
    elif query_params_user_id == -1:
        queryset = queryset.filter(models.Q(owner__is_superuser=True) | models.Q(owner=None))
    else:
        queryset = queryset.none()

    return queryset
