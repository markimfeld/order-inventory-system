import datetime

from django.contrib.auth import get_user_model

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.contrib import messages 
from django.db import transaction
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

from django.shortcuts import render, reverse, redirect 
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
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
    SaleProductFormSet,
    ReportForm
)

User = get_user_model()


from core.utilities import query_is_valid

from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf

# Create your views here.
class DashBoard(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sales_to_prepare'] = Sale.objects.filter(status__name__exact='Preparar')
        context['sales'] = Sale.objects.filter(status__name__exact='Pagado')
        context['revenue'] = Sale.objects.filter(status__name__exact='Pagado').aggregate(value=Coalesce(Sum('total'), Value(0)))
        context['customers'] = Customer.objects.all().count()
        context['items'] = Item.objects.all()
        return context

# ITEMS
class ItemView(ListView):
    model = Item
    template_name = 'core/products/items.html'


class ItemCreateView(CreateView):
    model = Item
    fields = ('name', 'cost', 'description', 'image')
    template_name = 'core/products/item-add.html'
    success_url = reverse_lazy('core:items')

    def form_valid(self, form):
        super(ItemCreateView, self).form_valid(form)
        message = f'El artículo {self.object.name} fue creado exitosamente!'
        messages.add_message(self.request, messages.SUCCESS, message)
        return HttpResponseRedirect(self.get_success_url())


class ItemEditView(UpdateView):
    model = Item
    fields = ('name', 'cost', 'description', 'image')
    template_name = 'core/products/item-edit.html'
    success_url = reverse_lazy('core:items')

    def form_valid(self, form):
        super(ItemEditView, self).form_valid(form)
        message = f'El artículo {self.object.name} fue actualizado exitosamente!'
        messages.add_message(self.request, messages.SUCCESS, message)
        return HttpResponseRedirect(self.get_success_url())


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
            message = f'El artículo "{item.name}" fue desactivado exitosamente!'
            messages.add_message(self.request, messages.SUCCESS, message)
        
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
            message = f'El artículo "{item.name}" fue activado exitosamente!'
            messages.add_message(self.request, messages.SUCCESS, message)
        
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

    def form_valid(self, form):
        super(CategoryCreateView, self).form_valid(form)
        message = f'La categoría {self.object.name} fue creada exitosamente!'
        messages.add_message(self.request, messages.SUCCESS, message)
        return HttpResponseRedirect(self.get_success_url())

class CategoryEditView(UpdateView):
    model = Category
    fields = ('name', )
    template_name = 'core/products/category-edit.html'
    success_url = reverse_lazy('core:categories')

    def form_valid(self, form):
        super(CategoryEditView, self).form_valid(form)
        message = f'La categoría {self.object.name} fue actualizada exitosamente!'
        messages.add_message(self.request, messages.SUCCESS, message)
        return HttpResponseRedirect(self.get_success_url())

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
            message = f'La categoria "{category.name}" fue desactivada exitosamente!'
            messages.add_message(self.request, messages.SUCCESS, message)
        
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
            message = f'La categoria "{category.name}" fue activada exitosamente!'
            messages.add_message(self.request, messages.SUCCESS, message)
        
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
                self.object.cost = self.object.get_cost()
                self.object.save()
                message = f'El producto {self.object.name} fue creado exitosamente!'
                messages.add_message(self.request, messages.SUCCESS, message)
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
                self.object.cost = self.object.get_cost()
                self.object.save()
                message = f'El producto {self.object.name} fue actualizado exitosamente!'
                messages.add_message(self.request, messages.SUCCESS, message)
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
            message = f'El producto {product.name} fue desactivado exitosamente!'
            messages.add_message(self.request, messages.SUCCESS, message)
        
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
            message = f'El producto {product.name} fue activado exitosamente!'
            messages.add_message(self.request, messages.SUCCESS, message)
        
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

    def form_valid(self, form):
        super(SupplierCreateView, self).form_valid(form)
        message = f'El proveedor {self.object.name} fue creado exitosamente!'
        messages.add_message(self.request, messages.SUCCESS, message)
        return HttpResponseRedirect(self.get_success_url())


class SupplierEditView(UpdateView):
    model = Supplier
    fields = ('name', 'phone', 'address', )
    template_name = 'core/suppliers/supplier-edit.html'
    success_url = reverse_lazy('core:suppliers')

    def form_valid(self, form):
        super(SupplierEditView, self).form_valid(form)
        message = f'El proveedor {self.object.name} fue actualizado exitosamente!'
        messages.add_message(self.request, messages.SUCCESS, message)
        return HttpResponseRedirect(self.get_success_url())


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
            message = f'El proveedor {supplier.name} fue desactivado exitosamente!'
            messages.add_message(self.request, messages.SUCCESS, message)
        
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
            message = f'El proveedor {supplier.name} fue activado exitosamente!'
            messages.add_message(self.request, messages.SUCCESS, message)
        
        return HttpResponseRedirect(reverse('core:suppliers'))


# PURCHASES
class PurchaseView(ListView):
    model = Purchase
    template_name = 'core/suppliers/purchases.html'


class PurchaseDetailView(DetailView):
    model = Purchase
    template_name = 'core/suppliers/purchase-detail.html'
    success_url = reverse_lazy('core:suppliers')


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

                date = self.object.created_at.strftime("%d-%m-%Y")
                message = f'Compra Creada Exitosamente el {date}!'
                messages.add_message(self.request, messages.SUCCESS, message)

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
        item = self.object
        items = self.object.get_items.all()

        for it in items:
            quantity = it.quantity
            it.item.decrease_inventory(quantity)

        message = f'Compra #{item.id} eliminada!'
        messages.add_message(self.request, messages.SUCCESS, message)

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

                saved_products = []

                for sale_item in products:
                    sale_item.subtotal = sale_item.get_subtotal()
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
                    # save the item
                    saved_products.append(sale_item.save())

                if len(saved_products) <= 0:
                    message = f'Debes añadir algún producto'
                    messages.add_message(self.request, messages.ERROR, message)
                    self.object.delete()
                    return self.render_to_response(self.get_context_data(form=form))


                self.object.total = self.object.get_sale_total()
                self.object.save()
                self.object.customer.increase_points(total_quantity)

                date = self.object.created_at.strftime("%d-%m-%Y")
                message = f'Venta Creada Exitosamente el {date}!'
                messages.add_message(self.request, messages.SUCCESS, message)

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
                self.object = form.save()
                # check if a form has changed
                delete_fields = []
                for f in formset:
                    if f.has_changed():
                        sale_item = f.cleaned_data['id']
                        self.object.reset_stock(sale_item)

                    delete_fields.append(f.cleaned_data['DELETE'])
                # if all delete fields are true we delete the sale
                if all(delete_fields):
                    object_id = self.object.id
                    self.object.delete()
                    message = f'Venta #{object_id} eliminada!'
                    messages.add_message(self.request, messages.SUCCESS, message)
                    return HttpResponseRedirect(self.get_success_url())

                # self.object = form.save()
                formset.instance = self.object

                # get all products from formset
                products = formset.save(commit=False)


                for sale_item in products:
                    sale_item.subtotal = sale_item.get_subtotal()
                    sale_quantity = sale_item.quantity
                    for product_item in sale_item.product.get_items.all():
                        product_quantity = product_item.quantity
                        total_quantity = sale_quantity * product_quantity
                        ok = product_item.item.decrease_inventory(total_quantity)
                        if not ok:
                            message = f'El Stock no alcanza: hay ({product_item.item.inventory}) {product_item.item.name} disponibles'
                            messages.add_message(self.request, messages.ERROR, message)
                            return self.render_to_response(self.get_context_data(form=form))
                    # save item
                    sale_item.save()
                
                ok = formset.save()

                self.object.total = self.object.get_sale_total()
                self.object.save()

                message = f'Venta #{self.object.id} actualizada!'
                messages.add_message(self.request, messages.SUCCESS, message)

                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('core:sales')


class SaleDetailView(DetailView):
    model = Sale
    template_name = 'core/sales/sale-detail.html'
    success_url = reverse_lazy('core:sales')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_quantities'] = self.object.calculate_products_quantities()
        return context


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

        message = f'Venta #{self.object.id} eliminada!'
        messages.add_message(self.request, messages.SUCCESS, message)

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

    def form_valid(self, form):
        super(CustomerCreateView, self).form_valid(form)
        message = f'{self.object.first_name} {self.object.last_name} fue creado exitosamente!'
        messages.add_message(self.request, messages.SUCCESS, message)
        return HttpResponseRedirect(self.get_success_url())


class CustomerEditView(UpdateView):
    model = Customer
    fields = ('first_name', 'last_name', 'address', )
    template_name = 'core/customers/customer-edit.html'
    success_url = reverse_lazy('core:customers')

    def form_valid(self, form):
        super(CustomerEditView, self).form_valid(form)
        message = f'{self.object.first_name} {self.object.last_name} fue actualizado exitosamente!'
        messages.add_message(self.request, messages.SUCCESS, message)
        return HttpResponseRedirect(self.get_success_url())


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

            message = f'{customer.first_name} {customer.last_name} fue desactivado exitosamente!'
            messages.add_message(self.request, messages.SUCCESS, message)
        
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

            message = f'{customer.first_name} {customer.last_name} fue activado exitosamente!'
            messages.add_message(self.request, messages.SUCCESS, message)
        
        return HttpResponseRedirect(reverse('core:customers'))


# API DATA FOR CHARTS
def get_most_sold_products(request):

    sale_items = SaleItem.objects.all().select_related('product', 'sale')

    most_sold_products= sale_items.values('product__name').annotate(total_sales=Coalesce(Sum('quantity'), Value(0))).order_by('-total_sales')


    labels = [item['product__name'] for item in most_sold_products]
    data = [item['total_sales'] for item in most_sold_products]
    backgroundColor = ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de', '#2D5DEB', '#3c8dbc', '#d2d6de', '#2D5DEB','#d2d6de', '#2D5DEB', '#3c8dbc', '#d2d6de', '#2D5DEB']
    donutData = {
        'labels': labels,
        'datasets': [
            {
                'data': data
            },
        ],
        'backgroundColor': backgroundColor
    }

    return JsonResponse(donutData)


class Report(FormView):
    template_name = 'core/reports/sales-report.html'
    form_class = ReportForm

    def form_valid(self, form):
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        start_year = start_date.year
        # start_month = format(start_date, 'm')
        start_month = start_date.month
        # start_day = format(start_date, 'd')
        start_day = start_date.day

        end_year = end_date.year
        # end_month = format(end_date, 'm')
        end_month = end_date.month
        # end_day = format(end_date, 'd')
        end_day = end_date.day

        return redirect('core:report_details', start_year, start_month, start_day, end_year, end_month, end_day)


class ReportDetails(View):
    
    def get(self, request, start_year, start_month, start_day, end_year, end_month, end_day):
        template = get_template('core/reports/sales-report-pdf.html')

        sales = Sale.objects.all()


        from_date = datetime.date(start_year, start_month, start_day)
        to_date = datetime.date(end_year, end_month, end_day)


        if query_is_valid(from_date) and query_is_valid(to_date):
            sales = Sale.objects.all().filter(created_at__date__range=(from_date, to_date))

        
        total_cost = 0
        for sale in sales:
            total_cost += sale.get_cost_sale()

        total_incomes = sales.aggregate(sales=Coalesce(Sum('total'), Value(0)))['sales']

        items_sold_total = 0
        combos_sold_total = 0
        for sale in sales:
            items_sold_total += sale.get_items_quantity()
            combos_sold_total += sale.get_combos_sale_quantity()

        context = {
            'from_date': from_date,
            'to_date': to_date,
            'total_cost': total_cost,
            'total_incomes': total_incomes,
            'revenue': total_incomes - total_cost,
            'products_sold_total': sales.annotate(quantity=Sum('get_products__quantity')).aggregate(quantities=Coalesce(Sum('quantity'), Value(0)))['quantities'],
            'items_sold_total': items_sold_total,
            'combos_sold_total': combos_sold_total,
            'sales': sales.order_by('created_at')
        }

        html = template.render(context)

        pdf = render_to_pdf('core/reports/sales-report-pdf.html', context)
        
        return HttpResponse(pdf, content_type='application/pdf')

# ACCOUNTS
class UserView(ListView):
    model = User
    template_name = 'core/users/employees.html'
