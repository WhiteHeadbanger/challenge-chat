def test_create_room(client, auth):
    username = 'test'
    room_name = 'room_test'

    register_url = f'/register?username={username}'
    room_create_url = f'/room/create?room_name={room_name}'

    mockup_response_success = {
        'success': True,
        'data': f"{room_name} created."
    }

    with client:
        # Register 'test'
        _ = client.post(register_url)

        # Login 'test'
        _ = auth.login(username)

        # Create room
        response = client.post(room_create_url)
        assert response.json == mockup_response_success

def test_invite_to_room_success(client, auth):
    username = 'test'
    friend_username = 'friend_test'
    room_name = 'room_test'

    register_username_url = f'/register?username={username}'
    register_friend_username_url = f'/register?username={friend_username}'
    friend_request_url = f'/friendrequest/send?username={friend_username}'
    friend_request_accept_url = f'/friendrequest/handle?username={username}&accept=true'
    room_create_url = f'/room/create?room_name={room_name}'
    room_invite_url = f'/room/invite?room_name={room_name}&username={username}'

    mockup_response_success = {
        'success': True,
        'data': f'{username} added to {room_name}'
    }

    with client:
        # Register 'test'
        _ = client.post(register_username_url)
        
        # Register 'friend_test'
        _ = client.post(register_friend_username_url)

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

        # Create room 
        _ = client.post(room_create_url)

        # Invite 'test' to the room 'room_test'
        response = client.post(room_invite_url)
        assert response.json == mockup_response_success


def test_invite_to_room_failed_not_in_friendlist(client, auth):
    username = 'test'
    not_friend_username = 'not_friend_test'
    room_name = 'room_test'

    register_username_url = f'/register?username={username}'
    register_not_friend_username_url = f'/register?username={not_friend_username}'
    
    room_create_url = f'/room/create?room_name={room_name}'
    room_invite_url = f'/room/invite?room_name={room_name}&username={not_friend_username}'

    mockup_response_user_not_in_friendlist = {
        'success': False,
        'data': f'{not_friend_username} is not your friend.'
    }

    with client:
        # Register 'test'
        _ = client.post(register_username_url)
        
        # Register 'not_friend_test'
        _ = client.post(register_not_friend_username_url)

        # Login 'test'
        _ = auth.login(username)

        # Create room 
        _ = client.post(room_create_url)

        # Invite 'not_friend_test' to the room 'room_test'
        response = client.post(room_invite_url)
        assert response.json == mockup_response_user_not_in_friendlist

def test_send_message_to_room(client, auth):
    username = 'test'
    friend_username = 'friend_test'
    room_name = 'room_test'
    message = 'test message'

    friend_request_url = f'/friendrequest/send?username={friend_username}'
    friend_request_accept_url = f'/friendrequest/handle?username={username}&accept=true'

    room_create_url = f'/room/create?room_name={room_name}'
    room_invite_url = f'/room/invite?room_name={room_name}&username={username}'
    send_room_message_url = f'/room/send?room_name={room_name}&message={message}'

    mockup_response_success = {
        'success': True,
        'data': {
            'type': 'room_message',
            'from': friend_username,
            'to': room_name,
            'message': message
        }
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

        # Create room 'room_test'
        _ = client.post(room_create_url)

        # Invite 'test' to 'room_test'
        _ = client.post(room_invite_url)

        # Send room message to 'room_test'
        response = client.post(send_room_message_url)
        assert response.json == mockup_response_success

