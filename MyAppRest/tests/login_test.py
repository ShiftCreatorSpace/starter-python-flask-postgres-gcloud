from MyAppRest.tests.base_test import BaseTest


class TestLogin(BaseTest):
    def test_invalid_credentials(self):
        data = {
            'email': 'sponge@bob.com',
            'password': 'wrongpassword'
        }

        response = self.client().post('/api/v1/login', data=data)
        self.assertEqual(400, response.status_code)

    def test_valid_credentials(self):
        data = {
            'email': 'sponge@bob.com',
            'password': 'password'
        }

        response = self.client().post('/api/v1/login', data=data)
        self.assertEqual(200, response.status_code)

        self.assertIsNotNone(response.json['token'])

    def test_invalid_token(self):
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNTkyNDQ0MDI0fQ.rV-5glmBa8ABu4ag3E9NUqJcnpN1__DYJga-S95RGiM'

        users_response = self.client().get('/api/v1/users', headers={
            'Authorization': f'Bearer {token}'
        })

        self.assertEqual(401, users_response.status_code)

    def test_valid_token(self):
        data = {
            'email': 'sponge@bob.com',
            'password': 'password'
        }

        response = self.client().post('/api/v1/login', data=data)
        self.assertEqual(200, response.status_code)

        self.assertIsNotNone(response.json['token'])

        users_response = self.client().get('/api/v1/users', headers={
            'Authorization': f'Bearer {response.json["token"]}'
        })

        self.assertEqual(1, len(users_response.json['users']))
        self.assertEqual(users_response.json['users'][0]['email'], data['email'])

    def test_token_expired(self):
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjExMTExMTExLTExMTEtMTExMS0xMTExLTExMTExMTExMTExMSIsImV4cCI6MTA5ODMyNzI5MH0.5z1gaUak4mmUCr-b0pxXgCvjFPQXvEiIJK8bVxSzZK4'
        users_response = self.client().get('/api/v1/users', headers={
            'Authorization': f'Bearer {token}'
        })

        self.assertEqual(401, users_response.status_code)