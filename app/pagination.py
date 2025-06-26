from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

class CustomPagination(PageNumberPagination):
    page_size = 10  # Default qiymat
    page_size_query_param = 'limit'  # Frontenddan keladigan parametr
    max_page_size = 100  # Maksimal ruxsat berilgan limit

    def get_page_size(self, request):
        """Limitni dinamik olish"""
        limit = request.query_params.get(self.page_size_query_param, self.page_size)
        try:
            return min(int(limit), self.max_page_size)
        except ValueError:
            return self.page_size

    def get_paginated_response(self, data):
        page_size = self.get_page_size(self.request)  # Foydalanuvchi kiritgan limit
        total_items = self.page.paginator.count  # Jami natijalar soni
        total_pages = math.ceil(total_items / page_size)  # Umumiy sahifalar soni

        return Response({
            'count': total_items,  # Jami natijalar soni
            'total_pages': total_pages,  # Umumiy sahifalar soni
            'current_page': self.page.number,  # Hozirgi sahifa
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,  # Sahifadagi natijalar
        })
