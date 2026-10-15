from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from apps.orders.models import Order
from apps.catalog.models import Car


class ReportService:
    """Сервис отчётов."""

    @staticmethod
    def kpi(days: int = 30) -> dict:
        """Главные KPI."""
        since = timezone.now() - timedelta(days=days)
        completed = Order.objects.filter(
            order_type=Order.OrderType.PURCHASE,
            status=Order.Status.COMPLETED,
            created_at__gte=since,
        )
        revenue = completed.aggregate(total=Sum("total_amount"))["total"] or 0
        count = completed.count()
        return {
            "revenue": float(revenue),
            "sales_count": count,
            "avg_check": float(revenue) / count if count else 0,
            "in_stock": Car.objects.filter(status=Car.Status.AVAILABLE).count(),
            "period_days": days,
        }

    @staticmethod
    def revenue_by_day(days: int = 30) -> list:
        """Выручка по дням."""
        since = timezone.now() - timedelta(days=days)
        rows = (
            Order.objects.filter(
                order_type=Order.OrderType.PURCHASE,
                status=Order.Status.COMPLETED,
                created_at__gte=since,
            )
            .extra(select={"day": "DATE(created_at)"})
            .values("day")
            .annotate(total=Sum("total_amount"))
            .order_by("day")
        )
        return [{"date": str(r["day"]), "total": float(r["total"])} for r in rows]

    @staticmethod
    def top_models(limit: int = 5) -> list:
        """Топ моделей."""
        rows = (
            Order.objects.filter(
                order_type=Order.OrderType.PURCHASE,
                status=Order.Status.COMPLETED,
            )
            .values("car__brand__name", "car__model")
            .annotate(count=Count("id"))
            .order_by("-count")[:limit]
        )
        return [
            {
                "brand": r["car__brand__name"],
                "model": r["car__model"],
                "count": r["count"],
            }
            for r in rows
        ]

    @staticmethod
    def manager_load(days: int = 30) -> list:
        """Загрузка менеджеров."""
        since = timezone.now() - timedelta(days=days)
        rows = (
            Order.objects.filter(
                order_type=Order.OrderType.PURCHASE,
                created_at__gte=since,
            )
            .values("manager__username")
            .annotate(count=Count("id"), total=Sum("total_amount"))
        )
        return [
            {
                "manager": r["manager__username"],
                "orders": r["count"],
                "total": float(r["total"]) or 0,
            }
            for r in rows
        ]

    @staticmethod
    def stock_status() -> list:
        """Состояние склада."""
        return [
            {"status": r["status"], "count": r["count"]}
            for r in Car.objects.values("status").annotate(count=Count("id"))
        ]
