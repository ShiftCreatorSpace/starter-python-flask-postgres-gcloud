from uuid import UUID

from MyAppRest.tests.base_test import KRUSTY_KRABS_RESTAURANT_ID
from MyAppRest.tests.helpers.foodie_session_test_helpers import test_helper_create_foodie_session
from common.models import db, RestaurantBillDao, RestaurantDao


def test_helper_delete_bill(restaurant_bill_id, restaurant_id=KRUSTY_KRABS_RESTAURANT_ID):
    restaurant = RestaurantDao.get_by_id(UUID(restaurant_id))
    bill = RestaurantBillDao.get_by_id_and_restaurant(restaurant_bill_id, restaurant)

    db.session.delete(bill)
    db.session.commit()


def test_helper_create_bill(client, table_id='22222222-2222-2222-2222-222222222222',
                            restaurant_id='11111111-1111-1111-1111-111111111111',
                            foodie_session=None):
    create_data = {
        'restaurant_table_id': table_id
    }

    session = foodie_session or test_helper_create_foodie_session(client)

    return client.post(f'/api/v1/restaurants/{restaurant_id}/bills', data=create_data, headers=session)
