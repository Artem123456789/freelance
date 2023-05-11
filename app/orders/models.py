import uuid

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from app.libs.base_models import NamedModel

from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class OrderExecutionEmployeeInfo(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField(null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _("Отзыв об исполнителе заказа")
        verbose_name_plural = _("Отзывы об исполнителях заказов")


class OrderExecutionCustomerInfo(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField(null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _("Отзыв об инициаторе заказа")
        verbose_name_plural = _("Отзывы об инициаторах заказов")


class OrderExecution(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

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


class Tag(NamedModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Тэг")
        verbose_name_plural = _("Тэги")


class Category(NamedModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


class Order(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    is_done = models.BooleanField(null=True, blank=True, default=False)
    order_execution = models.ForeignKey(OrderExecution, null=True, blank=True, on_delete=models.SET_NULL)
    is_employee_selected = models.BooleanField(null=True, blank=True, default=False)

    tags = models.ManyToManyField(Tag, null=True, blank=True)
    categories = models.ManyToManyField(Category, null=True, blank=True)

    @property
    def responses(self):
        return OrderResponse.objects.filter(order=self)

    @property
    def links_to_communicate(self):
        return LinkToCommunicate.objects.filter(user=self.user)

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")


class OrderResponse(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField(null=True, blank=True)
    suggest_price = models.FloatField(null=True, blank=True)
    proposed_deadline = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("Ответ на заказ")
        verbose_name_plural = _("Ответы на заказы")


class CommunicationSource(NamedModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Источник для cвязи")
        verbose_name_plural = _("Источники для cвязи")


class LinkToCommunicate(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    communication_source = models.ForeignKey(CommunicationSource, null=True, blank=True, on_delete=models.SET_NULL)
    link = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("Ссылка для связи")
        verbose_name_plural = _("Ссылки для связи")
