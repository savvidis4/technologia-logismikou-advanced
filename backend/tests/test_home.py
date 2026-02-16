from app.extensions import db
from app.models import User, Account

def test_home_load(client, app, auth_header):
    
    with app.app_context():
        user = db.session.query(User).filter_by(email="tester@uniwa.gr").first()
        acc = db.session.query(Account).filter_by(user_id=user.id).first()
        acc.euro_balance = 5500.50
        db.session.commit()

    response = client.get('/home', headers=auth_header)
    
    assert response.status_code == 200
    data = response.get_json()

    assert data["success"] == True
    assert float(data["balance"]) == 5500.50
    assert data["email"] == "tester@uniwa.gr"
    
    assert data["iban"].startswith("GR")
    
    assert "****" in data["card_number"]
    assert len(data["card_number"]) > 4