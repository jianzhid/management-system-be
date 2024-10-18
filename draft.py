from flask import Flask, request, jsonify
# 假设使用twilio服务发送短信验证码
from twilio.rest import Client
import random

app = Flask(__name__)
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)


@app.route('/send-code', methods=['POST'])
def send_code():
    phone_number = request.json.get('phone_number')
    code = str(random.randint(100000, 999999))
    message = client.messages.create(
        to=phone_number,
        from_='your_twilio_number',
        body=f"Your verification code is {code}."
    )
    # 将生成的验证码保存到session或数据库以供后续验证
    # session['code'] = code
    return jsonify({"message": "Code sent successfully!"})


@app.route('/verify-code', methods=['POST'])
def verify_code():
    phone_number = request.json.get('phone_number')
    code = request.json.get('code')
    # 从session或数据库获取验证码并验证
    # saved_code = session.get('code')
    # if saved_code and code == saved_code:
    if code == "expected_code_from_database":  # 示例代码，应从数据库获取实际验证码
        return jsonify({"message": "Code verified!"})
    else:
        return jsonify({"error": "Invalid code!"}), 403


if __name__ == '__main__':
    app.run(debug=True)