from django.contrib import admin

from .models import (
    Tag,
    Category,
    OrderExecution,
    OrderExecutionCustomerInfo,
    OrderExecutionEmployeeInfo,
    Order,
    OrderResponse,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(OrderExecutionEmployeeInfo)
class OrderExecutionEmployeeInfoAdmin(admin.ModelAdmin):
    search_fields = ['user__username']


@admin.register(OrderExecutionCustomerInfo)
class OrderExecutionCustomerInfoAdmin(admin.ModelAdmin):
    search_fields = ['user__username']


@admin.register(OrderExecution)
class OrderExecutionAdmin(admin.ModelAdmin):
    ...


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ['title', 'user__username']


@admin.register(OrderResponse)
class OrderResponseAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
