import socket
from _thread import *
import pickle
from game import Game

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    print("Player", p, " connected")

    reply = ""
    while True:
        try:
            data = conn.recv(4096)
            game = games[gameId]
            revThing = pickle.loads(data)
            if not revThing:
                break
            else:
                if isinstance(revThing, str):
                    if revThing == "reset":
                        print("game reseting")
                        game.resetGame()
                    elif data != "get":
                        pass
                    games[gameId] = game
                    conn.sendall(pickle.dumps(game))
                elif isinstance(revThing, Game):
                    games[gameId] = revThing
                    conn.sendall(pickle.dumps(revThing))

        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


player = ["Dealer", "Player"]
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("New Game")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, player[p], gameId))
