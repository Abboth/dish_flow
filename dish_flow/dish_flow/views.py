from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

@extend_schema(tags=["HealthCheck"])
class HealthCheck(APIView):
    def get(self, request):
        return Response({"status": "ok"})