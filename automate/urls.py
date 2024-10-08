from django.urls import path, include
from rest_framework.routers import DefaultRouter

from automate.views import ContactViewSet, SyncDataFromWatiToFreshDesk, SyncDataFromShopfloToFreshDesk

router = DefaultRouter()
router.register(r'contact', ContactViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
    path('syncDataFromWatiToFreshDesk/',SyncDataFromWatiToFreshDesk.as_view()),
    path('syncDataFromShopfloToFreshDesk/',SyncDataFromShopfloToFreshDesk.as_view())
]
