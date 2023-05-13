from dataclasses import dataclass

from django.contrib.auth import get_user_model

User = get_user_model()


@dataclass
class ChooseEmployeeInputEntity:
    employee: User
    customer: User
