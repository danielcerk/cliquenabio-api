from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from api.product.views import ProductViewSet
from api.links.views import LinkViewSet
from api.auth.views import AccountViewSet

# Colocar as váriaveis do stripe no ENV

router = DefaultRouter()
router.register(r'account', AccountViewSet, basename='account')

account_product_router = NestedDefaultRouter(router, r'account', lookup='account')
account_product_router.register(r'product', ProductViewSet, basename='account-product')

account_link_router = NestedDefaultRouter(router, r'account', lookup='account')
account_link_router.register(r'link', LinkViewSet, basename='account-link')

urlpatterns = [
    path('api/v1/subscription/', include('api.subscriptions.urls')),
    path('api/v1/', include('api.profile_user.urls')),
    path('api/v1/auth/', include('api.auth.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(account_product_router.urls)),
    path('api/v1/', include(account_link_router.urls)),
]
