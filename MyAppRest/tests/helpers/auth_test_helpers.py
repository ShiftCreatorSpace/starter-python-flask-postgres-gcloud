def login(client, email='sponge@bob.com', password='password'):
    data = {
        'email': email,
        'password': password
    }

    response = client.post('/api/v1/login', data=data)

    return {'Authorization': f'Bearer {response.json["token"]}'}