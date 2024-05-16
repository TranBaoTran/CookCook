import random
import sched
import socket
import sys
import time
from _thread import *
import threading  # Import threading module

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
    print(str(e))

s.listen(2)
print("Waiting for a connection. Server start")

players = [PlayerData(200, 100, "Red"), PlayerData(200, 400, "Blue")]

currentPlayer = 0
map_path = "map01.tmx"
saw_blocks = []
saw_send = []
saw_stop = False
saw_p1 = False
saw_p2 = False
saw_ready = False

# Lock for controlling access to shared data
lock = threading.Lock()


def extract_objects():
    tmx_map = pytmx.TiledMap(map_path)

    for obj in tmx_map.get_layer_by_name("groundboss"):
        if obj.name == "saw":
            saw_blocks.append((obj.x, obj.y, obj.width, obj.height))


def AddSaw(sc):
    global saw_ready
    saw_send.clear()
    for obj in saw_blocks:
        if random.random() > 0.8:
            saw_send.append(obj)
    saw_ready = True


def threaded_client(conn, player):
    global currentPlayer
    conn.send(pickle.dumps(players[player]))
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

                reply = players[1 - player]  # Switch player
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


def event_loop(sc):
    if not saw_stop:
        AddSaw(sc)
    sc.enter(6, 1, event_loop, (sc,))


# Create the scheduler
scheduler = sched.scheduler(time.time, time.sleep)
scheduler.enter(6, 1, event_loop, (scheduler,))

# Start the scheduler in a new thread
threading.Thread(target=scheduler.run).start()

extract_objects()

while True:
    conn, addr = s.accept()
    print("Connect to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
