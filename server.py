import sched
import socket
import sys
import time
from _thread import *

import pytmx

import globalvariable
from Data import PlayerData
import pickle

hostname = socket.gethostname()
ipv4_address = socket.gethostbyname(hostname)
server = ipv4_address
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection. Server start")

players = [PlayerData(200, 100, "Red"), PlayerData(200, 400, "Blue")]

currentPlayer = 0


def AddSaw():
    # do something
    pass


def threaded_client(conn, player):
    global currentPlayer
    # players[player].connected = currentPlayer
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048 * 8))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                players[player].connected = currentPlayer

                if players[0].die and players[1].die:
                    players[player].restart = True
                else:
                    players[player].restart = False

                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print(reply.connected)
            conn.sendall(pickle.dumps(reply))
        except:
            break
    try:
        del players[player]
        print("Closing Game", player)
    except:
        pass
    currentPlayer -= 1
    print("Lost connection")
    conn.close()


scheduler = sched.scheduler(time.time, time.sleep)


# Define an event loop function
def event_loop(sc):
    AddSaw()
    sc.enter(10, 1, event_loop, (sc,))


# Schedule the first event loop call
scheduler.enter(10, 1, event_loop, (scheduler,))

while True:
    conn, addr = s.accept()
    print("Connect to: ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
