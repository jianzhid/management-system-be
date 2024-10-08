from flask import request,make_response



class Register():

    def __init__(self):
        pass

    def person(self,users):
        res = {
            "code": 0,
            "msg": "OK",
            "data": {}
        }
        data = request.json.get("data")
        for user in users:
            if data['idcard']==user.id_card:
                res['code'] = -4
                res['msg'] = '账号已存在，请重新输入'
                return data,make_response(res)
        return data,make_response(res)


    def business(self,users):
        res = {
            "code": 0,
            "msg": "OK",
            "data": {}
        }
        data = request.json.get("data")
        for user in users:
            if data['usci']==user.usci:
                res['code'] = -4
                res['msg'] = '账号已存在，请重新输入'
                return data,make_response(res)
        return data,make_response(res)


