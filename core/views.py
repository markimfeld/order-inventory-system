from django.contrib import messages

from django.db import transaction
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.shortcuts import render, reverse 
from django.views.generic import TemplateView
from django.views import View

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, 
    UpdateView,
    DeleteView
)

from core.models import (
    Item, 
    Product, 
    Category, 
    ProductItem,
    Supplier,
    Purchase,
    Sale,
    SaleItem,
    Customer
)

from core.forms import (
    ProductForm, 
    ProductItemFormSet, 
    PurchaseForm,
    PurchaseItemFormSet,
    SaleForm,
    SaleItemForm,
    SaleProductFormSet
)



# Create your views here.
class DashBoard(TemplateView):
    template_name = 'core/index.html'

# ITEMS
class ItemView(ListView):
    model = Item
    template_name = 'core/products/items.html'


class ItemCreateView(CreateView):
    model = Item
    fields = ('name', 'description', 'image')
    template_name = 'core/products/item-add.html'
    success_url = reverse_lazy('core:items')


class ItemEditView(UpdateView):
    model = Item
    fields = ('name', 'description', 'image')
    template_name = 'core/products/item-edit.html'
    success_url = reverse_lazy('core:items')


class ItemDeactivateView(TemplateView):
    template_name = 'core/products/item-deactivate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['item'] = Item.objects.get(pk=kwargs.get('pk'))
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        item_pk = kwargs.get('pk')
        item = Item.objects.get(pk=item_pk)
        if item is not None:
            item.deactivate()
        
        return HttpResponseRedirect(reverse('core:items'))


class ItemActivateView(TemplateView):
    template_name = 'core/products/item-activate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = Item.objects.get(pk=kwargs.get('pk'))
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        item_pk = kwargs.get('pk')
        item = Item.objects.get(pk=item_pk)
        if item is not None:
            item.activate()
        
        return HttpResponseRedirect(reverse('core:items'))


# CATEGORIES
class CategoryView(ListView):
    model = Category
    template_name = 'core/products/category.html'


class CategoryCreateView(CreateView):
    model = Category
    fields = ('name', )
    template_name = 'core/products/category-add.html'
    success_url = reverse_lazy('core:categories')


class CategoryEditView(UpdateView):
    model = Category
    fields = ('name', )
    template_name = 'core/products/category-edit.html'
    success_url = reverse_lazy('core:categories')


class CategoryDeactivateView(TemplateView):
    template_name = 'core/products/category-deactivate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=kwargs.get('pk'))
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        category_pk = kwargs.get('pk')
        category = Category.objects.get(pk=category_pk)
        if category is not None:
            category.deactivate()
        
        return HttpResponseRedirect(reverse('core:categories'))


class CategoryActivateView(TemplateView):
    template_name = 'core/products/category-activate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=kwargs.get('pk'))
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        category_pk = kwargs.get('pk')
        category = Category.objects.get(pk=category_pk)
        if category is not None:
            category.activate()
        
        return HttpResponseRedirect(reverse('core:categories'))

# PRODUCTS
class ProductView(ListView):
    model = Product
    template_name = 'core/products/products.html'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'core/products/product-add.html'
    form_class = ProductForm
    success_url = None

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['items'] = ProductItemFormSet(self.request.POST)
        else:
            context['items'] = ProductItemFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        
        with transaction.atomic():
            if items.is_valid():
                self.object = form.save()
                items.instance = self.object
                items.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('core:products')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'core/products/product-detail.html'
    success_url = reverse_lazy('core:products')

