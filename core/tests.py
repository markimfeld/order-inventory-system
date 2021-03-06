import datetime

from django.test import (
    TestCase,
    Client,
)

from core.models import (
    Category,
    Item,
    Product,
    ProductItem,
    Status,
    Country,
    Province,
    City,
    ProductItem,
    Supplier,
    Purchase,
    PurchaseItem,
    Customer,
    Sale,
    SaleItem
)
# Create your tests here.

class CategoryTestCase(TestCase):

    def setUp(self):
        Category.objects.create(name='Individual')

    def test_category_activate(self):
        category_one = Category.objects.get(name='Individual')
        category_one.is_active = False
        category_one.save()
        category_one.activate()
        self.assertEqual(category_one.is_active, True)

    def test_category_deactivate(self):
        category_one = Category.objects.get(name='Individual')
        category_one.deactivate()
        self.assertEqual(category_one.is_active, False)

    def test_category_str(self):
        name = Category.objects.get(name='Individual')
        self.assertEqual(str(name), 'Individual')

    def test_category_name_has_correct_max_length(self):
        """category with correct max_length are valid"""
        self.assertEqual(Category._meta.get_field('name').max_length, 64)

    def test_category_is_active_by_default(self):
        """category with is_active true as defualt is valid"""
        self.assertEqual(Category._meta.get_field('is_active').default, True)


class ItemTestCase(TestCase):

    def setUp(self):
        Item.objects.create(name='ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd', cost=0.0)
        Item.objects.create(name='criolla', cost=21.0, inventory=5)
        Item.objects.create(name='activate', cost=1.0)
        Item.objects.create(name='deactivate', cost=1.0)

    def test_item_increase_inventory(self):
        criolla = Item.objects.get(name='criolla')
        quantity = 5
        criolla.increase_inventory(quantity)
        self.assertEqual(criolla.inventory, 10)

    def test_item_increase_inventory_quantity_is_int(self):
        criolla = Item.objects.get(name='criolla')
        quantity = '3'
        with self.assertRaises(Exception, msg='Tipo de dato incorrecto'):
            criolla.increase_inventory(quantity)

    def test_item_decrease_inventory(self):
        criolla = Item.objects.get(name='criolla')
        quantity = 2
        criolla.decrease_inventory(quantity)
        self.assertEqual(criolla.inventory, 3)

    def test_item_decrease_inventory_with_quantity_lower_to_inventory(self):
        criolla = Item.objects.get(name='criolla')
        quantity = 6
        self.assertFalse(criolla.decrease_inventory(quantity))

    def test_item_decrease_inventory_quantity_is_int(self):
        criolla = Item.objects.get(name='criolla')
        quantity = '3'
        with self.assertRaises(Exception, msg='Tipo de dato incorrecto'):
            criolla.decrease_inventory(quantity)

    def test_item_has_inventory_quantity_is_int(self):
        criolla = Item.objects.get(name='criolla')
        quantity = '3'
        with self.assertRaises(Exception, msg='Tipo de dato incorrecto'):
            criolla.has_inventory(quantity)

    def test_item_has_inventory(self):
        criolla = Item.objects.get(name='criolla')
        quantity = 3 
        self.assertTrue(criolla.has_inventory(quantity))

    def test_item_has_no_inventory(self):
        criolla = Item.objects.get(name='criolla')
        quantity = 10
        self.assertFalse(criolla.has_inventory(quantity))

    def test_item_activate(self):
        item = Item.objects.get(name='deactivate')
        item.activate()
        self.assertEqual(item.is_active, True)

    def test_item_deactivate(self):
        item = Item.objects.get(name='activate')
        item.deactivate()
        self.assertEqual(item.is_active, False)

    def test_category_str(self):
        name = Item.objects.get(name='criolla')
        self.assertEqual(str(name), 'criolla')
    
    def test_item_name_has_correct_max_length(self):
        """item with correct max_length is valid"""
        self.assertEqual(Item._meta.get_field('name').max_length, 64)

    def test_item_is_active_True_by_default(self):
        self.assertTrue(Item._meta.get_field('is_active').default, True)


