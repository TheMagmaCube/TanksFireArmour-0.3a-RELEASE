import socket
import threading
from datetime import datetime
import time
import pygame

now = datetime.now()
time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
print(f'[{time_raport}]Server: Starting...')
HOST = 'localhost'
PORT = 49152
transmision_type = 'utf-8'
now = datetime.now()
time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
print(f'[{time_raport}]Server: listening at {HOST}:{PORT}.')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server.bind((HOST,PORT))
server.listen()

#Globals players
counter = 0
players_data = {}

clock_socket = pygame.time.Clock()


class Connection:
    def information_exchange(connection, counter):
        global players_data
        while True:
            try:
                data = connection.recv(2048).decode(transmision_type)
            except Exception as e:
                connection.close()
                now = datetime.now()
                time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
                print(f'[{time_raport}]Server: Lost connection with {address[0]}:{address[1]}.')
                print(f'{e}')
                #player_data[counter] = {}
                break
            if data == '':
                connection.close()
                now = datetime.now()
                time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
                print(f'[{time_raport}]Server: Lost connection with {address[0]}:{address[1]}.')
                #player_data[counter] = {}
                break
            try:
                [pos_x, pos_y, hull_a, turett_a, bullets, killed] = data.split(':')
            except Exception as e:
                connection.close()
                now = datetime.now()
                time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
                print(f'[{time_raport}]Server: Lost connection with {address[0]}:{address[1]}.')
                print(f'{e}')
                #player_data[counter] = {}
                break

            players_data[counter] = {'pos_x': pos_x, 'pos_y': pos_y, 'hull_a': hull_a, 'turett_a': turett_a, 'bullets': bullets,'killed': killed}
            package = ''
            #print(players_data)
            for id in players_data:
                if id == counter:
                    continue
                player_data = players_data[id]
                package += (f"{(id)}:{player_data['pos_x']}:{player_data['pos_y']}:{player_data['hull_a']}:{player_data['turett_a']}:{player_data['bullets']}:{player_data['killed']}\n")

            #print(f'{id}<>{package}')
            if package == '':
                package = 'empty'
            time.sleep(0.1)
            connection.send(package.encode(transmision_type))
            now = datetime.now()
            time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
            #print(f'[{time_raport}]after send package')

            

            clock_socket.tick(150)
        
        

        
        








while True:
    connection, address = server.accept()
    #id = counter
    counter += 1
    #id {'pos_x': }:{tank.position_y_hull}:{tank.hull_angle}:{tank.turett_angle}'}
    now = datetime.now()
    time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f'[{time_raport}]Server: Connected with {address[0]}:{address[1]}.')
    try:
        Thread = threading.Thread(target=Connection.information_exchange,args =(connection, counter))
        Thread.start()
    except Exception as e:
        connection.close()
        now = datetime.now()
        time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f'[{time_raport}]Server: Lost connection with {address[0]}:{address[1]}.')
        print(f'{e}')
