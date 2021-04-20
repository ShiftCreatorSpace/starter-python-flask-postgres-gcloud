from sqlalchemy import and_

from MyAppRest.tests.helpers.foodie_session_test_helpers import TEST_FOODIE_SESSION
from common.models import db, RestaurantOrderLineItemDao


def test_helper_delete_order_line_item(restaurant_order_line_item_id):
    db.session.query(RestaurantOrderLineItemDao).filter(
        and_(RestaurantOrderLineItemDao.id == restaurant_order_line_item_id)).delete(synchronize_session='fetch')
    db.session.commit()


def test_helper_create_order_line_item(client, restaurant_bill_id='11111111-1111-1111-1111-111111111111',
                                       restaurant_menu_id='11111111-1111-1111-1111-111111111111',
                                      restaurant_order_id='1a1a1010101010101010101010101010', headers=None):
    data = {
        'restaurant_item_id': restaurant_menu_id,
        'price': 5.99,
        'quantity': 1,
        'comment': 'no food please',
        'modifiers': '[{"id": "11111111111111111111111111111111", "options": [{"id": "22222222222222222222222222222222"}]}]'
    }

    session = headers or TEST_FOODIE_SESSION

    return client.post(
        f'/api/v1/restaurants/11111111-1111-1111-1111-111111111111/bills/{restaurant_bill_id}/orders'
        f'/{restaurant_order_id}/items',
        headers=session,
        data=data)