class ProductManagerTestCase(TestCase):

    def setUp(self):
        criolla = Item.objects.create(name='criolla', cost=21.0)
        pascualina = Item.objects.create(name='pascualina', cost=34.40)
        raviol = Item.objects.create(name='raviol', cost=54.50)
        fideo = Item.objects.create(name='fideo', cost=34.40)

        combo = Category.objects.create(name='Combo')
        combo1 = Product.objects.create(name='combo 1', price=1.0, cost=1.0, category=combo)
        combo1.items.add(criolla, criolla, raviol)
        combo2 = Product.objects.create(name='combo 2', price=1.0, cost=1.0, category=combo)
        combo2.items.add(pascualina, criolla, criolla, criolla)
        combo3 = Product.objects.create(name='combo 3', price=1.0, cost=1.0, is_active=False, category=combo)
        combo3.items.add(fideo, fideo, criolla)

    def test_get_queryset_active_manager(self):
        active_products = Product.active_products.all()
        self.assertEqual(len(active_products), 2)

class ProductTestCase(TestCase):
    
    def setUp(self):
        criolla = Item.objects.create(name='criolla', cost=21.0)
        raviol = Item.objects.create(name='raviol', cost=54.50)

        combo = Category.objects.create(name='Combo')
        combo1 = Product.objects.create(name='combo 1', price=150.0, cost=96.5, category=combo)
        combo2 = Product.objects.create(name='combo 2', price=150.0, cost=96.5, category=combo, is_active=False)
        produc_item1 = ProductItem.objects.create(item=criolla, product=combo1, quantity=2)
        produc_item2 = ProductItem.objects.create(item=raviol, product=combo1, quantity=1)


    def test_get_revenue(self):
        combo1 = Product.objects.get(name='combo 1')
        self.assertEqual(combo1.get_revenue(), 53.5)

    def test_get_cost(self):
        combo1 = Product.objects.get(name='combo 1')
        self.assertEqual(combo1.get_cost(), 96.5)

    def test_get_items_detail(self):
        combo1 = Product.objects.get(name='combo 1')
        items = [('criolla', 2), ('raviol', 1)]
        
        self.assertEqual(combo1.get_items_detail(), items)

    def test_get_absolute_url(self):
        combo1 = Product.objects.get(name='combo 1')
        path = f'/products/detail/{combo1.pk}/'
        self.assertEqual(combo1.get_absolute_url(), path)

    def test_product_str(self):
        combo1 = Product.objects.get(name='combo 1')
        self.assertEqual(str(combo1), 'combo 1')

    def test_product_activate(self):
        combo2 = Product.objects.get(name='combo 2')
        combo2.activate()
        self.assertTrue(combo2.is_active)

    def test_product_deactivate(self):
        combo1 = Product.objects.get(name='combo 1')
        combo1.deactivate()
        self.assertFalse(combo1.is_active)

    def test_has_stock(self):
        combo1 = Product.objects.get(name='combo 1')
        
        self.assertFalse(combo1.has_stock())

    def test_has_no_stock(self):
        combo1 = Product.objects.get(name='combo 1')
        raviol = Item.objects.get(name='raviol')
        raviol.increase_inventory(10)
        criolla = Item.objects.get(name='criolla')
        criolla.increase_inventory(10)
        self.assertTrue(combo1.has_stock())


class StatusTestCase(TestCase):

    def setUp(self):
        Status.objects.create(name='Preparar')
    
    def test_status_str(self):
        status = Status.objects.get(name='Preparar')
        self.assertEqual(str(status), 'Preparar')
    

class CountryTestCase(TestCase):

    def setUp(self):
        Country.objects.create(name='Argentina')
    
    def test_country_str(self):
        country = Country.objects.get(name='Argentina')
        self.assertEqual(str(country), 'Argentina')


class ProvinceTestCase(TestCase):

    def setUp(self):
        country = Country.objects.create(name='Argentina')
        Province.objects.create(name='Chaco', country=country)
    
    def test_province_str(self):
        province = Province.objects.get(name='Chaco')
        self.assertEqual(str(province), 'Chaco')


class CityTestCase(TestCase):

    def setUp(self):
        country = Country.objects.create(name='Argentina')
        province = Province.objects.create(name='Chaco', country=country)
        City.objects.create(name='Machagai', province=province)

    def test_city_str(self):
        province = Province.objects.get(name='Chaco')
        city = City.objects.get(name='Machagai')
        self.assertEqual(str(city), 'Machagai')


