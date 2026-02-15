import pytest
from app.extensions import db
from app.models import User, Account

def test_transfer_success(client, app, auth_header):
    
    client.post('/register', json={
        "email": "recipient@uniwa.gr",
        "password": "Password123!",
        "ver_password": "Password123!"
    })

    recipient_iban = ""

    with app.app_context():

        recipient = db.session.query(User).filter_by(email="recipient@uniwa.gr").first()
        rec_acc = db.session.query(Account).filter_by(user_id=recipient.id).first()
        recipient_iban = rec_acc.iban
        
        sender = db.session.query(User).filter_by(email="tester@uniwa.gr").first()
        sender_acc = db.session.query(Account).filter_by(user_id=sender.id).first()
        sender_acc.euro_balance = 500.00
        db.session.commit()

    payload = {
        "amount": 100,
        "currency": "EUR",
        "recipient": recipient_iban
    }
    
    response = client.post('/transfers', json=payload, headers=auth_header)

    assert response.status_code == 200
    assert response.get_json()["success"] == True

    with app.app_context():
        
        sender = db.session.query(User).filter_by(email="tester@uniwa.gr").first()
        s_acc = db.session.query(Account).filter_by(user_id=sender.id).first()
        assert float(s_acc.euro_balance) == 400.00

        recipient = db.session.query(User).filter_by(email="recipient@uniwa.gr").first()
        r_acc = db.session.query(Account).filter_by(user_id=recipient.id).first()
        assert float(r_acc.euro_balance) == 100.00


def test_transfer_insufficient_funds(client, app, auth_header):
    
    with app.app_context():
        sender = db.session.query(User).filter_by(email="tester@uniwa.gr").first()
        sender_acc = db.session.query(Account).filter_by(user_id=sender.id).first()
        sender_acc.euro_balance = 0.00
        db.session.commit()

    payload = {
        "amount": 50,
        "currency": "EUR",
        "recipient": "GR1234567890123456789012345" 
    }

    response = client.post('/transfers', json=payload, headers=auth_header)

    assert response.status_code == 401 
    assert response.get_json()["success"] == False
    assert "Insufficient funds" in response.get_json()["message"]


def test_transfer_invalid_iban(client, auth_header):
    
    payload = {
        "amount": 10,
        "currency": "EUR",
        "recipient": "GR_FAKE_IBAN_9999"
    }

    response = client.post('/transfers', json=payload, headers=auth_header)

    assert response.get_json()["success"] == False