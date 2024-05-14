import socket
from _thread import *
import sys
import character
import pickle
import character
import main

hostname = socket.gethostname()
ipv4_address = socket.gethostbyname(hostname)
print(f"Internal IPv4 Address for {hostname}: {ipv4_address}")

server = ipv4_address
port = 5555


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")




players = [character.Player(200, 100, 30, 50, 0.5), character.Player(200, 100, 30, 50, 0.5)]
# def read_pos(str):
#     str = str.split(",")
#     return int(str[0]), int(str[1])
#
#
# def make_pos(tup):
#     return str(tup[0]) + "," + str(tup[1])
# players = [character.Player(200, 100, 30, 50, 0.5),character.Player(200, 100, 30, 50, 0.5)]
# pos = [(200,100),(200,100)]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()
currentPlayer = 0
while True:
        conn, addr = s.accept()
        print("Connected to:", addr)
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1