class SupplierTestCase(TestCase):

    def setUp(self):
        Supplier.objects.create(name='NONO', is_active=False)
        Supplier.objects.create(name='Bochi')
        
    def test_supplier_activate(self):
        supplier = Supplier.objects.get(name='NONO')
        supplier.activate()
        self.assertTrue(supplier.is_active)
    
    def test_supplier_deactivate(self):
        supplier = Supplier.objects.get(name='Bochi')
        supplier.deactivate()
        self.assertFalse(supplier.is_active)

    def test_supplier_str(self):
        supplier = Supplier.objects.get(name='NONO')
        self.assertEqual(str(supplier), 'NONO')


class PurchaseTestCase(TestCase):

    def setUp(self):
        supplier = Supplier.objects.create(name='NONO')
        purchase = Purchase.objects.create(supplier=supplier)
        item1 = Item.objects.create(name='criolla', cost=21.00)
        item2 = Item.objects.create(name='pascualina', cost=34.40)
        purchase_item1 = PurchaseItem.objects.create(item=item1, purchase=purchase, quantity=30, subtotal=630)
        purchase_item2 = PurchaseItem.objects.create(item=item2, purchase=purchase, quantity=20, subtotal=688)
    

    def test_purchase_calculate_total(self):
        purchase = Purchase.objects.all().first()
        purchase.calculate_total()
        self.assertEqual(purchase.total, 1318)
    

class PurchaseItemTestCase(TestCase):


    def setUp(self):
        supplier = Supplier.objects.create(name='NONO')
        purchase = Purchase.objects.create(supplier=supplier)
        item1 = Item.objects.create(name='criolla', cost=21.00)
        purchase_item1 = PurchaseItem.objects.create(description='purchase1', item=item1, purchase=purchase, quantity=30)
    
    def test_purchaseitem_calculate_total(self):
        purchase_item = PurchaseItem.objects.get(description='purchase1')
        purchase_item.calculate_subtotal()
        self.assertEqual(purchase_item.subtotal, 630)


class CustomerTestCase(TestCase):

    def setUp(self):
        Customer.objects.create(first_name='Marcos', last_name='Imfeld', is_active=False)
        Customer.objects.create(first_name='Luz', last_name='Imfeld')
    
    def test_customer_activate(self):
        customer = Customer.objects.get(first_name='Marcos')
        customer.activate()
        self.assertTrue(customer.is_active)

    def test_customer_deactivate(self):
        customer = Customer.objects.get(first_name='Luz')
        customer.deactivate()
        self.assertFalse(customer.is_active)
    
    def test_customer_str(self):
        customer = Customer.objects.get(first_name='Luz')
        self.assertEqual(str(customer), 'Luz Imfeld')

    def test_customer_full_name(self):
        customer = Customer.objects.get(first_name='Luz')
        self.assertEqual(str(customer.full_name), 'Luz Imfeld')


class SaleTestCase(TestCase):


    def setUp(self):
        status = Status.objects.create(name='Preparar')
        customer = Customer.objects.create(first_name='Marcos', last_name='Imfeld')
        sale = Sale.objects.create(status=status, customer=customer)
        criolla = Item.objects.create(name='criolla', cost=21.0, inventory=10)
        pascualina = Item.objects.create(name='pascualina', cost=34.40, inventory=10)
        raviol = Item.objects.create(name='raviol', cost=54.50, inventory=10)
        category = Category.objects.create(name='combo')
        combo1 = Product.objects.create(name='combo 1', price=150, cost=96.5, category=category)
        combo2 = Product.objects.create(name='combo 2', price=150, cost=97.4, category=category)

        productitem1 = ProductItem.objects.create(item=criolla, product=combo1, quantity=2)
        productitem2 = ProductItem.objects.create(item=raviol, product=combo1, quantity=1)
        
        productitem3 = ProductItem.objects.create(item=criolla, product=combo2, quantity=3)
        productitem4 = ProductItem.objects.create(item=pascualina, product=combo2, quantity=1)

        saleitem1 = SaleItem.objects.create(product=combo1, sale=sale, quantity=2, subtotal=300)
        saleitem2 = SaleItem.objects.create(product=combo2, sale=sale, quantity=1, subtotal=150)
        saleitem3 = SaleItem.objects.create(product=combo2, sale=sale, quantity=3, subtotal=450)

    
    def test_sale_get_cost_sale(self):
        sale = Sale.objects.get(status__name__exact='Preparar')

        sale_cost = sale.get_cost_sale()

        self.assertEqual(float(sale_cost), 582.60)