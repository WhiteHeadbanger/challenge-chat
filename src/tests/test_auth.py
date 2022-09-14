def test_register(client):
    username = 'test'
    url = f'/register?username={username}'
    
    mockup_response_success = {
        'success': True,
        'data': f"{username} registered."
    }

    mockup_response_failed = {
        'success': False,
        'data': f"{username} already exists."
    }
    with client:
        response = client.post(url)
        assert response.json == mockup_response_success
        
        response = client.post(url)
        assert response.json == mockup_response_failed

def test_login(client):
    username = 'test'
    url = f'/login?username={username}'
    url_other_user = f'/login?username=other_user'
    
    mockup_response_success = {
        'success': True,
        'data': f"{username} successfully logged in."
    }

    mockup_response_already_logged_in = {
        'success': False,
        'data': f"{username} is already logged in."
    }

    mockup_response_failed = {
        'success': False,
        'data': f"other_user does not exist."
    }
    with client:
        response = client.post(url)
        assert response.json == mockup_response_success

        response = client.post(url)
        assert response.json == mockup_response_already_logged_in

        response = client.post(url_other_user)
        assert response.json == mockup_response_failed

def test_logout(client, auth):
    url = f'/logout'

    mockup_response_success = {
        'success': True,
        'data': "Successfully logged out."
    }

    mockup_response_failed = {
        'success': False,
        'data': "You must first log in."
    }

    response = client.get(url)
    assert response.json == mockup_response_failed
    with client:
        # Force login
        username = 'test'
        _ = auth.login(username)

        response = client.get(url)
        assert response.json == mockup_response_success

def test_delete(client, auth):
    username = 'test'
    url = '/deleteaccount'
    mockup_response_success = {
        'success': True,
        'data': "Account deleted."
    }
    with client:
        # Force login
        _ = auth.login(username)
        
        response = client.delete(url)
        assert response.json == mockup_response_success
        







