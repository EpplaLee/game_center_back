import tornado.websocket
import json
from datetime import datetime

class RoomWebSocket(tornado.websocket.WebSocketHandler):
    room_pool = dict()
    def check_origin(self, origin):
        return True
    def open(self):
        phone_num = self.get_secure_cookie("phone_num").decode()
        RoomWebSocket.room_pool[phone_num] = self
        pass
    def on_close(self):
        phone_num = self.get_secure_cookie("phone_num").decode()
        del RoomWebSocket.room_pool[phone_num]
        # 加上leaveRoom方法
        pass
    @staticmethod
    def send_to_all(message):
        pass
    def on_message(self, message):
        room_req = json.loads(message)
        if int(room_req['action']) == 0:
            RoomWebSocket.relayEnterRoom(self, room_req)
        elif int(room_req['action']) == 1:
            RoomWebSocket.relayGameStart(self, room_req)
    @classmethod
    def update(cls, msg):
        for i in cls.chatroom_pool:
            i.write_message(msg)

    def relayEnterRoom(self, room_req):
        if room_req['type'] == 'chess':
            player_list = self.application.GameLobby.chess_rooms[room_req['room_num']]['player_list']
        elif room_req['type'] == 'draw':
            player_list = self.application.GameLobby.draw_rooms[room_req['room_num']]['player_list']
        print(RoomWebSocket.room_pool)

        if player_list:
            for item in player_list:
                RoomWebSocket.room_pool[item['phone_num']].write_message({
                    'action': 0, # 0为更新列表，1为开始游戏
                    'player_list': player_list,
                })


    def relayGameStart(self, room_req):
        if room_req['type'] == 'chess':
            player_list = self.application.GameLobby.chess_rooms[room_req['room_num']]['player_list']
        elif room_req['type'] == 'draw':
            player_list = self.application.GameLobby.draw_rooms[room_req['room_num']]['player_list']
        print(RoomWebSocket.room_pool)

        if player_list:
            for item in player_list:
                RoomWebSocket.room_pool[item['phone_num']].write_message({
                    'action': 1, # 0为更新列表，1为开始游戏
                    'player_list': player_list,
                })
