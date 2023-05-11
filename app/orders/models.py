from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from app.libs.base_models import NamedModel

from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class Tag(NamedModel):

    class Meta:
        verbose_name = _("Тэг")
        verbose_name_plural = _("Тэги")


class Category(NamedModel):

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


class OrderExecutionEmployeeInfo(TimeStampedModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField(null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _("Отзыв об исполнителе заказа")
        verbose_name_plural = _("Отзывы об исполнителях заказов")


class OrderExecutionCustomerInfo(TimeStampedModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField(null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _("Отзыв об инициаторе заказа")
        verbose_name_plural = _("Отзывы об инициаторах заказов")


class OrderExecution(TimeStampedModel):
    execution_employee_info = models.ForeignKey(
        OrderExecutionEmployeeInfo,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    execution_customer_info = models.ForeignKey(
        OrderExecutionCustomerInfo,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    is_paid = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = _("Информация об исполнении заказа")
        verbose_name_plural = _("Информация об исполнении заказов")


class Order(TimeStampedModel):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    is_done = models.BooleanField(null=True, blank=True)
    order_execution = models.ForeignKey(OrderExecution, null=True, blank=True, on_delete=models.SET_NULL)
    is_employee_selected = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")


class OrderTags(models.Model):
    tag = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("Тэг заказа")
        verbose_name_plural = _("Тэги заказов")


class OrderCategory(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("Категория заказа")
        verbose_name_plural = _("Категории заказов")


class OrderResponse(TimeStampedModel):
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField(null=True, blank=True)
    suggest_price = models.FloatField(null=True, blank=True)
    proposed_deadline = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("Ответ на заказ")
        verbose_name_plural = _("Ответы на заказы")
