from django.test import TestCase

from core.models import (
    Category,
    Item,
    Product
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


class ProductActiveManagerTestCase(TestCase):

    def setUp(self):
        combo = Category.objects.create(name='Combo')
        Product.objects.create(name='combo 1', price=1.0, cost=1.0, category=combo)
        Product.objects.create(name='combo 2', price=1.0, cost=1.0, category=combo)
        Product.objects.create(name='combo 3', price=1.0, cost=1.0, is_active=False, category=combo)

    def test_get_queryset(self):
        active_products = Product.active_products.all()
        self.assertEqual(len(active_products), 2)

