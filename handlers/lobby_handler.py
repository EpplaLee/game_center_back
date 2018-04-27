# from base_handler import BaseHandler, secureHandler
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "http://192.168.0.2:3000")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

class secureHandler(BaseHandler):
    def get_current_user(self):
        return self.get_secure_cookie("phone_num")


class EnterGameLobbyHandler(secureHandler):
    def get(self):
        if not self.current_user:
            self.finish({'err': '用户未登录'})
            return
        player = {
            'phone_num': self.get_argument('phone_num'),
            'nickname': self.get_argument('nickname'),
        #TODO:个人信息待补全
        }
        type = self.get_argument('type')
        room = self.application.GameLobby.enterLobby(player, type)
        if room:
            self.finish({
                'msg': '房间信息查询成功',
                'room': room,
            })
        else:
            self.finish({
                'err': '房间信息查询失败'
            })

class LeaveGameLobbyHandler(secureHandler):
    def get(self):
        if not self.current_user:
            self.finish({ 'err': '用户未登录'})
            return
        phone_num = self.get_argument('phone_num')
        type = self.get_argument('type')
        self.application.GameLobby.leaveLobby(phone_num, type)

class LobbyInfoHandler(BaseHandler):
    def get(self):
        self.finish({
            'msg': '查询成功',
            'chess_rooms': self.application.GameLobby.chess_rooms,
            'draw_rooms': self.application.GameLobby.draw_rooms,
            'chess_players': self.application.GameLobby.chess_players,
            'draw_players': self.application.GameLobby.draw_players,
        })
class CreateRoomHandler(secureHandler):
    def get(self):
        pass
    def post(self):
        player = {
            'phone_num': self.get_argument('phone_num'),
            'nickname': self.get_argument('nickname'),
            'authority': 0  #0为房主， 1为访客
        }
        type = self.get_argument('type')
        num = self.application.GameLobby.createRoom(player, type)
        if num:
            self.finish({
                'msg': '创建成功',
                'room_num': num,
                'chess_rooms': self.application.GameLobby.chess_rooms,
                'draw_rooms': self.application.GameLobby.draw_rooms,
            })
        else:
            self.finish({
                'err': '创建请求失败',
            })
class EnterRoomHandler(secureHandler):
    def get(self):
        pass
    def post(self):
        player = {
            'phone_num': self.get_argument('phone_num'),
            'nickname': self.get_argument('nickname'),
            'authority': 1  # 0为房主， 1为访客
        }
        type = self.get_argument('type')
        room_num = self.get_argument('room_num')
        result = self.application.GameLobby.enterRoom(player, type, room_num)
        if result:
            self.finish({
                'msg': '进入房间',
                'chess_rooms': self.application.GameLobby.chess_rooms,
                'draw_rooms': self.application.GameLobby.draw_rooms,
            })
        else:
            self.finish({
                'err': '未找到该房间',
            })


class GameLobby(object):
    # chess_rooms = {
    #     '0001': {
    #         'player_list': [{
    #             'phone_num': '111111',
    #             'nickname': 'Gua',
    #             'authority': 0,
    #         }],
    #         'full_count': 2,
    #         'current_count': 1,
    #         'status': 0,
    #         'data': None,
    #     }
    # }
    chess_rooms = dict()
    chess_players = dict()
    chess_room_num = 0

    draw_rooms = dict()
    draw_players = dict()
    draw_room_num = 0

    def getPlayers(self):
        return self.players

    def getRooms(self):
        return self.rooms

    def enterLobby(self, player, type):
        if type == 'chess':
            self.chess_players[player['phone_num']] = player
            return self.chess_rooms
        elif type == 'draw':
            self.draw_players[player['phone_num']] = player
            return self.draw_rooms
    def leaveLobby(self, phone_num, type):
        if type == 'chess':
            del self.chess_players[phone_num]
        elif type == 'draw':
            del self.draw_players[phone_num]

    def createRoom(self, player, type):
        if type == 'chess':
            chess_room_num = "%04d" % self.chess_room_num
            self.chess_room_num = self.chess_room_num + 1
            self.chess_rooms[chess_room_num]  = {
                'player_list': [player],
                'full_count': 2,
                'current_count': 1,
                'status': 0,    # 0代表等待中，1代表游戏中
                'data': None,
            }
            return chess_room_num
        elif type == 'draw':
            draw_room_num = "%04d" % self.draw_room_num
            self.draw_room_num = self.draw_room_num + 1
            self.draw_rooms[draw_room_num] = {
                'player_list': [player],
                'full_count': 5,
                'current_count': 1,
                'status': 0,  # 0代表等待中，1代表游戏中
                'data': None,
            }
            return draw_room_num

    def deleteRoom(self, type, room_num):
        if type == 'chess':
            del self.chess_rooms[room_num]
        elif type == 'draw':
            del self.draw_rooms[room_num]


    def enterRoom(self, player, type, room_num):
        if type == 'chess':
            if self.chess_rooms[room_num]:
               self.chess_rooms[room_num]['player_list'].append(player)
               self.chess_rooms[room_num]['current_count'] = self.chess_rooms[room_num]['current_count'] + 1
               return True
        elif type == 'draw':
            if self.draw_rooms[room_num]:
                self.draw_rooms[room_num]['player_list'].append(player)
                self.draw_rooms[room_num]['current_count'] = self.draw_rooms[room_num]['current_count'] + 1
                return True

    def leaveRoom(self):
        pass


