from app.extensions import db
from app.models import User, Account

def test_graphs_empty_data(client, auth_header):
    
    response = client.get('/graphs', headers=auth_header)
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert "pie_chart" in data
    assert "bar_in_out" in data
    assert "count_chart" in data
    
    assert len(data["pie_chart"]["labels"]) == 0
    assert len(data["pie_chart"]["data"]) == 0
    
    assert len(data["bar_in_out"]["labels"]) == 0
    
    assert len(data["count_chart"]["labels"]) == 0
    assert len(data["count_chart"]["data"]) == 0


def test_graphs_populated_data(client, app, auth_header):
    
    with app.app_context():
        user = db.session.query(User).filter_by(email="tester@uniwa.gr").first()
        acc = db.session.query(Account).filter_by(user_id=user.id).first()
        acc.euro_balance = 1000.00
        db.session.commit()

    payload = {
        "amount": 100,
        "currencyFrom": "EUR",
        "currencyTo": "USD"
    }
    client.post('/exchange', json=payload, headers=auth_header)

    response = client.get('/graphs', headers=auth_header)
    assert response.status_code == 200
    data = response.get_json()
    
    assert len(data["pie_chart"]["labels"]) > 0
    assert len(data["pie_chart"]["data"]) > 0
    
    assert len(data["bar_in_out"]["labels"]) > 0
    
    datasets = data["bar_in_out"]["datasets"]
    assert len(datasets) == 2 
    
    money_in = sum(datasets[0]["data"])
    money_out = sum(datasets[1]["data"])
    
    assert (money_in > 0 or money_out > 0)