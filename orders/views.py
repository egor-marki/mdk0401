from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """CRUD для заказов."""
    queryset = Order.objects.select_related("client", "car", "manager").all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "order_type", "manager"]
    search_fields = ["client__full_name", "car__model", "comment"]
    ordering_fields = ["created_at", "total_amount"]

    def perform_create(self, serializer):
        """Автоматически привязываем текущего вошедшего пользователя как менеджера."""
        serializer.save(manager=self.request.user)
