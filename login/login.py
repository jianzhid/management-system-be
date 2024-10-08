from flask import request,make_response,session

class Login():

    def __init__(self):
        pass


    def login(self,users,data):
        res={
            'code':0,
            'msg':'OK',
            'data':{}
        }
        way=data['way']
        username = data['username']
        password = data['password']
        user_info=None
        if way=='person':
            for user in users:
                if (username==user.tel and password==user.password) or (username==user.id_card and password==user.password):
                    user_info=user.tel
                    return user_info,make_response(res)
            res['code']=-1
            res['msg']='请填写正确的账号密码'
            return user_info,make_response(res)
        elif way=='business':
            for user in users:
                if username==user.usci and password==user.password:
                    user_info=user.usci
                    return user_info,make_response(res)
            res['code']=-1
            res['msg']='请填写正确的账号密码'
            return user_info,make_response(res)
        elif way=='':
            res['code'] = -2
            res['msg'] = '请选择正确的登录方式'
            return user_info,make_response(res)
        else:
            res['code']=-1
            res['msg']='请填写正确的账号密码'
            return user_info,make_response(res)

