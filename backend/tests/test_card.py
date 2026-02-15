import pytest
from app.extensions import db
from app.models import User, Account, Card

def test_get_card_info(client, auth_header):
    
    response = client.get('/card', headers=auth_header)
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["success"] == True
    assert "number" in data
    assert "cvv" in data
    assert "exp" in data
    
    assert data["isFrozen"] == False


def test_card_freeze_toggle(client, app, auth_header):
    
    response = client.post('/card', headers=auth_header)
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["success"] == True
    assert data["isFrozen"] == True  
    
    with app.app_context():
        user = db.session.query(User).filter_by(email="tester@uniwa.gr").first()
        acc = db.session.query(Account).filter_by(user_id=user.id).first()
        card = db.session.query(Card).filter_by(account_id=acc.id).first()
        assert card.frozen_card == True

    response = client.post('/card', headers=auth_header)
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["isFrozen"] == False 
    
    with app.app_context():
        user = db.session.query(User).filter_by(email="tester@uniwa.gr").first()
        acc = db.session.query(Account).filter_by(user_id=user.id).first()
        card = db.session.query(Card).filter_by(account_id=acc.id).first()
        assert card.frozen_card == False