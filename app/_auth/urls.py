from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.auth_views import (
    register,
    UserViewSet,
)

app_name = "_auth"

urlpatterns = [
    path("register/", register)
]

router = DefaultRouter()

router.register(
    "users",
    UserViewSet,
    basename="users"
)
router.register("users", UserViewSet, basename="users")


urlpatterns += router.get_urls()
