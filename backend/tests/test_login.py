import json

def test_login_jwt(client, test_user):

    # ---------------------------------------------------------
    # 1. Test Login
    # ---------------------------------------------------------
    login_data = {
        "email": test_user['email'],
        "password": test_user['password']
    }
    
    log_response = client.post('/login', json=login_data)
    assert log_response.status_code == 200
    
    log_json = log_response.get_json()
    assert log_json["success"] == True
    assert "token" in log_json
    
    token = log_json["token"]

    # ---------------------------------------------------------
    # 2. Test Protected Route (/home) Using the JWT Token
    # ---------------------------------------------------------
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    home_response = client.get('/home', headers=headers)
    assert home_response.status_code == 200
    
    home_json = home_response.get_json()
    assert home_json["success"] == True
    assert "balance" in home_json
    assert "iban" in home_json
    assert home_json["email"] == test_user['email']