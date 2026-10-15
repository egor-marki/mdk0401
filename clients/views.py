from rest_framework import viewsets, filters
from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """CRUD для клиентов."""
    queryset = Client.objects.select_related("manager").all()
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["full_name", "phone", "email"]
    ordering_fields = ["created_at", "full_name"]
