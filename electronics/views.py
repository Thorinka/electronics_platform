from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from electronics.models import Product, NetworkNode
from electronics.paginators import NetworkNodePaginator, ProductPaginator
from electronics.serializers import ProductSerializer, NetworkNodeSerializer


# Product CRUD
class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('id').distinct()
    permission_classes = [IsAuthenticated]
    pagination_class = ProductPaginator


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]


class ProductUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]


class ProductDestroyAPIView(generics.DestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]


# NetworkNode CRUD
class NetworkNodeCreateAPIView(generics.CreateAPIView):
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsAuthenticated]


class NetworkNodeListAPIView(generics.ListAPIView):
    serializer_class = NetworkNodeSerializer
    queryset = NetworkNode.objects.all().order_by('id').distinct()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('country',)
    pagination_class = NetworkNodePaginator

class NetworkNodeRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = NetworkNodeSerializer
    queryset = NetworkNode.objects.all()
    permission_classes = [IsAuthenticated]


class NetworkNodeUpdateAPIView(generics.UpdateAPIView):
    serializer_class = NetworkNodeSerializer
    queryset = NetworkNode.objects.all()
    permission_classes = [IsAuthenticated]


class NetworkNodeDestroyAPIView(generics.DestroyAPIView):
    serializer_class = NetworkNodeSerializer
    queryset = NetworkNode.objects.all()
    permission_classes = [IsAuthenticated]
