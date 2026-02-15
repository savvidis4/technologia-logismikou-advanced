import pytest
from app.extensions import db
from app.models import User, Account

def test_get_transactions_empty(client, auth_header):
    
    response = client.get('/transactions', headers=auth_header)
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["success"] == True
    assert isinstance(data["transactions"], list)
    assert len(data["transactions"]) == 0


def test_get_transactions_populated(client, app, auth_header):
    
    client.post('/register', json={
        "email": "recipient@uniwa.gr",
        "password": "Password123!",
        "ver_password": "Password123!"
    })

    recipient_iban = ""
    
    with app.app_context():
        # Get Recipient Info
        recipient = db.session.query(User).filter_by(email="recipient@uniwa.gr").first()
        rec_acc = db.session.query(Account).filter_by(user_id=recipient.id).first()
        recipient_iban = rec_acc.iban
        
        # Fund the Tester (User created by auth_header)
        tester = db.session.query(User).filter_by(email="tester@uniwa.gr").first()
        tester_acc = db.session.query(Account).filter_by(user_id=tester.id).first()
        tester_acc.euro_balance = 1000.00
        db.session.commit()

    transfer_payload = {
        "amount": 50,
        "currency": "EUR",
        "recipient": recipient_iban
    }
    client.post('/transfers', json=transfer_payload, headers=auth_header)

    response = client.get('/transactions', headers=auth_header)
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["success"] == True
    transactions = data["transactions"]
    
    assert len(transactions) > 0
    
    latest_tx = transactions[0] 
    
    assert str(latest_tx[3]).startswith("-50")
    assert latest_tx[4] == "EUR"    
    assert latest_tx[6] == "DEBIT"  