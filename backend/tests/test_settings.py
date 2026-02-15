from app.extensions import db
from app.models import User, Account, Card
from werkzeug.security import check_password_hash

def test_change_password(client, auth_header):
    
    payload = {
        "old_password": "Password123!", 
        "new_password": "NewStrongPassword99!",
        "new_password_verification": "NewStrongPassword99!"
    }
    
    response = client.post('/change_password', json=payload, headers=auth_header)
    
    if response.status_code != 200 or not response.get_json().get("success"):
        print("\nDEBUG ERROR:", response.get_json())

    assert response.status_code == 200
    assert response.get_json()["success"] == True

    login_payload = {
        "email": "tester@uniwa.gr",
        "password": "NewStrongPassword99!"
    }
    login_res = client.post('/login', json=login_payload)
    
    assert login_res.status_code == 200
    assert login_res.get_json()["success"] == True


def test_change_pin(client, app, auth_header):
    
    current_pin = ""
    
    with app.app_context():
        user = db.session.query(User).filter_by(email="tester@uniwa.gr").first()
        acc = db.session.query(Account).filter_by(user_id=user.id).first()
        card = db.session.query(Card).filter_by(account_id=acc.id).first()
        
        current_pin = str(card.card_number)[-4:]

    payload = {
        "old_pin": current_pin,
        "new_pin": "0000",
        "new_pin_verification": "0000"
    }
    
    response = client.post('/change_pin', json=payload, headers=auth_header)
    assert response.status_code == 200
    assert response.get_json()["success"] == True

    with app.app_context():
        user = db.session.query(User).filter_by(email="tester@uniwa.gr").first()
        acc = db.session.query(Account).filter_by(user_id=user.id).first()
        card = db.session.query(Card).filter_by(account_id=acc.id).first()
        
        assert check_password_hash(card.card_pin_hash, "0000")


def test_change_email(client, app, auth_header):
    
    payload = {
        "old_email": "tester@uniwa.gr",
        "new_email": "new_email@uniwa.gr",
        "new_email_verification": "new_email@uniwa.gr"
    }
    
    response = client.post('/change_email', json=payload, headers=auth_header)
    assert response.status_code == 200
    assert response.get_json()["success"] == True

    with app.app_context():
        
        old_user = db.session.query(User).filter_by(email="tester@uniwa.gr").first()
        assert old_user is None
        
        new_user = db.session.query(User).filter_by(email="new_email@uniwa.gr").first()
        assert new_user is not None
        assert new_user.id is not None