from flask import Flask, jsonify, request


app = Flask(__name__)


account_balance = 1000.0


@app.route('/', methods=['GET'])
def menu():
    return jsonify({
        "message": "Welcome to the Simple Banking Application",
        "options": {
            "1": "Check Balance (/balance)",
            "2": "Deposit Money (/deposit)",
            "3": "Withdraw Money (/withdraw)"
        }
    })

@app.route('/balance', methods=['GET'])
def check_balance():
    return jsonify({"balance": account_balance}), 200

@app.route('/deposit', methods=['POST'])
def deposit_money():
    global account_balance
    data = request.get_json()
    
    if not data or 'amount' not in data:
        return jsonify({"error": "Invalid payload. 'amount' is required."}), 400
        
    amount = float(data['amount'])
    if amount <= 0:
        return jsonify({"error": "Deposit amount must be greater than zero."}), 400
        
    account_balance += amount
    return jsonify({"message": f"Successfully deposited ${amount:.2f}", "new_balance": account_balance}), 200

@app.route('/withdraw', methods=['POST'])
def withdraw_money():
    global account_balance
    data = request.get_json()
    
    if not data or 'amount' not in data:
        return jsonify({"error": "Invalid payload. 'amount' is required."}), 400
        
    amount = float(data['amount'])
    if amount <= 0:
        return jsonify({"error": "Withdrawal amount must be greater than zero."}), 400
        
    
    if amount > account_balance:
        return jsonify({"error": "Insufficient funds available."}), 400
        
    account_balance -= amount
    return jsonify({"message": f"Successfully withdrew ${amount:.2f}", "new_balance": account_balance}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)