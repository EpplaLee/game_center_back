from handlers.lobby_handler import EnterGameLobbyHandler,LeaveGameLobbyHandler, LobbyInfoHandler
from handlers.user_handler import LoginHandler, SignupHandler
from handlers.chat_handler import EchoWebSocket

urls = [
    (r'/api/login', LoginHandler),
    (r'/api/signup', SignupHandler),
    (r'/api/lobby/enter', EnterGameLobbyHandler),
    (r'/api/lobby/leave', LeaveGameLobbyHandler),
    (r'/api/lobby', LobbyInfoHandler),
    (r'/ws/chatroom', EchoWebSocket),
]
