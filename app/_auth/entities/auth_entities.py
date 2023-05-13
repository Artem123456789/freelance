from dataclasses import dataclass


@dataclass
class RegisterInputEntity:
    username: str
    password: str
    customer_description: str
    employee_description: str


@dataclass
class RegisterResponseEntity:
    user_id: int
