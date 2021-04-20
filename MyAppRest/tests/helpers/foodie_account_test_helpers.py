import random
from .foodie_session_test_helpers import test_helper_create_verified_foodie_session

def test_helper_add_extra_info(client,
                                      first_name = "Bob", last_name = "Jones", email="BJ@chimemenu.com", foodie_session=None,
                               address='923 South State St, Ann Arbor, MI, USA', place_id='ChIJ3XqqM0iuPIgRHLNOdsDUGeY', birthate='1995-10-15'):
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'address': address,
        "place_id": place_id,
        'birthdate': birthate
    }

    session = foodie_session or test_helper_create_verified_foodie_session(client)

    response = client.put('/api/v1/foodie-accounts', data=data, headers=session)

    return response

TEST_FOODIE_SESSION_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjhkYzcwZGQwZWY1YjQyYzRhZGZkMDc4YmI2YTJkMDMwIiwidHlwZSI6ImZvb2RpZV9zZXNzaW9uIn0.Zm2zbEe7N37R4CHDgPjAjLeOLUbX6nZn9pieCPkBZTU'
TEST_FOODIE_SESSION = {'Authorization': f'Bearer {TEST_FOODIE_SESSION_TOKEN}'}
