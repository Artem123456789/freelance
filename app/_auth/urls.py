from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import auth_views

from .views.auth_views import register

app_name = "_auth"

urlpatterns = [
    path("register/", register)
]

router = DefaultRouter()

router.register(
    "users",
    auth_views.UserViewSet,
    basename="users"
)

urlpatterns += router.get_urls()
