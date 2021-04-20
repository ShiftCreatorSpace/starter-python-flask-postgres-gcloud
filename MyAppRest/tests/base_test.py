import logging
import unittest
from datetime import datetime, timezone
from MyAppRest.tests.setup import reset, app, client
FROZEN_TIME = datetime(2020, 6, 16, 7, 19, 10, 1234, tzinfo=timezone.utc)
KRUSTY_KRABS_RESTAURANT_ID = '11111111-1111-1111-1111-111111111111'


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = client

        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    def reset_db(self):
        reset()

    def tearDown(self):
        pass

    def assertIsEvent(self, event, resolver_user=False):
        self.assertIsNotNone(event['id'])
        self.assertIsNotNone(event['request_type'])
        self.assertIsNotNone(event['created_date'])
        self.assertIsNotNone(event['entity_type'])
        self.assertTrue('restaurant_dine_in_order_frozen' in event or 'restaurant_bill_frozen' in event)

        if resolver_user:
            self.assertIsUser(event['resolver_user'], sensitive=False)

    def assertIsBill(self, bill, orders=True):
        self.assertIsNotNone(bill['id'])
        self.assertIsNotNone(bill['restaurant_table_id'])
        self.assertIsNotNone(bill['created_date'])

        if orders:
            self.assertIsNotNone(bill['orders'])

            for order in bill['orders']:
                self.assertIsOrder(order)

    def assertIsMenu(self, menu, categories=True):
        self.assertIsNotNone(menu['id'])
        self.assertIsNotNone(menu['created_date'])
        self.assertIsNotNone(menu['name'])
        self.assertIsNotNone(menu['restaurant_id'])

        if categories:
            for category in menu['categories']:
                self.assertIsMenuCategory(category)

    def assertIsMenuCategory(self, category, items=True):
        self.assertIsNotNone(category['id'])
        self.assertIsNotNone(category['name'])

        if items:
            self.assertIsNotNone(category['items'])
            for item in category['items']:
                self.assertIsRestaurantItem(item, modifiers=False, tags=False)

    def assertIsRestaurantItem(self, item, modifiers=True, tags=True):
        self.assertIsNotNone(item['id'])
        self.assertIsNotNone(item['created_date'])
        self.assertIsNotNone(item['name'])
        self.assertIsNotNone(item['price'])
        self.assertIsNotNone(item['featured'])
        self.assertIsNotNone(item['available'])

        if modifiers:
            self.assertIsNotNone(item['modifiers'])

            for modifier in item['modifiers']:
                self.assertIsItemModifier(modifier)

        if tags:
            self.assertIsNotNone(item['tags'])

            for tag in item['tags']:
                self.assertIsMenuTag(tag)

    def assertIsRestaurantItemCategory(self, restaurant_item_category):
        self.assertIsNotNone(restaurant_item_category['menu_category'])
        self.assertIsMenuCategory(restaurant_item_category['menu_category'], items=False)

    def assertIsMenuCategoryItem(self, restaurant_item_category):
        self.assertIsNotNone(restaurant_item_category['restaurant_item'])
        self.assertIsRestaurantItem(restaurant_item_category['restaurant_item'], modifiers=False, tags=True)
        self.assertIsNotNone(restaurant_item_category['position'])

    def assertIsMenuItemTag(self, restaurant_item_tag):
        self.assertIsMenuTag(restaurant_item_tag['tag'])
        self.assertIsNotNone(restaurant_item_tag['position'])

    def assertIsMenuTagItem(self, menu_tag_item):
        self.assertIsRestaurantItem(menu_tag_item['restaurant_item'], modifiers=False, tags=True)

    def assertIsMenuItemModifier(self, restaurant_item_modifier):
        self.assertIsItemModifier(restaurant_item_modifier['item_modifier'], required=False)
        self.assertIsNotNone(restaurant_item_modifier['position'])
        self.assertIsNotNone(restaurant_item_modifier['required'])

    def assertIsMenuModifierItem(self, menu_modifier_item):
        self.assertIsRestaurantItem(menu_modifier_item['restaurant_item'], modifiers=False, tags=False)
        self.assertIsNotNone(menu_modifier_item['required'])

    def assertIsItemModifier(self, modifier, required=True):
        self.assertIsNotNone(modifier['id'])
        self.assertIsNotNone(modifier['name'])
        self.assertIsNotNone(modifier['type'])
        self.assertIn(modifier['type'], ['single', 'multi'])
        self.assertIsNotNone(modifier['available'])

        if required:
            self.assertIsNotNone(modifier['required'])

        self.assertIsNotNone(modifier['options'])

        for option in modifier['options']:
            self.assertIsItemModifierOption(option)

    def assertIsItemModifierOption(self, option):
        self.assertIsNotNone(option['id'])
        self.assertIsNotNone(option['label'])
        self.assertIsNotNone(option['restaurant_item_modifier_id'])
        self.assertIsNotNone(option['price'])
        self.assertIsNotNone(option['available'])

    def assertIsOrder(self, order, line_items=True):
        self.assertIsNotNone(order['id'])
        self.assertIsNotNone(order['line_items'])
        self.assertIsNotNone(order['status'])
        self.assertIn(order['status'], ['created', 'ordered', 'resolved', 'expired'])
        self.assertIsNotNone(order['total_price'])
        self.assertIsNotNone(order['created_date'])

        if line_items:
            self.assertIsNotNone(order['line_items'])

            for line_item in order['line_items']:
                self.assertIsOrderLine(line_item)

    def assertIsOrderLine(self, line, restaurant_item=True):
        self.assertIsNotNone(line['id'])
        self.assertIsNotNone(line['price'])
        self.assertIsNotNone(line['quantity'])
        self.assertIsNotNone(line['comment'])
        self.assertIsNotNone(line['restaurant_order_id'])
        self.assertIsNotNone(line['modifiers'])

        for modifier in line['modifiers']:
            self.assertIsOrderLineItemModifier(modifier)

        if restaurant_item:
            self.assertIsNotNone(line['restaurant_item'])
            self.assertIsRestaurantItem(line['restaurant_item'], modifiers=False)

    def assertIsOrderLineItemModifier(self, line_item_modifier):
        self.assertIsNotNone(line_item_modifier['id'])
        self.assertIsNotNone(line_item_modifier['name'])
        self.assertIsNotNone(line_item_modifier['type'])
        self.assertIsNotNone(line_item_modifier['available'])

        for option in line_item_modifier['options']:
            self.assertIsOrderLineItemModifierOption(option)

    def assertIsOrderLineItemModifierOption(self, line_item_modifier_option):
        self.assertIsNotNone(line_item_modifier_option['label'])
        self.assertIsNotNone(line_item_modifier_option['price'])
        self.assertIsNotNone(line_item_modifier_option['id'])
        self.assertIsNotNone(line_item_modifier_option['available'])

    def assertIsRestaurant(self, resto):
        self.assertIsNotNone(resto['id'])
        self.assertIsNotNone(resto['created_date'])
        self.assertIsNotNone(resto['name'])
        self.assertIsNotNone(resto['address'])
        self.assertIsNotNone(resto['handle'])
        self.assertIsNotNone(resto['code'])
        self.assertIsNotNone(resto['ga_code'])

    def assertIsTable(self, table):
        self.assertIsNotNone(table['id'])
        self.assertIsNotNone(table['restaurant_id'])
        self.assertIsNotNone(table['created_date'])
        self.assertIsNotNone(table['display_name'])

        self.assertIsNotNone(table['code'])
        self.assertEqual(4, len(table['code']))

    def assertIsMenuTag(self, tag):
        self.assertIsNotNone(tag['id'])
        self.assertIsNotNone(tag['name'])

    def assertIsUser(self, user, sensitive=False):
        self.assertIsNotNone(user['id'])
        self.assertIsNotNone(user['email'])
        self.assertIsNotNone(user['first_name'])
        self.assertIsNotNone(user['last_name'])
        self.assertIsNotNone(user['created_date'])

        if sensitive:
            pass

    def assertIsRestaurantUser(self, restaurant_user):
        self.assertIsUser(restaurant_user['user'])
        self.assertIsNotNone(restaurant_user['created_date'])

    def assertIsRestaurantUserInvitation(self, restaurant_user_invitation):
        self.assertIsNotNone(restaurant_user_invitation['id'])
        self.assertIsNotNone(restaurant_user_invitation['email'])
        self.assertIsNotNone(restaurant_user_invitation['role'])
        self.assertIsNotNone(restaurant_user_invitation['created_date'])

    def assertIsUserRestaurant(self, user_restaurant):
        self.assertIsUserRestaurantRestaurant(user_restaurant['restaurant'])
        self.assertIsNotNone(user_restaurant['created_date'])

    def assertIsUserRestaurantRestaurant(self, ur_restaurant):
        self.assertIsNotNone(ur_restaurant['id'])
        self.assertIsNotNone(ur_restaurant['name'])
