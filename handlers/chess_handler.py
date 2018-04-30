import tornado.websocket
import json
from datetime import datetime

class ChessWebSocket(tornado.websocket.WebSocketHandler):
    chess_pool = dict()
    def check_origin(self, origin):
        return True
    def open(self):
        # phone_num = self.get_secure_cookie("phone_num").decode()
        # ChessWebSocket.chess_pool[phone_num] = self
        pass
    def on_close(self):
        phone_num = self.get_secure_cookie("phone_num").decode()
        del ChessWebSocket.chess_pool[phone_num]
        # 加上leaveRoom方法
        pass
    @staticmethod
    def send_to_all(message):
        pass
    def on_message(self, message):
        chess_req = json.loads(message)
        cur_player = {
            'phone_num': chess_req['phone_num'],
            'nickname': chess_req['nickname'],
        }
        # TODO: 若两次连接过于接近以至于同时进入else逻辑（在前端控制先后？）
        if int(chess_req['action']) == 0:
            if ChessWebSocket.chess_pool[chess_req['room_num']]:
                ChessWebSocket.chess_pool[chess_req['room_num']]['player'].append(cur_player)
                ChessWebSocket.chess_pool[chess_req['room_num']]['pool'].append(self)
                for i in ChessWebSocket.chess_pool[chess_req['room_num']]['pool']:
                    i.write_message({
                        'action': 0,
                        'player':  ChessWebSocket.chess_pool[chess_req['room_num']]['player'],
                        'second_to_play': chess_req['phone_num'],
                        'chess_list': ChessWebSocket.chess_pool[chess_req['room_num']]['data']['chess_list'],
                    })
            else:
                chess_list = []
                for i in range(15):
                    chess_list[i] = []
                    for j in range(15):
                        chess_list[i][j] = 0
                ChessWebSocket.chess_pool[chess_req['room_num']] = {
                    'player': [cur_player],
                    'pool': [self],
                    'chess_list': chess_list,
                }
        elif int(chess_req['action']) == 1:
            ChessWebSocket.laozi(self, chess_req)
            if ChessWebSocket.judge(chess_req['x'], chess_req['y'], chess_req['color'] ):
                for i in ChessWebSocket.chess_pool[chess_req['room_num']]['pool']:
                    i.write_message({
                        'action': 2,
                        'x': chess_req['x'],
                        'y': chess_req['y'],
                        'color': chess_req['color'],
                        'chess_list': ChessWebSocket.chess_pool[chess_req['room_num']]['data']['chess_list'],
                    })
            else:
                for i in ChessWebSocket.chess_pool[chess_req['room_num']]['pool']:
                    i.write_message({
                        'action': 1,
                        'x': chess_req['x'],
                        'y': chess_req['y'],
                        'color': 2 if chess_req['color'] == 1 else 1,
                        'chess_list': ChessWebSocket.chess_pool[chess_req['room_num']]['data']['chess_list'],
                    })

    @classmethod
    def laozi(cls, self, chess_req):
        chess_list = cls.chess_pool[chess_req['room_num']]['chess_list']
        chess_list[chess_req['x']][chess_req['y']] = chess_req['color']

    @classmethod
    def judge(cls, x, y, color):
        chess_list = cls.chess_pool[chess_req['room_num']]['chess_list']
        dir0 = 0
        dir1 = 0
        dir2 = 0
        dir3 = 0
        #   判断左右方向是否五子连珠
        for i in range(x)[::-1]:
            if chess_list[i][y] == color:
                dir0 += 1
            else:
                break
        for i in range(x + 1, 15):
            if chess_list[i][y] == color:
                dir0 += 1
            else:
                break
        #   判断上下方向是否五子连珠
        for i in range(y)[::-1]:
            if chess_list[x][i] == color:
                dir1 += 1
            else:
                break
        for i in range(y + 1, 15):
            if chess_list[x][i] == color:
                dir1 += 1
            else:
                break
        #   判断撇方向是否五子连珠
        i = 0
        while x+i<15 and y-i>=0:
            i += 1
            if chess_list[x+i][y-i] == color:
                dir2 += 1
            else:
                break
        i = 0
        while x-i>=0 and y+i<15:
            i += 1
            if chess_list[x-i][y+i] == color:
                dir2 += 1
            else:
                break
        # 判断捺方向是否五子连珠
        i=0
        while x-i>=0 and y-i>=0:
            i += 1
            if chess_list[x-i][y-i] == color:
                dir3 += 1
            else:
                break
        i=0
        while x+i<15 and y+i<15:
            i += 1
            if chess_list[x+i][y+i] == color:
                dir3 += 1
            else:
                break
        return dir0>=5 or dir1>=5 or dir2>=5 or dir3>=5


