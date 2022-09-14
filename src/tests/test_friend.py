def test_friend_request(client, auth):
    username = 'test'
    friend_username = 'friend_test'

    friend_request_url = f'/friendrequest/send?username={friend_username}'

    mockup_response_send = {
        'success': True,
        'data': f"Friend request sent to {friend_username}",
    }
    
    with client:
        # Register 'friend_test'
        register_url = f'/register?username={friend_username}'
        _ = client.post(register_url)
    
        # Register 'test'
        register_url = f'/register?username={username}'
        _ = client.post(register_url)
        
        # Login 'test'
        _ = auth.login(username)
        
        # Send friend request to 'friend_test'
        response = client.post(friend_request_url)
        assert response.json == mockup_response_send

def test_friend_request_user_not_exists(client, auth):
    username = 'test'
    not_found_user = 'not_found_test'

    friend_request_url = f'/friendrequest/send?username={not_found_user}'

    mockup_response_user_not_exists = {
        'success': False,
        'data': f"{not_found_user} not found.",
    }
    
    with client:
        # Register 'test'
        register_url = f'/register?username={username}'
        _ = client.post(register_url)
        
        # Login 'test'
        _ = auth.login(username)
        
        # Send friend request to 'not_found_test'
        response = client.post(friend_request_url)
        assert response.json == mockup_response_user_not_exists

def test_accept_friend_request(client, auth):
    username = 'test'
    friend_username = 'friend_test'

    friend_request_url = f'/friendrequest/send?username={friend_username}'
    friend_request_accept_url = f'/friendrequest/handle?username={username}&accept=true'

    mockup_response_accepted = {
        'success': True,
        'data': f"Accepted {username}'s friend request.",
    }
    
    with client:
        # Register 'friend_test'
        register_url = f'/register?username={friend_username}'
        _ = client.post(register_url)
    
        # Register 'test'
        register_url = f'/register?username={username}'
        _ = client.post(register_url)
        
        # Login 'test'
        _ = auth.login(username)
        
        # Send friend request to 'friend_test'
        _ = client.post(friend_request_url)
        
        # Logout 'test'
        _ = auth.logout()

        # Login 'friend_test'
        _ = auth.login(friend_username)

        # Accept friend request from 'test'
        response = client.post(friend_request_accept_url)
        assert response.json == mockup_response_accepted

def test_reject_friend_request(client, auth):
    username = 'test'
    friend_username = 'friend_test'

    friend_request_url = f'/friendrequest/send?username={friend_username}'
    friend_request_reject_url = f'/friendrequest/handle?username={username}&accept=false'

    mockup_response_rejected = {
        'success': True,
        'data': f"Denied {username}'s friend request",
    }
    
    with client:
        # Register 'friend_test'
        register_url = f'/register?username={friend_username}'
        _ = client.post(register_url)
    
        # Register 'test'
        register_url = f'/register?username={username}'
        _ = client.post(register_url)
        
        # Login 'test'
        _ = auth.login(username)
        
        # Send friend request to 'friend_test'
        _ = client.post(friend_request_url)
        
        # Logout 'test'
        _ = auth.logout()

        # Login 'friend_test'
        _ = auth.login(friend_username)

        # Reject friend request from 'test'
        response = client.post(friend_request_reject_url)
        assert response.json == mockup_response_rejected

def test_friend_delete_success(client, auth):
    username = 'test'
    friend_username = 'friend_test'

    friend_request_url = f'/friendrequest/send?username={friend_username}'
    friend_request_accept_url = f'/friendrequest/handle?username={username}&accept=true'
    friend_delete_url = f'/friend/delete?username={username}'
   

    mockup_response_success = {
        'success': True,
        'data': f"{username} removed from friend list."
    }

    with client:
        # Register 'test'
        register_url = f'/register?username={username}'
        _ = client.post(register_url)

        # Register 'friend_test'
        register_url = f'/register?username={friend_username}'
        _ = client.post(register_url)
        
        # Login 'test'
        _ = auth.login(username)
        
        # Send friend request to 'friend_test'
        _ = client.post(friend_request_url)
        
        # Logout 'test'
        _ = auth.logout()

        # Login 'friend_test'
        _ = auth.login(friend_username)

        # Accept friend request from 'test'
        _ = client.post(friend_request_accept_url)

        # Delete 'test' from 'friend_test' friendlist
        response = client.delete(friend_delete_url)
        assert response.json == mockup_response_success


