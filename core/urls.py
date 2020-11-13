from django.contrib.auth.decorators import login_required
from django.urls import path

from core.views import (
    # REPORTS
    get_most_sold_products
)

from core.views import (
    # DASHBOARD
    DashBoard,
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
    # REPORTS
    SalesReportView,
)

app_name = 'core'
urlpatterns = [
    # DASHBOARD
    path('', login_required(DashBoard.as_view()), name='index'),
    # PRODUCTS AND CATEGORY
    # ITEMS
    path('items/', login_required(ItemView.as_view()), name='items'),
    path('items/add/', login_required(ItemCreateView.as_view()), name='item-add'),
    path('items/edit/<int:pk>/', login_required(ItemEditView.as_view()), name='item-edit'),
    path('items/deactivate/<int:pk>/', login_required(ItemDeactivateView.as_view()), name='item-deactivate'),
    path('items/activate/<int:pk>/', login_required(ItemActivateView.as_view()), name='item-activate'),
    # PRODUCTS
    path('products/', login_required(ProductView.as_view()), name='products'),
    path('products/add/', login_required(ProductCreateView.as_view()), name='product-add'),
    path('products/edit/<int:pk>/', login_required(ProductEditView.as_view()), name='product-edit'),
    path('products/detail/<int:pk>/', login_required(ProductDetailView.as_view()), name='product-detail'),
    path('products/deactivate/<int:pk>/', login_required(ProductDeactivateView.as_view()), name='product-deactivate'),
    path('products/activate/<int:pk>/', login_required(ProductActivateView.as_view()), name='product-activate'),
    # CATEGORIES
    path('categories/', login_required(CategoryView.as_view()), name='categories'),
    path('categories/add/', login_required(CategoryCreateView.as_view()), name='category-add'),
    path('categories/edit/<int:pk>/', login_required(CategoryEditView.as_view()), name='category-edit'),
    path('categories/deactivate/<int:pk>/', login_required(CategoryDeactivateView.as_view()), name='category-deactivate'),
    path('categories/activate/<int:pk>/', login_required(CategoryActivateView.as_view()), name='category-activate'),
    # SUPPLIERS
    path('suppliers/', login_required(SupplierView.as_view()), name='suppliers'),
    path('suppliers/add/', login_required(SupplierCreateView.as_view()), name='supplier-add'),
    path('suppliers/edit/<int:pk>/', login_required(SupplierEditView.as_view()), name='supplier-edit'),
    path('suppliers/deactivate/<int:pk>/', login_required(SupplierDeactivateView.as_view()), name='supplier-deactivate'),
    path('suppliers/activate/<int:pk>/', login_required(SupplierActivateView.as_view()), name='supplier-activate'),
    # PURCHASES
    path('purchases/', login_required(PurchaseView.as_view()), name='purchases'),
    path('purchases/add/', login_required(PurchaseCreateView.as_view()), name='purchase-add'),
    path('purchases/edit/<int:pk>/', login_required(PurchaseEditView.as_view()), name='purchase-edit'),
    path('purchases/detail/<int:pk>/', login_required(PurchaseDetailView.as_view()), name='purchase-detail'),
    path('purchases/delete/<int:pk>/', login_required(PurchaseDeleteView.as_view()), name='purchase-delete'),
    # SALES
    path('sales/', login_required(SaleView.as_view()), name='sales'),
    path('sales/add/', login_required(SaleCreateView.as_view()), name='sale-add'),
    path('sales/edit/<int:pk>/', login_required(SaleEditView.as_view()), name='sale-edit'),
    path('sales/detail/<int:pk>/', login_required(SaleDetailView.as_view()), name='sale-detail'),
    path('sales/delete/<int:pk>/', login_required(SaleDeleteView.as_view()), name='sale-delete'),
    # CUSTOMERS
    path('customers/', login_required(CustomerView.as_view()), name='customers'),
    path('customers/add/', login_required(CustomerCreateView.as_view()), name='customer-add'),
    path('customers/edit/<int:pk>/', login_required(CustomerEditView.as_view()), name='customer-edit'),
    path('customers/detail/<int:pk>/', login_required(CustomerDetailView.as_view()), name='customer-detail'),
    path('customers/deactivate/<int:pk>/', login_required(CustomerDeactivateView.as_view()), name='customer-deactivate'),
    path('customers/activate/<int:pk>/', login_required(CustomerActivateView.as_view()), name='customer-activate'),
    # REPORTS
    path('reports/sales/', login_required(SalesReportView.as_view()), name='sales-report'),
    path('reports/most-sold-products/', login_required(get_most_sold_products), name='get-most-sold-products'),
]
