from rest_framework.routers import DefaultRouter

from .views import OrdersViewSet

app_name = "orders"

router = DefaultRouter()
router.register(r'orders', OrdersViewSet)

urlpatterns = router.urls