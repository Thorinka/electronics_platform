from django.urls import path

from electronics.apps import ElectronicsConfig
from electronics.views import ProductCreateAPIView, NetworkNodeCreateAPIView, ProductListAPIView, \
    ProductRetrieveAPIView, ProductUpdateAPIView, ProductDestroyAPIView, NetworkNodeListAPIView, \
    NetworkNodeRetrieveAPIView, NetworkNodeUpdateAPIView, NetworkNodeDestroyAPIView

app_name = ElectronicsConfig.name

urlpatterns = [
    path('product/create/', ProductCreateAPIView.as_view(), name='product_create'),
    path('product/view/', ProductListAPIView.as_view(), name='product_view_list'),
    path('product/view/<int:pk>', ProductRetrieveAPIView.as_view(), name='product_view'),
    path('product/update/<int:pk>', ProductUpdateAPIView.as_view(), name='product_update'),
    path('product/delete/<int:pk>', ProductDestroyAPIView.as_view(), name='product_delete'),


    path('networknode/create/', NetworkNodeCreateAPIView.as_view(), name='networknode_create'),
    path('networknode/view/', NetworkNodeListAPIView.as_view(), name='networknode_view_list'),
    path('networknode/view/<int:pk>', NetworkNodeRetrieveAPIView.as_view(), name='networknode_view'),
    path('networknode/update/<int:pk>', NetworkNodeUpdateAPIView.as_view(), name='networknode_update'),
    path('networknode/delete/<int:pk>', NetworkNodeDestroyAPIView.as_view(), name='networknode_delete'),
]