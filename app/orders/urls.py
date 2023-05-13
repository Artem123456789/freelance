from rest_framework.routers import DefaultRouter
from app.orders.views import orders_views

app_name = "orders"

router = DefaultRouter()
router.register(
    "tags",
    orders_views.TagViewSet,
    basename="tags"
)
router.register("tags", orders_views.TagViewSet, basename="tags")

router.register(
    "categories",
    orders_views.CategoryViewSet,
    basename="categories"
)
router.register("categories", orders_views.CategoryViewSet, basename="categories")

router.register(
    "orders",
    orders_views.OrderViewSet,
    basename="orders"
)
router.register("orders", orders_views.OrderViewSet, basename="orders")

router.register(
    "order_responses",
    orders_views.OrderResponseViewSet,
    basename="order_responses"
)
router.register("order_responses", orders_views.OrderResponseViewSet, basename="order_responses")

router.register(
    "order_execution_customer_infos",
    orders_views.OrderExecutionCustomerInfoViewSet,
    basename="order_execution_customer_infos"
)

router.register(
    "order_execution_employees_infos",
    orders_views.OrderExecutionEmployeeInfoViewSet,
    basename="order_execution_employees_infos"
)


urlpatterns = router.get_urls()
