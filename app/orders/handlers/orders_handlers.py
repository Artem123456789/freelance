from typing import List

from app.orders.enitites.orders_entities import ChooseEmployeeInputEntity
from app.orders.models import (
    Order,
    OrderExecution,
    OrderExecutionEmployeeInfo,
    OrderExecutionCustomerInfo,
)

from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()


class OrdersHandler:

    def __init__(self, order: Order = None):
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
        self.order.datetime_employee_selected = now()
        self.order.deadline_date = input_entity.deadline_date

        self.order.save()

    def complete_order(self) -> None:
        self.order.is_done = True
        self.order.datetime_compelete = now()
        self.order.save()

    def employee_orders(self, user: User) -> List[Order]:
        employee_executions = OrderExecutionEmployeeInfo.objects.filter(user=user)
        order_executions = OrderExecution.objects.filter(execution_employee_info__in=employee_executions)

        orders = Order.objects.filter(order_execution__in=order_executions)
        return orders
