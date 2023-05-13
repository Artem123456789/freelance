from app.orders.enitites.orders_entities import ChooseEmployeeInputEntity
from app.orders.models import (
    Order,
    OrderExecution,
    OrderExecutionEmployeeInfo,
    OrderExecutionCustomerInfo,
)

from django.contrib.auth import get_user_model

User = get_user_model()


class OrdersHandler:

    def __init__(self, order: Order):
        self.order = order

    def choose_employee(
        self,
        input_entity: ChooseEmployeeInputEntity,
    ) -> None:
        order_execution = OrderExecution()

        execution_employee_info = OrderExecutionEmployeeInfo(user=input_entity.employee)
        execution_employee_info.save()

        execution_customer_info = OrderExecutionCustomerInfo(user=input_entity.customer)
        execution_customer_info.save()

        order_execution.execution_employee_info = execution_employee_info
        order_execution.execution_customer_info = execution_customer_info
        order_execution.save()

        self.order.is_employee_selected = True
        self.order.order_execution = order_execution

        self.order.save()
