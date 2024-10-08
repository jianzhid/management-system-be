from flask import Flask, request, session, redirect, url_for, render_template
from flask_cors import CORS,cross_origin
from flask_session import Session
import pymysql
from flask_sqlalchemy import SQLAlchemy


from login.login import Login
from register.register import Register
from qr.generate_qr import GenerateQr

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app,supports_credentials=True)
app.config['SESSION_TYPE'] = 'filesystem'  # 可以是 'memcached', 'redis', etc.
Session(app)

@cross_origin()
def get_user_file_release():
    pass

@app.route('/login', methods=['POST'])
def login():


    # 假设这里有用户验证逻辑
    # 验证成功后，将用户ID存储在session中
    session['user_id'] = 'user123'
    user_id = session.get('user_id')
    print(user_id)
    return 'Login successful', 200


@app.route('/logout')
def logout():
    # 清除session中的用户ID
    session.pop('user_id', None)
    return 'Logout successful', 200


@app.route('/me')
def get_user_info():
    # 检查session中是否有用户ID
    user_id = session.get('user_id')
    print(user_id)
    print('test1')
    if user_id:
        # 用户已登录，返回用户信息
        print('test2')
        return {'user_id': user_id, 'name': 'John Doe'}, 200
    else:
        # 用户未登录，返回错误信息或重定向到登录页面
        print('test3')
        return 'User not logged in', 401


if __name__ == '__main__':
    app.run(debug=True)