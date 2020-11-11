from django.urls import path

from core.views import DashBoard

from core.views import (
    # ITEM
    ItemView, 
    ItemCreateView, 
    ItemEditView, 
    ItemDeactivateView, 
    ItemActivateView, 
    # PRODUCT
    ProductView, 
    ProductCreateView,
    ProductDetailView,
    ProductEditView,
    ProductDeactivateView,
    ProductActivateView,
    # CATEGORY
    CategoryView, CategoryCreateView, CategoryEditView, 
    CategoryDeactivateView, 
    CategoryActivateView,
    # SUPPLIER
    SupplierView,
    SupplierCreateView,
    SupplierEditView,
    SupplierActivateView,
    SupplierDeactivateView,
    # PURCHASE
    PurchaseView,
    PurchaseDetailView,
    PurchaseCreateView,
    PurchaseEditView,
    PurchaseDeleteView,
    # SALES
    SaleView,
    SaleCreateView,
    SaleEditView,
    SaleDeleteView,
    SaleDetailView,
    # CUSTOMERS
    CustomerView,
    CustomerCreateView,
    CustomerEditView,
    CustomerDeactivateView,
    CustomerActivateView,
    CustomerDetailView,
)

app_name = 'core'
urlpatterns = [
    # DASHBOARD
    path('', DashBoard.as_view(), name='index'),
    # PRODUCTS AND CATEGORY
    # ITEMS
    path('items/', ItemView.as_view(), name='items'),
    path('items/add/', ItemCreateView.as_view(), name='item-add'),
    path('items/edit/<int:pk>/', ItemEditView.as_view(), name='item-edit'),
    path('items/deactivate/<int:pk>/', ItemDeactivateView.as_view(), name='item-deactivate'),
    path('items/activate/<int:pk>/', ItemActivateView.as_view(), name='item-activate'),
    # PRODUCTS
    path('products/', ProductView.as_view(), name='products'),
    path('products/add/', ProductCreateView.as_view(), name='product-add'),
    path('products/edit/<int:pk>/', ProductEditView.as_view(), name='product-edit'),
    path('products/detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/deactivate/<int:pk>/', ProductDeactivateView.as_view(), name='product-deactivate'),
    path('products/activate/<int:pk>/', ProductActivateView.as_view(), name='product-activate'),
    # CATEGORIES
    path('categories/', CategoryView.as_view(), name='categories'),
    path('categories/add/', CategoryCreateView.as_view(), name='category-add'),
    path('categories/edit/<int:pk>/', CategoryEditView.as_view(), name='category-edit'),
    path('categories/deactivate/<int:pk>/', CategoryDeactivateView.as_view(), name='category-deactivate'),
    path('categories/activate/<int:pk>/', CategoryActivateView.as_view(), name='category-activate'),
    # SUPPLIERS
    path('suppliers/', SupplierView.as_view(), name='suppliers'),
    path('suppliers/add/', SupplierCreateView.as_view(), name='supplier-add'),
    path('suppliers/edit/<int:pk>/', SupplierEditView.as_view(), name='supplier-edit'),
    path('suppliers/deactivate/<int:pk>/', SupplierDeactivateView.as_view(), name='supplier-deactivate'),
    path('suppliers/activate/<int:pk>/', SupplierActivateView.as_view(), name='supplier-activate'),
    # PURCHASES
    path('purchases/', PurchaseView.as_view(), name='purchases'),
    path('purchases/add/', PurchaseCreateView.as_view(), name='purchase-add'),
    path('purchases/edit/<int:pk>/', PurchaseEditView.as_view(), name='purchase-edit'),
    path('purchases/detail/<int:pk>/', PurchaseDetailView.as_view(), name='purchase-detail'),
    path('purchases/delete/<int:pk>/', PurchaseDeleteView.as_view(), name='purchase-delete'),
    # SALES
    path('sales/', SaleView.as_view(), name='sales'),
    path('sales/add/', SaleCreateView.as_view(), name='sale-add'),
    path('sales/edit/<int:pk>/', SaleEditView.as_view(), name='sale-edit'),
    path('sales/detail/<int:pk>/', SaleDetailView.as_view(), name='sale-detail'),
    path('sales/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale-delete'),
    # CUSTOMERS
    path('customers/', CustomerView.as_view(), name='customers'),
    path('customers/add/', CustomerCreateView.as_view(), name='customer-add'),
    path('customers/edit/<int:pk>/', CustomerEditView.as_view(), name='customer-edit'),
    path('customers/detail/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('customers/deactivate/<int:pk>/', CustomerDeactivateView.as_view(), name='customer-deactivate'),
    path('customers/activate/<int:pk>/', CustomerActivateView.as_view(), name='customer-activate'),


]
