from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet, basename='carts')
router.register('customers', views.CustomerViewSet, basename='customers')

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet,
                         basename='product-reviews')

cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items_router.register(
    'items', views.CartItemViewSet, basename='cart-items-list')

# URLConf
urlpatterns = router.urls + products_router.urls + cart_items_router.urls
