from django.contrib.auth import get_user_model
from config import settings
from django import forms

from core.models import (
    ProductItem, 
    Product,
    Purchase,
    PurchaseItem,
    Item,
    Category,
    Supplier,
    Sale,
    SaleItem,
    Customer
)

from django.forms.models import inlineformset_factory


User = get_user_model()


class ProductForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_active=True).all()

    class Meta:
        model = Product
        # excluyo items porque los agrego luego en el controlador
        exclude = ('items', 'is_active', )


class ProductItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductItemForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(is_active=True).all()

    class Meta:
        model = ProductItem
        exclude = ()


ProductItemFormSet = inlineformset_factory (
    Product, ProductItem, form=ProductItemForm,
    fields=['item', 'product', 'quantity', 'description'], 
    extra=1, 
    can_delete=True,
)


class PurchaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.filter(is_active=True).all()

    class Meta:
        model = Purchase
        exclude = ('items', 'is_active', 'total', )

    purchased_at = forms.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS)

class PurchaseItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PurchaseItemForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(is_active=True).all()

    class Meta:
        model = PurchaseItem
        exclude = ('subtotal', )


PurchaseItemFormSet = inlineformset_factory (
    Purchase, PurchaseItem, form=PurchaseItemForm,
    fields = ['item', 'purchase', 'unit_cost', 'quantity', 'description'],
    extra=1,
    can_delete=True,
)


class SaleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(is_active=True).all()

    class Meta:
        model = Sale
        exclude = ('total', 'products', )

    delivered_at = forms.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS)

class SaleItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SaleItemForm, self).__init__(*args, **kwargs)

        products = Product.products_with_inventory.all()
        self.fields['product'].choices = products

    class Meta:
        model = SaleItem
        exclude = ('subtotal', )


SaleProductFormSet = inlineformset_factory (
    Sale, SaleItem, form=SaleItemForm,
    extra=0,
    can_delete=True,
)
