from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ( WeatherViewSet,HomeView)


router = DefaultRouter()
router.register('weather', WeatherViewSet)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # This should be named 'home'
    path('api/v1/', include(router.urls)),

]