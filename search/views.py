from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

from rest_api.serializers import ProductInventorySerializer
from search.documents import ProductInventoryDocument


class SearchProductInventory(APIView, LimitOffsetPagination):
    productinventory_serializer = ProductInventorySerializer
    search_document = ProductInventoryDocument

    def get(self, request, query):
        try:
            q = Q(
                'multi_match',
                query=query,
                fields=[
                    #'sku'
                    'product.name'
                ], fuzziness='auto'
            ) & Q(
                'bool',
                should=[
                    Q('match', is_default=True)
                ]
            )

            search = self.search_document().search().query(q)
            total = search.count()
            search = search[0:total]
            response = search.execute()

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.productinventory_serializer(results, many=True)
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            return HttpResponse(e, status=500)
