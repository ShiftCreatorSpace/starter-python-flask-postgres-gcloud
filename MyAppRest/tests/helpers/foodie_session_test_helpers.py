import random

def test_helper_create_foodie_session(client,
                                      restaurant_id='11111111-1111-1111-1111-111111111111',
                                      hash_val='fe01b8f7b5ecca6be7f0e95b110b6d4b',
                                      user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) '
                                                 'Gecko/20100101 Firefox/78.0'):
    data = {
        'hash': hash_val,
        'user_agent': user_agent,
        'restaurant_id': restaurant_id
    }

    response = client.post('/api/v1/foodie-sessions', data=data)

    return {'Authorization': f'Bearer {response.json["token"]}'}

def test_helper_create_verified_foodie_session(client, restaurant_id='22222222-2222-2222-2222-222222222222',
                                      hash_val='fe01b8f7b5ecca6be7f0e95b110b6d4b',
                                      user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) '
                                                 'Gecko/20100101 Firefox/78.0',
                                        phone_number='+16502231052'):
    random.seed(0)
    data = {
        'hash': hash_val,
        'user_agent': user_agent,
        'restaurant_id': restaurant_id
    }

    response = client.post('/api/v1/foodie-sessions', data=data)

    put_data = {
        'phone': phone_number
    }
    put_response = client.put('/api/v1/foodie-sessions', data=put_data,
                                     headers={'Authorization': f'Bearer {response.json["token"]}'})

    put_data = {
        'phone': phone_number,
        'code': '985440',
    }
    put_response = client.put('/api/v1/foodie-sessions', data=put_data,
                                     headers={'Authorization': f'Bearer {response.json["token"]}'})

    return {'Authorization': f'Bearer {response.json["token"]}'}

TEST_FOODIE_SESSION_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjhkYzcwZGQwZWY1YjQyYzRhZGZkMDc4YmI2YTJkMDMwIiwidHlwZSI6ImZvb2RpZV9zZXNzaW9uIn0.Zm2zbEe7N37R4CHDgPjAjLeOLUbX6nZn9pieCPkBZTU'
TEST_FOODIE_SESSION = {'Authorization': f'Bearer {TEST_FOODIE_SESSION_TOKEN}'}
