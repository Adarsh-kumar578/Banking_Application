import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_check_balance(client):
    response = client.get('/balance')
    assert response.status_code == 200
    assert response.get_json()['balance'] == 1000.0

def test_deposit_money(client):
    response = client.post('/deposit', json={"amount": 500})
    assert response.status_code == 200
    assert response.get_json()['new_balance'] == 1500.0


def test_withdraw_success(client):
    response = client.post('/withdraw', json={"amount": 400})
    assert response.status_code == 200
    assert response.get_json()['new_balance'] == 1100.0  

def test_withdraw_insufficient_funds(client):
    response = client.post('/withdraw', json={"amount": 5000})
    assert response.status_code == 400
    assert response.get_json()['error'] == "Insufficient funds available."