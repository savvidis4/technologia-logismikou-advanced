from unittest.mock import patch
from app.extensions import db
from app.models import User, Account


def test_logout(client, auth_header):
    
    response = client.post('/logout', headers=auth_header)
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["success"] == True
    assert "Logged out" in data["message"]


def test_email_service_otp(client, auth_header):
    
    with patch('app.business.email_service.smtplib.SMTP') as mock_smtp:
        
        instance = mock_smtp.return_value
        instance.login.return_value = True
        instance.sendmail.return_value = {}
        
        response = client.get('/otp', headers=auth_header)
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data["success"] == True
        assert "message" in data
        
        instance.starttls.assert_called()
        instance.login.assert_called()