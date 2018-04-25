# from base_handler import BaseHandler, secureHandler
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

class secureHandler(BaseHandler):
    def get_current_user(self):
        return self.get_secure_cookie("phone_num")
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "http://localhost:3000")


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
        self.application.GameLobby.enterLobby(player, type)

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

class GameLobby(object):
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
            self.chess_players[player.phone_num] = player
        elif type == 'draw':
            self.draw_players[player.phone_num] = player

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
                'owner': player,
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
                'owner': player,
                'full_count': 5,
                'current_count': 1,
                'status': 0,  # 0代表等待中，1代表游戏中
                'data': None,
            }
            return draw_room_num

    def enterRoom(self, room_num, type):
        if type == 'chess':
            del self.chess_rooms[room_num]
        elif type == 'draw':
            del self.draw_rooms[room_num]


    def deleteRoom(self, player, room_num, type):
        if type == 'chess':
            if player.phone_num == self.chess_rooms[room_num]:
                del self.chess_rooms[room_num]
        elif type == 'draw':
            if player.phone_num == self.draw_rooms[room_num]:
                del self.draw_rooms[room_num]