def test_friend_delete_user_not_in_friendlist(client, auth):
    username = 'test'
    not_friend_username = 'not_friend_test'

    not_friend_delete_url = f'/friend/delete?username={not_friend_username}'

    mockup_response_user_not_in_friendlist = {
        'success': False,
        'data': f"{not_friend_username} is not your friend."
    }

    with client:
        # Register 'test'
        register_url = f'/register?username={username}'
        _ = client.post(register_url)
        
        # Register 'not_friend_test'
        register_url = f'/register?username={not_friend_username}'
        _ = client.post(register_url)
        
        # Login 'test'
        _ = auth.login(username)

        # Try to delete 'not_friend_test' from 'test' friendlist
        response = client.delete(not_friend_delete_url)
        assert response.json == mockup_response_user_not_in_friendlist

def test_send_private_message(client, auth):
    username = 'test'
    friend_username = 'friend_test'
    not_friend_username = 'not_friend_test'
    message = 'test message'

    friend_request_url = f'/friendrequest/send?username={friend_username}'
    friend_request_accept_url = f'/friendrequest/handle?username={username}&accept=true'
    send_private_message_url = f'/pm/send?username={username}&message={message}'
    not_friend_send_private_message_url = f'/pm/send?username={not_friend_username}&message={message}'

    mockup_response_success = {
        'success': True,
        'data': {
            'type': 'private_message',
            'from': friend_username,
            'to': username,
            'message': message
        }
    }
    
    mockup_response_user_not_in_friendlist = {
        'success': False,
        'data': f"{not_friend_username} is not your friend."
    }

    with client:
        # Register 'test'
        register_url = f'/register?username={username}'
        _ = client.post(register_url)

        # Register 'friend_test'
        register_url = f'/register?username={friend_username}'
        _ = client.post(register_url)
        
        # Register 'not_friend_test'
        register_url = f'/register?username={not_friend_username}'
        _ = client.post(register_url)
        
        # Login 'test'
        _ = auth.login(username)
        
        # Send friend request to 'friend_test'
        _ = client.post(friend_request_url)
        
        # Logout 'test'
        _ = auth.logout()

        # Login 'friend_test'
        _ = auth.login(friend_username)

        # Accept friend request from 'test'
        _ = client.post(friend_request_accept_url)

        # Send private message to 'test'
        response = client.post(send_private_message_url)
        assert response.json == mockup_response_success
        
        # Send private message to 'not_friend_test'
        response = client.post(not_friend_send_private_message_url)
        assert response.json == mockup_response_user_not_in_friendlist

def test_show_private_message(client, auth):
    username = 'test'
    friend_username = 'friend_test'
    message = "test message"

    register_test_url = f'/register?username={username}'
    register_friend_test_url = f'/register?username={friend_username}'

    friend_request_url = f'/friendrequest/send?username={friend_username}'
    friend_request_accept_url = f'/friendrequest/handle?username={username}&accept=true'

    send_private_message_url = f'/pm/send?username={username}&message={message}'
    show_private_message_url = '/pm'

    mockup_response_success = {
        'success': True,
        'data': [
            {
                'type': 'private_message',
                'from': friend_username,
                'to': username,
                'message': message
            }
        ]
    }

    with client:
        # Register 'test'
        _ = client.post(register_test_url)

        # Register 'friend_test'
        _ = client.post(register_friend_test_url)
        
        # Login 'test'
        _ = auth.login(username)
        
        # Send friend request to 'friend_test'
        _ = client.post(friend_request_url)
        
        # Logout 'test'
        _ = auth.logout()

        # Login 'friend_test'
        _ = auth.login(friend_username)

        # Accept friend request from 'test'
        _ = client.post(friend_request_accept_url)

        # Send private message to 'test'
        _ = client.post(send_private_message_url)
        
        # Logout 'friend_test'
        _ = auth.logout()

        # Login 'test'
        _ = auth.login(username)

        # Show private message
        response = client.get(show_private_message_url)
        assert response.json == mockup_response_success