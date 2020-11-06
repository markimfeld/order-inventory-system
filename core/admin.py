from django.contrib import admin

# Register your models here.
from core.models import (
    Item, 
    Category, 
    Product, 
    ProductItem,
    Address,
    City,
    Country,
    Province,
    Supplier,
    Purchase,
    PurchaseItem,
    Sale,
    SaleItem,
    Status,
    Customer
)

class ProductItemInline(admin.TabularInline):
    model = ProductItem


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductItemInline, ]


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem


class PurchaseAdmin(admin.ModelAdmin):
    inlines = [PurchaseItemInline, ]


class SaleItemInline(admin.TabularInline):
    model = SaleItem


class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline, ]


admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(ProductItem)
admin.site.register(Address)
admin.site.register(City)
admin.site.register(Status)
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseItem)
admin.site.register(Supplier)
admin.site.register(Customer)
