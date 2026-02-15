from app.extensions import db
from app.models import User, Account

def test_exchange_success(client, app, auth_header):
    
    with app.app_context():
        user = db.session.query(User).filter_by(email="tester@uniwa.gr").first()
        acc = db.session.query(Account).filter_by(user_id=user.id).first()
        
        acc.euro_balance = 1000.00
        acc.usd_balance = 0.00
        db.session.commit()

    payload = {
        "amount": 100,
        "currencyFrom": "EUR",
        "currencyTo": "USD"
    }
    
    response = client.post('/exchange', json=payload, headers=auth_header)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] == True

    with app.app_context():
        user = db.session.query(User).filter_by(email="tester@uniwa.gr").first()
        acc = db.session.query(Account).filter_by(user_id=user.id).first()
        
        assert float(acc.euro_balance) == 900.00
        
        assert float(acc.usd_balance) > 100.00 


def test_exchange_insufficient_funds(client, app, auth_header):
    
    with app.app_context():
        user = db.session.query(User).filter_by(email="tester@uniwa.gr").first()
        acc = db.session.query(Account).filter_by(user_id=user.id).first()
        acc.euro_balance = 10.00 
        db.session.commit()

    payload = {
        "amount": 100,
        "currencyFrom": "EUR",
        "currencyTo": "USD"
    }
    
    response = client.post('/exchange', json=payload, headers=auth_header)
    data = response.get_json()

    assert data["converted_amount"] == 0.0
    assert "Insufficient" in data["errmsg"]