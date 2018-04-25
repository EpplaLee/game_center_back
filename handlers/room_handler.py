import tornado.websocket
from datetime import datetime

class RoomWebSocket(tornado.websocket.WebSocketHandler):
    chatroom_pool = set()
    def check_origin(self, origin):
        return True
    def open(self):
        print('ws open')
        EchoWebSocket.chatroom_pool.add(self)
        phone_num = self.get_secure_cookie("phone_num")
        EchoWebSocket.send_to_all(str(phone_num) + '加入了聊天室')
    def on_close(self):
        print('ws close')
        EchoWebSocket.chatroom_pool.remove(self)
        phone_num = self.get_secure_cookie("phone_num")
        EchoWebSocket.send_to_all(str(phone_num) + '离开了聊天室')
    @staticmethod
    def send_to_all(message):
        for i in EchoWebSocket.chatroom_pool:
            i.write_message(message)
    def on_message(self, message):
        print('msg receive:', message)
        phone_num = self.get_secure_cookie("phone_num")
        time = datetime.now().strftime("%H:%M:%S")
        # EchoWebSocket.update(dict(
        #     phone_num = str(phone_num),
        #     msg = message,
        #     #
        # ))
        EchoWebSocket.update(str(phone_num) + '(' + time + '):' +  message)
    @classmethod
    def update(cls, msg):
        for i in cls.chatroom_pool:
            i.write_message(msg)
