from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class NarrationPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 40

    def get_paginated_response(self, data):
        return Response({
            'page': self.get_page_number(self.request, self.page.paginator),
            'next': self.page.next_page_number(),
            'last': self.page.paginator.num_pages,

            'number_of_records': self.page.paginator.count,
            'results': data
        })
