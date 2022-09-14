from src.app import app

def test_index():
    client = app.test_client()
    url = '/'
    response = client.get(url)
    mockup_response = {
        'success': True,
        'data': "Online"
    }
    assert response.json == mockup_response 