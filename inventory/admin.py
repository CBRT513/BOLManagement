from django.contrib import admin
from .models import (
    Item, Size, Supplier, Customer, Carrier, Truck, 
    Location, Batch, BOL, BOLItem
)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_code', 'item_name', 'standard_bag_weight', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['item_code', 'item_name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size_label', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['size_label']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['supplier_name', 'bol_prefix', 'next_bol_no', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['supplier_name', 'bol_prefix']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_code', 'customer_city', 'customer_state', 'is_active']
    list_filter = ['is_active', 'customer_state', 'created_at']
    search_fields = ['customer_name', 'customer_code', 'customer_city']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    list_display = ['carrier_name', 'carrier_code', 'contact_name', 'contact_phone', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['carrier_name', 'carrier_code', 'contact_name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ['truck_number', 'carrier', 'trailer_number', 'is_active', 'created_at']
    list_filter = ['is_active', 'carrier', 'created_at']
    search_fields = ['truck_number', 'trailer_number', 'carrier__carrier_name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['location_name', 'customer', 'location_city', 'location_state', 'is_active']
    list_filter = ['is_active', 'customer', 'location_state', 'created_at']
    search_fields = ['location_name', 'customer__customer_name', 'location_city']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['barcode', 'item', 'size', 'supplier', 'current_quantity', 'status', 'receipt_date']
    list_filter = ['status', 'item', 'size', 'supplier', 'receipt_date', 'created_at']
    search_fields = ['barcode', 'lot_number', 'barge', 'item__item_code', 'supplier__supplier_name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'total_weight_mt', 'is_depleted']
    date_hierarchy = 'receipt_date'


class BOLItemInline(admin.TabularInline):
    model = BOLItem
    extra = 1
    readonly_fields = ['weight_mt']


@admin.register(BOL)
class BOLAdmin(admin.ModelAdmin):
    list_display = ['bol_number', 'supplier', 'customer', 'ship_date', 'total_bags', 'total_weight_mt']
    list_filter = ['supplier', 'customer', 'ship_date', 'created_at']
    search_fields = ['bol_number', 'supplier__supplier_name', 'customer__customer_name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'ship_date'
    inlines = [BOLItemInline]


@admin.register(BOLItem)
class BOLItemAdmin(admin.ModelAdmin):
    list_display = ['bol', 'batch', 'quantity_shipped', 'weight_mt']
    list_filter = ['bol__ship_date', 'batch__item', 'batch__supplier']
    search_fields = ['bol__bol_number', 'batch__barcode']
    readonly_fields = ['weight_mt']