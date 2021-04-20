from sqlalchemy import and_

from MyAppRest.tests.helpers.foodie_session_test_helpers import test_helper_create_foodie_session
from common.models import db, RestaurantDeliveryOrderDao, RestaurantOrderDao


def test_helper_delete_order(restaurant_delivery_order_id):
    db.session.query(RestaurantOrderDao).filter(RestaurantOrderDao.id == restaurant_delivery_order_id).delete(synchronize_session='fetch')
    # db.session.query(RestaurantDeliveryOrderDao).filter(
    #     and_(RestaurantDeliveryOrderDao.id == restaurant_delivery_order_id)).delete(synchronize_session='fetch')
    db.session.commit()


def test_helper_create_order(client, restaurant_bill_id='11111111-1111-1111-1111-111111111111',
                             restaurant_id='11111111-1111-1111-1111-111111111111',
                             restaurant_menu_id='11111111-1111-1111-1111-111111111111', headers=None):
    data = {
        'restaurant_bill_id': restaurant_bill_id,
        'restaurant_menu_id': restaurant_menu_id,
    }
    session = headers or test_helper_create_foodie_session(client)

    return client.post(f'/api/v1/restaurants/{restaurant_id}/bills/{restaurant_bill_id}/delivery_orders', data=data,
                       headers=session)
