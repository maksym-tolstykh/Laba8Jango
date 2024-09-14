from django.contrib import admin
from .models import Supplier, Material, Delivery

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'phone', 'bank_account')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('material_name', 'price')

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_date', 'supplier', 'material', 'delivery_days', 'quantity')
