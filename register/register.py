from flask import request,make_response



class Register():

    def __init__(self):
        pass

    def person1(self,users):
        res = {
            "code": 0,
            "msg": "OK",
            "data": {}
        }
        idcard = request.form.get('idcard')
        tel=request.form.get('tel')
        for user in users:
            if idcard==user.id_card or tel==user.tel :
                res['code'] = -4
                res['msg'] = '账号已存在，请重新输入'
                return make_response(res)
        return make_response(res)


    def business1(self,users):
        res = {
            "code": 0,
            "msg": "OK",
            "data": {}
        }
        usci = request.form.get('usci')
        for user in users:
            if usci==user.usci:
                res['code'] = -4
                res['msg'] = '账号已存在，请重新输入'
                return make_response(res)
        return make_response(res)




    def person(self, users):
        res = {
            "code": 0,
            "msg": "OK",
            "data": {}
        }

        data = request.json.get("data")
        for user in users:
            if data['idcard'] == user.id_card or data['tel'] == user.tel:
                res['code'] = -4
                res['msg'] = '账号已存在，请重新输入'
                return data, make_response(res)
        return data, make_response(res)


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


