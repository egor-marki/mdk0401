from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrandViewSet, CarViewSet

router = DefaultRouter()
router.register("brands", BrandViewSet, basename="brands")
router.register("cars", CarViewSet, basename="cars")

urlpatterns = [
    path("", include(router.urls)),
]
