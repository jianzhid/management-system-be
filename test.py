from flask import Flask, jsonify, request,make_response,session,send_file  # 导入Flask类库
from flask_cors import CORS,cross_origin
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy import create_engine
from qrcode.main import QRCode
import qrcode
import tempfile
import io

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


pymysql.install_as_MySQLdb()

host = '127.0.0.1'
port='3306'
user = 'root'
password = '123456'
database = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://%s:%s@%s:3306/%s" % (user, password, host, database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 创建数据库 sqlalchemy 工具对象
db = SQLAlchemy(app)



class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))

class User(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    tel = db.Column(db.String(64))
    id_card = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    email = db.Column(db.String(64))
    referrer = db.Column(db.String(64))



class Business(db.Model):
    __tablename__ = 'business'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    usci = db.Column(db.String(64))
    adress = db.Column(db.String(64))
    bn = db.Column(db.String(64))
    money = db.Column(db.String(64))
    time = db.Column(db.String(64))
    # time = db.Column(db.Date)
    person = db.Column(db.String(64))
    tel = db.Column(db.String(64))
    referrer = db.Column(db.String(64))
    password = db.Column(db.String(64))




# with app.app_context():
#     db.create_all()
#     new_user=Test(name='Haha')
#     db.session.add(new_user)
#     db.session.commit()



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
    if user_id:
        # 用户已登录，返回用户信息
        return {'user_id': user_id}, 200
    else:
        # 用户未登录，返回错误信息或重定向到登录页面
        print('test3')
        return 'User not logged in', 401




@app.route('/login', methods=["POST"])
def login():
    print('test1')
    data = request.json.get("data")
    way = data['way']
    if way=='person':
        users = Person.query.all()
        user_info,login_data = Login().login(users,data)
        print(login_data.get_json()['code'])
        if login_data.get_json()['code']==0:
            session['user_id'] = user_info
        return login_data
    elif way=='business':
        users = Business.query.all()
        user_info,login_data = Login().login(users,data)
        if login_data.get_json()['code']==0:
            session['user_id'] = user_info
        return login_data,
    elif way=='':
        res={
            'code':-1,
            'msg':'请选择正确的登录方式',
            'data':{}
        }
        return make_response(res)
    else:
        res={
            'code':-2,
            'msg':'请填写正确的账号密码',
            'data':{}
        }
        return make_response(res)




@app.route('/per_register', methods=["POST"])
def per_register():
    users = Person.query.all()
    data,res=Register().person(users)
    if res.get_json()['code'] == 0:
        name = data['name']
        tel = data['tel']
        idcard = data['idcard']
        gender = data['gender']
        email = data['email']
        referrer = data['referrer']
        password = data['pass']
        user=Person(username=name,password=password,tel=tel,id_card=idcard,gender=gender,email=email,referrer=referrer)
        db.session.add(user)
        db.session.commit()
        return res
    else:
        return res

@app.route('/bus_register', methods=["POST"])
def bus_register():
    users = Business.query.all()
    data,res=Register().business(users)
    if res.get_json()['code'] == 0:
        name = data['name']
        usci = data['usci']
        adress = data['adress']
        bn = data['bn']
        money = data['money']
        time = data['time']
        person = data['person']
        tel = data['tel']
        referrer = data['referrer']
        password = data['twopass']
        print(time)
        print(type(time))
        user=Business(name=name,usci=usci,adress=adress,bn=bn,money=money,time=time,
                    person=person,tel=tel,referrer=referrer,password=password)
        db.session.add(user)
        print('test2')
        db.session.commit()
        return res
    else:
        return res



# 用于生成二维码的路由
@app.route('/generate_qr/<string:data>')
def generate_qr(data):
    print('test')
    print(data)
    return GenerateQr().generate_qr1(data)


@app.route('/generate_qrcode', methods=['POST'])
def generate_qr_image():
    print('test')
    link= request.json.get("data")['url']
    print(link)
    return GenerateQr().generate_qr1(link)






@app.route('/test1')
def test1():
    user_id = request.args.get('userId')
    # 你可以在这里使用user_id做后续处理
    print('test')
    print(user_id)
    return f"Received user ID: {user_id}"

@app.route('/user/<string:user_id>')
def user(user_id):
    # 这里的 id 就是通过路由传递过来的参数
    print(user_id)
    return f"User ID: {id}"


@app.route('/test2', methods=['POST'])
def post_example():
    data = request.get_json()  # 获取JSON格式的数据
    # 或者使用 request.form 如果发送的是表单数据
    # data = request.form
    # 处理data...
    print(data)
    print(type(data))
    print(data['userId'])
    return jsonify({'message': 'Data received!', 'received_data': data}), 200




@app.route('/your-flask-endpoint')
def your_flask_method():
    # 你的Flask方法逻辑
    response_data = {'message': 'Hello from Flask!'}
    return jsonify(response_data)

@app.route('/send-data', methods=['POST'])
def receive_data():
    data = request.json.get('data')
    # 处理data
    return jsonify({'status': 'success', 'data': data})

@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    if request.method == 'GET':
        data = request.args.get('input_data')
    elif request.method == 'POST':
        data = request.form.get('input_data')
    return f"收到的数据是: {data}"

if __name__ == '__main__':  # 启动服务
   app.run(debug = True,port=5000)