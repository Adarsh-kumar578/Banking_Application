# Add this new route inside app.py beneath your deposit_money endpoint
@app.route('/withdraw', methods=['POST'])
def withdraw_money():
    global account_balance
    data = request.get_json()

    if not data or 'amount' not in data:
        return jsonify({"error": "Invalid payload. 'amount' is required."}), 400

    amount = float(data['amount'])
    if amount <= 0:
        return jsonify({"error": "Withdrawal amount must be greater than zero."}), 400

    # Business Rules / Balance Validation
    if amount > account_balance:
        return jsonify({"error": "Insufficient funds available."}), 400

    account_balance -= amount
    return jsonify({"message": f"Successfully withdrew ${amount:.2f}", "new_balance": account_balance}), 200
