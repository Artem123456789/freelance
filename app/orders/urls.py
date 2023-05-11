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


urlpatterns = router.get_urls()
