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
laser_blocks = []
saw_send = []
laser_send = []
saw_ready = False
laser_warn_ready = False
saw_stop = True
laser_stop = True

# Lock for controlling access to shared data
lock = threading.Lock()


def extract_objects():
    tmx_map = pytmx.TiledMap(map_path)

    for obj in tmx_map.get_layer_by_name("groundboss"):
        if obj.name == "saw":
            saw_blocks.append((obj.x, obj.y, obj.width, obj.height))

    for obj in tmx_map.get_layer_by_name("laser"):
        if obj.name == "laser":
            laser_blocks.append((obj.x, obj.y, obj.width, obj.height))


def AddSaw(sc):
    global saw_ready
    saw_send.clear()
    for obj in saw_blocks:
        if random.random() > 0.8:
            saw_send.append(obj)
    saw_ready = True


def AddWarnLaser(sc):
    global laser_warn_ready
    laser_send.clear()
    for obj in laser_blocks:
        if random.random() > 0.9:
            if random.randint(0, 500) % 2 == 0:
                laser_send.append((obj[0], obj[1], True))
            else:
                laser_send.append((obj[0], obj[1], False))
    laser_warn_ready = True


def threaded_client(conn, player):
    global currentPlayer, saw_ready, laser_warn_ready, saw_stop, laser_stop
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
                if currentPlayer == 2:
                    saw_stop = False
                    laser_stop = False

                if saw_ready:
                    players[0].saws.clear()
                    players[1].saws.clear()
                    players[0].isSawSend = True
                    players[1].isSawSend = True
                    for obj in saw_send:
                        players[0].saws.append(obj)
                        players[1].saws.append(obj)
                    saw_ready = False
                    players[0].isSawReceive = True
                    players[1].isSawReceive = True

                if laser_warn_ready:
                    players[0].lasers.clear()
                    players[1].lasers.clear()
                    players[0].isLaserSend = True
                    players[1].isLaserSend = True
                    for obj in laser_send:
                        players[0].lasers.append(obj)
                        players[1].lasers.append(obj)
                    laser_warn_ready = False
                    players[0].isLaserReceive = True
                    players[1].isLaserReceive = True

                if players[0].die and players[1].die:
                    players[player].restart = True
                else:
                    players[player].restart = False

                reply = players[1 - player]  # Switch player
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


def event_warn_laser_loop(sc):
    if not laser_stop:
        AddWarnLaser(sc)
    sc.enter(1.7, 1, event_warn_laser_loop, (sc,))


# Create the scheduler
scheduler = sched.scheduler(time.time, time.sleep)
scheduler.enter(6, 1, event_loop, (scheduler,))

warn_laser_scheduler = sched.scheduler(time.time, time.sleep)
warn_laser_scheduler.enter(1.7, 1, event_warn_laser_loop, (warn_laser_scheduler,))

# Start the scheduler in a new thread
threading.Thread(target=scheduler.run).start()
threading.Thread(target=warn_laser_scheduler.run).start()

extract_objects()

while True:
    conn, addr = s.accept()
    print("Connect to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
