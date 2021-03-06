from handlers.lobby_handler import EnterGameLobbyHandler,LeaveGameLobbyHandler, LobbyInfoHandler, CreateRoomHandler, EnterRoomHandler
from handlers.user_handler import LoginHandler, SignupHandler, CheckLoginHandler
from handlers.chat_handler import EchoWebSocket
from handlers.room_handler import RoomWebSocket

urls = [
    (r'/api/login', LoginHandler),
    (r'/api/signup', SignupHandler),
    (r'/api/login/check', CheckLoginHandler),
    (r'/api/lobby/enter', EnterGameLobbyHandler),
    (r'/api/lobby/leave', LeaveGameLobbyHandler),
    (r'/api/lobby', LobbyInfoHandler),
    (r'/api/room/create', CreateRoomHandler),
    (r'/api/room/enter', EnterRoomHandler),
    (r'/ws/chatroom', EchoWebSocket),
    (r'/ws/gameroom', RoomWebSocket),
]
