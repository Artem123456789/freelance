from django.contrib.auth import get_user_model

from rest_framework.exceptions import PermissionDenied

from app._auth.entities.auth_entities import RegisterInputEntity

User = get_user_model()


class AuthHandler:

    def register(self, input_entity: RegisterInputEntity) -> User:
        if User.objects.filter(username=input_entity.username).exists():
            raise PermissionDenied("User with this username exists")

        user = User(username=input_entity.username)
        user.set_password(input_entity.password)
        user.customer_description = input_entity.customer_description
        user.employee_description = input_entity.employee_description
        user.save()
        return user