class ProductEditView(UpdateView):
    model = Product
    template_name = 'core/products/product-edit.html'
    form_class = ProductForm
    success_url = None

    def get_context_data(self, **kwargs):
        context = super(ProductEditView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['items'] = ProductItemFormSet(self.request.POST, instance=self.object)
        else:
            context['items'] = ProductItemFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']

        with transaction.atomic():
            if items.is_valid():
                self.object = form.save()
                items.instance = self.object
                items.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        print(form.errors)
        return super(ProductCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('core:products')


class ProductDeactivateView(TemplateView):
    template_name = 'core/products/product-deactivate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=kwargs.get('pk'))
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        product_pk = kwargs.get('pk')
        product = Product.objects.get(pk=product_pk)
        if product is not None:
            product.deactivate()
        
        return HttpResponseRedirect(reverse('core:products'))


class ProductActivateView(TemplateView):
    template_name = 'core/products/product-activate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=kwargs.get('pk'))
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        product_pk = kwargs.get('pk')
        product = Product.objects.get(pk=product_pk)
        if product is not None:
            product.activate()
        
        return HttpResponseRedirect(reverse('core:products'))


# SUPPLIERS
class SupplierView(ListView):
    model = Supplier
    template_name = 'core/suppliers/suppliers.html'


class SupplierCreateView(CreateView):
    model = Supplier
    fields = ('name', 'phone', 'address', )
    template_name = 'core/suppliers/supplier-add.html'
    success_url = reverse_lazy('core:suppliers')


class SupplierEditView(UpdateView):
    model = Supplier
    fields = ('name', 'phone', 'address', )
    template_name = 'core/suppliers/supplier-edit.html'
    success_url = reverse_lazy('core:suppliers')


class SupplierDeactivateView(TemplateView):
    template_name = 'core/suppliers/supplier-deactivate.html'

    def get_context_data(self, **kwargs):
        context = super(SupplierDeactivateView, self).get_context_data(**kwargs)
        context['supplier'] = Supplier.objects.get(pk=kwargs.get('pk'))
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        supplier_pk = kwargs.get('pk')
        supplier = Supplier.objects.get(pk=supplier_pk)
        if supplier is not None:
            supplier.deactivate()
        
        return HttpResponseRedirect(reverse('core:suppliers'))


class SupplierActivateView(TemplateView):
    template_name = 'core/suppliers/supplier-activate.html'

    def get_context_data(self, **kwargs):
        context = super(SupplierActivateView, self).get_context_data(**kwargs)
        context['supplier'] = Supplier.objects.get(pk=kwargs.get('pk'))
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        supplier_pk = kwargs.get('pk')
        supplier = Supplier.objects.get(pk=supplier_pk)
        if supplier is not None:
            supplier.activate()
        
        return HttpResponseRedirect(reverse('core:suppliers'))


# PURCHASES
class PurchaseView(ListView):
    model = Purchase
    template_name = 'core/suppliers/purchases.html'


class PurchaseCreateView(CreateView):
    model = Purchase
    template_name = 'core/suppliers/purchase-add.html'
    form_class = PurchaseForm
    success_url = None

    def get_context_data(self, **kwargs):
        context = super(PurchaseCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['items'] = PurchaseItemFormSet(self.request.POST)
        else:
            context['items'] = PurchaseItemFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['items']

        with transaction.atomic():
            if formset.is_valid():
                self.object = form.save()
                formset.instance = self.object

                items = formset.save(commit=False)

                for it in items:
                    it.calculate_subtotal()
                    quantity = it.quantity
                    it.item.increase_inventory(quantity)

                self.object.calculate_total()

                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('core:purchases')


class PurchaseEditView(UpdateView):
    model = Purchase
    template_name = 'core/suppliers/purchase-edit.html'
    form_class = PurchaseForm
    success_url = None

    def get_context_data(self, **kwargs):
        context = super(PurchaseEditView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['items'] = PurchaseItemFormSet(self.request.POST, instance=self.object)
        else:
            context['items'] = PurchaseItemFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        
        with transaction.atomic:
            if items.is_valid():
                self.object = form.save()
                items.instance = self.object
                items.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        print(form.errors)
        return super(PurchaseCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('core:purchases')


class PurchaseDeleteView(DeleteView):
    model = Purchase
    template_name = 'core/suppliers/purchase-delete.html'
    success_url = reverse_lazy('core:purchases')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        items = self.object.get_items.all()

        for it in items:
            quantity = it.quantity
            it.item.decrease_inventory(quantity)

        return super(PurchaseDeleteView, self).delete(request)


# SALES
class SaleView(ListView):
    model = Sale
    template_name = 'core/sales/sales.html'


class SaleCreateView(CreateView):
    model = Sale
    template_name = 'core/sales/sale-add.html'
    form_class = SaleForm
    success_url = None

    def get_context_data(self, **kwargs):
        context = super(SaleCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['products'] = SaleProductFormSet(self.request.POST)
        else:
            context['items'] = Item.objects.all()
            context['products'] = SaleProductFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['products']

        
        with transaction.atomic():
            if formset.is_valid():
                self.object = form.save()
                formset.instance = self.object

                # get all products from formset
                products = formset.save(commit=False)

                total_quantity = 0

                for sale_item in products:
                    sale_item.calculate_subtotal()
                    sale_quantity = sale_item.quantity
                    for product_item in sale_item.product.get_items.all():
                        product_quantity = product_item.quantity
                        total_quantity = sale_quantity * product_quantity
                        ok = product_item.item.decrease_inventory(total_quantity)
                        if not ok:
                            message = f'El Stock no alcanza: hay ({product_item.item.inventory}) {product_item.item.name} disponibles'
                            messages.add_message(self.request, messages.ERROR, message)
                            self.object.delete()
                            return self.render_to_response(self.get_context_data(form=form))



                self.object.calculate_total()
                self.object.customer.increase_points(total_quantity)

                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('core:sales')


class SaleEditView(UpdateView):
    model = Sale
    template_name = 'core/sales/sale-edit.html'
    form_class = SaleForm
    success_url = None

    def get_context_data(self, **kwargs):
        context = super(SaleEditView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['products'] = SaleProductFormSet(self.request.POST, instance=self.object)
        else:
            context['products'] = SaleProductFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['products']

        with transaction.atomic():
            if formset.is_valid():
                # check if a form has changed
                for f in formset:
                    if f.has_changed():
                        sale_item = f.cleaned_data['id']
                        self.object.reset_stock(sale_item)

                self.object = form.save()
                formset.instance = self.object

                # get all products from formset
                products = formset.save(commit=False)

                for sale_item in products:
                    sale_item.calculate_subtotal()
                    sale_quantity = sale_item.quantity
                    for product_item in sale_item.product.get_items.all():
                        product_quantity = product_item.quantity
                        total_quantity = sale_quantity * product_quantity
                        product_item.item.decrease_inventory(total_quantity)

                self.object.calculate_total()

                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('core:sales')


class SaleDetailView(DetailView):
    model = Sale
    template_name = 'core/sales/sale-detail.html'
    success_url = reverse_lazy('core:sales')


class SaleDeleteView(DeleteView):
    model = Sale
    template_name = 'core/sales/sale-delete.html'
    success_url = reverse_lazy('core:sales')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        products = self.object.get_products.all()

        for sale_item in products:
            sale_quantity = sale_item.quantity
            for product_item in sale_item.product.get_items.all():
                product_quantity = product_item.quantity
                total_quantity = sale_quantity * product_quantity
                product_item.item.increase_inventory(total_quantity)

        return super(SaleDeleteView, self).delete(request)


# CUSTOMERS
class CustomerView(ListView):
    model = Customer
    template_name = 'core/customers/customers.html'


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'core/customers/customer-detail.html'
    success_url = reverse_lazy('core:customers')


class CustomerCreateView(CreateView):
    model = Customer
    fields = ('first_name', 'last_name', 'address', )
    template_name = 'core/customers/customer-add.html'
    success_url = reverse_lazy('core:customers')


class CustomerEditView(UpdateView):
    model = Customer
    fields = ('first_name', 'last_name', 'address', )
    template_name = 'core/customers/customer-edit.html'
    success_url = reverse_lazy('core:customers')


class CustomerDeactivateView(TemplateView):
    template_name = 'core/customers/customer-deactivate.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerDeactivateView, self).get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(pk=kwargs.get('pk'))
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        customer_pk = kwargs.get('pk')
        customer = Customer.objects.get(pk=customer_pk)
        if customer is not None:
            customer.deactivate()
        
        return HttpResponseRedirect(reverse('core:customers'))


class CustomerActivateView(TemplateView):
    template_name = 'core/customers/customer-activate.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerActivateView, self).get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(pk=kwargs.get('pk'))
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        customer_pk = kwargs.get('pk')
        customer = Customer.objects.get(pk=customer_pk)
        if customer is not None:
            customer.activate()
        
        return HttpResponseRedirect(reverse('core:customers'))
