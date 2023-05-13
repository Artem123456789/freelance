from dataclasses import dataclass
from datetime import date

from django.contrib.auth import get_user_model

User = get_user_model()


@dataclass
class ChooseEmployeeInputEntity:
    employee: User
    customer: User
    deadline_date: date
