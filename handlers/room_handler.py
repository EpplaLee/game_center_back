import tornado.websocket
from datetime import datetime

class RoomWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def open(self):

        pass
    def on_close(self):
        pass
    @staticmethod
    def send_to_all(message):
        pass
        # for i in EchoWebSocket.chatroom_pool:
        #     i.write_message(message)
    def on_message(self, message):
        pass
        # print('msg receive:', message)
        # phone_num = self.get_secure_cookie("phone_num")
        # time = datetime.now().strftime("%H:%M:%S")
        # EchoWebSocket.update(str(phone_num) + '(' + time + '):' +  message)
    @classmethod
    def update(cls, msg):
        for i in cls.chatroom_pool:
            i.write_message(msg)
