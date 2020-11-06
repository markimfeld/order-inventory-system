from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum

User = get_user_model()


# Create your models here.
class Category(models.Model): 
    name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=120, blank=True, null=True)
    inventory = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(upload_to='media/products/', default='empty.png')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def has_inventory(self, quantity):
        return self.inventory >= quantity

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def increase_inventory(self, quantity):
        if type(quantity) !=  int:
            raise Exception("Tipo de dato incorrecto")
        self.inventory += quantity
        self.save()

    def decrease_inventory(self, quantity):
        if type(quantity) != int:
            raise Exception("Tipo de dato incorrecto")
        if not self.has_inventory(quantity):
            return False

        self.inventory -= quantity
        item = self.save()
        
        return True


class ProductActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class ProductWithInventoryManager(models.Manager):
    def get_queryset(self):
        products_in_stock = []
        for p in Product.active_products.all():
            if p.has_stock():
                products_in_stock.append((p.pk, p.name))

        qs = [p for p in products_in_stock]

        return qs


class Product(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='media/products/', default='empty.png')
    description = models.CharField(max_length=120, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    items = models.ManyToManyField(Item, through='ProductItem')

    objects = models.Manager()
    active_products = ProductActiveManager()
    products_with_inventory = ProductWithInventoryManager()


    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:product-detail', args=[self.id])

    def __str__(self):
        return self.name

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def has_stock(self):
        items = self.get_items.all()

        # check if every item has inventory to sell
        every_has_stock = [p_item.item.has_inventory(p_item.quantity) for p_item in items]
        # check if every is true 
        return all(every_has_stock)


class ProductItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='get_items')
    quantity = models.PositiveSmallIntegerField(default=1)
    description = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.item.name


# LOOK UPS
class Status(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'Statuses'

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=64)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Provinces'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=64)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Address(models.Model):
    number = models.PositiveSmallIntegerField()
    street = models.CharField(max_length=120)
    neightborhood = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=10)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Addresses'

    @property
    def full_address(self):
        return f'{self.street} Nº{self.number} {self.neightborhood}'

    def __str__(self):
        return f'{self.street} Nº{self.number} ({self.postal_code})'


# SUPPLIERS
class Supplier(models.Model):
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.name


class Purchase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    items = models.ManyToManyField(Item, through='PurchaseItem')
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    purchased_at = models.DateTimeField()

    def calculate_total(self):
        total = self.get_items.aggregate(total=Sum('subtotal'))
        self.total = total['total']
        self.save()

    def __str__(self):
        return f'Compra #{self.id} realizada el {self.created_at}'


class PurchaseItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='get_items')
    unit_cost = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=1)
    description = models.CharField(max_length=120, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def calculate_subtotal(self):
        self.subtotal = self.unit_cost * self.quantity
        self.save()

    def __str__(self):
        return self.item.name


# CUSTOMER
class Customer(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    points = models.IntegerField(default=0)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def increase_points(self, quantity):
        if quantity < 5:
            self.points += 1
        elif quantity < 10:
            self.points += 5
        elif quantity < 20:
            self.points += 7
        else:
            self.points += 10

        self.save()

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save()

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save()

    @property
    def full_name(self):
        "Return the customer's full name."
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# SALES
class Sale(models.Model):
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    products = models.ManyToManyField(Product, through='SaleItem')

    def calculate_total(self):
        total = self.get_products.aggregate(total=Sum('subtotal'))
        self.total = total['total']
        self.save()

    def reset_stock(self):
        for sale_item in self.get_products.all():
            sale_quantity = sale_item.quantity
            for product_item in sale_item.product.get_items.all():
                product_quantity = product_item.quantity
                total_quantity = sale_quantity * product_quantity
                product_item.item.increase_inventory(total_quantity)
        

    def __str__(self):
        return f'Venta #{self.id}'


class SaleItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='get_products')
    quantity = models.PositiveSmallIntegerField(default=1)
    description = models.CharField(max_length=120, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def calculate_subtotal(self):
        self.subtotal = self.product.price * self.quantity
        self.save()

    def __str__(self):
        return self.product.name
