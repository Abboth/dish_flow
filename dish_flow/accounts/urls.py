from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RestaurantViewSet, UserViewSet

app_name = "accounts"

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls