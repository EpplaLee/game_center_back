# from base_handler import BaseHandler

import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "http://192.168.0.246:3000")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

class secureHandler(BaseHandler):
    def get_current_user(self):
        return self.get_secure_cookie("phone_num")


class LoginHandler(BaseHandler):
    def get(self):
        pass
    def post(self):
        user_db = self.application.db.user

        phone_num = self.get_argument('phone_num')
        password = self.get_argument('password')

        find_result = user_db.find_one({"phone_num": phone_num})

        if find_result:
            if find_result['password'] == password:
                self.set_secure_cookie('phone_num', phone_num)
                self.finish({ 'msg': '登录成功', "nickname": find_result['nickname'] })
            else:
                self.finish({ 'err': '用户名与密码不符'})
        else:
            self.finish({ 'err': '该帐号尚未注册'})

class SignupHandler(BaseHandler):
    def get(self):
        pass
    def post(self):
        user_db = self.application.db.user
        phone_num = self.get_argument('phone_num')
        if user_db.find_one({ "phone_num": phone_num }):
            self.finish({ 'err': '手机号已被注册'})
        else:
            user_db.insert_one({
                "phone_num": self.get_argument('phone_num'),
                "password": self.get_argument('password'),
                "nickname": self.get_argument('nickname'),
            })
            # TODO：错误处理
            self.set_secure_cookie('phone_num', phone_num)
            self.finish({ 'msg': '注册成功' })