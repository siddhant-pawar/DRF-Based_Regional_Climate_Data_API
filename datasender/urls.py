from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HomeView,
    TmaxViewSet, TminViewSet, TmeanViewSet,
    RainfallViewSet, SunshineViewSet,
    Raindays1mmViewSet, AirFrostViewSet,
    map_view
)

router = DefaultRouter()
router.register('tmax', TmaxViewSet)
router.register('tmin', TminViewSet)
router.register('tmean', TmeanViewSet)
router.register('rainfall', RainfallViewSet)
router.register('sunshine', SunshineViewSet)
router.register('raindays1mm', Raindays1mmViewSet)
router.register('airfrost', AirFrostViewSet)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # This should be named 'home'
    path('api/v1/', include(router.urls)),
    path('map/', map_view, name='map'),
]