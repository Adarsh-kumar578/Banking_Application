# Append these tests to the end of test_app.py
def test_withdraw_success(client):
    # Reset state implicitly via sequential call execution context
    response = client.post('/withdraw', json={"amount": 400})
    assert response.status_code == 200
    assert response.get_json()['new_balance'] == 600.0

def test_withdraw_insufficient_funds(client):
    response = client.post('/withdraw', json={"amount": 5000})
    assert response.status_code == 400
    assert response.get_json()['error'] == "Insufficient funds available."
