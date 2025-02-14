from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from api.snaps.views import SnapViewSet
from api.links.views import LinkViewSet
from api.auth.views import AccountViewSet

router = DefaultRouter()
router.register(r'account', AccountViewSet, basename='account')

account_snap_router = NestedDefaultRouter(router, r'account', lookup='account')
account_snap_router.register(r'snap', SnapViewSet, basename='account-snap')

account_link_router = NestedDefaultRouter(router, r'account', lookup='account')
account_link_router.register(r'link', LinkViewSet, basename='account-link')


urlpatterns = [

    path('api/v1/', include('api.dashboard.urls')),
    path('api/v1/', include('api.status.urls')),
    path('api/v1/', include('api.form_contact.urls')),
    path('api/v1/subscription/', include('api.subscriptions.urls')),
    path('api/v1/', include('api.theme.urls')),
    path('api/v1/', include('api.profile_user.urls')),
    path('api/v1/auth/', include('api.auth.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(account_snap_router.urls)),
    path('api/v1/', include(account_link_router.urls)),

]
