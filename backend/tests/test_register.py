import json

def test_register(client):
    
    register_data = {
        "email": "student@uniwa.gr",
        "password": "StrongPassword123!",
        "ver_password": "StrongPassword123!"
    }
    
    reg_response = client.post('/register', json=register_data)
    assert reg_response.status_code == 201  
    
    reg_json = reg_response.get_json()
    assert reg_json["success"] == True
    assert "iban" in reg_json
    assert "card_number" in reg_json

    