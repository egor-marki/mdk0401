"""МОДУЛЬ 4 (ЗАКАЗЫ): формы."""

from django import forms
from .models import Order
from apps.catalog.models import Car


class OrderForm(forms.ModelForm):
    """Форма создания заказа."""

    class Meta:
        model = Order
        fields = ["client", "car", "order_type", "total_amount", "comment"]
        widgets = {
            "client": forms.Select(attrs={"class": "form-select"}),
            "car": forms.Select(attrs={"class": "form-select"}),
            "order_type": forms.Select(attrs={"class": "form-select"}),
            "total_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем только доступные авто
        self.fields["car"].queryset = Car.objects.filter(status=Car.Status.AVAILABLE)
