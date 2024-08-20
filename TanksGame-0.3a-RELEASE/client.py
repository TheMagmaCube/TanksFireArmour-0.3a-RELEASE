# Importowane pliki
import pygame
from sys import exit
from pygame.locals import *
import math
import socket
import time
import threading
import random

enemies = []

clock_socket = pygame.time.Clock()
#Sockets
def information_exchange():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((HOST,PORT))
    global enemies
    print(f'Successfully connected with the server.')
    while True:
        bullets = ''
        for bullet in tank.bullet_list:
            bullets += f"{bullet['bullet_a']},{bullet['position_x_b']},{bullet['position_y_b']},"
        data = f'{tank.position_x_hull}:{tank.position_y_hull}:{tank.hull_angle}:{tank.turett_angle}:{bullets}:{tank.killed}'
        connection.send(data.encode(Transmission_type))
        time.sleep(0.1)
        server_odp = connection.recv(2048).decode(Transmission_type)
        enemies = []
        if server_odp == 'empty':
            continue
        first_list_of_data = server_odp.split('\n')
        for char in first_list_of_data:
            if char == '':
                first_list_of_data.remove(char)
        for char in first_list_of_data:
            player_data = char.split(':')

            for i in range(0,len(player_data), 7):
                id = player_data[i]
                pos_x = float(player_data[i+1])
                pos_y = float(player_data[i+2])
                hull_a = float(player_data[i+3])
                turett_a = float(player_data[i+4])
                bullets = str(player_data[i+5])
                killed = bool(player_data[i+6])


                enemy = {'id':id,
                        'pos_x':pos_x,
                        'pos_y':pos_y,
                        'hull_a':hull_a,
                        'turett_a':turett_a,
                        'bullet_lst': [],
                        'killed': killed}


                if bullets != '':
                    bullets_lst = bullets.split(',')
                    for char in bullets_lst:
                        if char == '':
                            bullets_lst.remove(char)
                    for i in range(0 , len(bullets_lst), 3):
                        bullet = []
                        bullet.append(float(bullets_lst[i]))
                        bullet.append(float(bullets_lst[i+1]))
                        bullet.append(float(bullets_lst[i+2]))
                    

                        enemy['bullet_lst'].append(bullet)

            
            enemies.append(enemy)      
            clock_socket.tick(100)


HOST = 'localhost'
PORT = 49152
Transmission_type = 'utf-8'





# #Pygame ustawiena
pygame.init()
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption('TanksFireArmour-0.3a-RELEASE')
clock = pygame.time.Clock()

#Orginalna textura do obrotu czołgu



#klasa 'Tank'
class Tank:
    def __init__(self):
        self.o_hull = pygame.image.load('assets/textures/tanks_textures/tank_hull.png').convert_alpha()
        self.o_turett = pygame.image.load('assets/textures/tanks_textures/tank_turett.png').convert_alpha()
        self.o_bullet = pygame.image.load('assets/textures/bullet/bullet.png').convert_alpha()
        self.o_hull = pygame.transform.rotate(self.o_hull, -90)
        self.o_turett = pygame.transform.rotate(self.o_turett, -90)
        self.o_bullet = pygame.transform.rotate(self.o_bullet, -90)
        self.hull = self.o_hull
        self.hull_mask = pygame.mask.from_surface(self.hull)
        self.turett = self.o_turett
        self.bullet = self.o_bullet
        self.bullet_list = []
        self.position_x_turett = random.randint(1, 1920)
        self.position_y_turett = random.randint(1, 1080)
        self.position_x_hull = self.position_x_turett
        self.position_y_hull = self.position_y_turett
        self.hull_angle = 0
        self.turett_angle = 0
        self.reload = 0
        self.speed = 3
        self.speed_bullet = 30
        self.hp = 3
        self.killed = False

    def rect(self):
        self.tank_hull_rect = self.hull.get_rect(center = (self.position_x_hull, self.position_y_hull))
        self.tank_turett_rect =  self.turett.get_rect(center = (self.position_x_turett, self.position_y_turett))

    def hull_rotate(self):
        self.hull_rotated = pygame.transform.rotate(tank.o_hull, self.hull_angle)
        self.hull = self.hull_rotated

    def turett_rotate(self):
        self.turett_rotated = pygame.transform.rotate(tank.o_turett, self.turett_angle)
        self.turett = self.turett_rotated

    def movement_front(self):
        self.direction_x = math.cos(math.radians(self.hull_angle)) #cos
        self.direction_y = -math.sin(math.radians(self.hull_angle)) #sin

        self.position_x_hull += self.direction_x * self.speed #x
        self.position_y_hull += self.direction_y * self.speed #y

        self.position_x_turett += self.direction_x * self.speed
        self.position_y_turett += self.direction_y * self.speed


    def movement_back(self):
        self.direction_x = math.cos(math.radians(self.hull_angle)) #cos
        self.direction_y = -math.sin(math.radians(self.hull_angle)) #sin

        self.position_x_hull -= self.direction_x * self.speed #x
        self.position_y_hull -= self.direction_y * self.speed #y

        self.position_x_turett -= self.direction_x * self.speed
        self.position_y_turett -= self.direction_y * self.speed

    def shoot(self):
        if self.reload <= 0:
            self.reload = 200
            bullet_angle = self.turett_angle
            bullet = pygame.transform.rotate(self.o_bullet, bullet_angle)
            bullet_mask = pygame.mask.from_surface(bullet)
            position_x_bullet = self.position_x_turett
            position_y_bullet = self.position_y_turett
            bullet_rect = bullet.get_rect(center = (position_x_bullet,position_y_bullet))
            bullet_dict = {'bullet':bullet, 'bullet_a':bullet_angle, 'position_x_b':position_x_bullet, 'position_y_b':position_y_bullet, 'bullet_rect':bullet_rect,'bullet_mask': bullet_mask}
            self.bullet_list.append(bullet_dict)
        

        
    def after_shoot(self):
        if self.bullet_list != []:
            for bullet in self.bullet_list:
                direction_x_bullet = math.cos(math.radians(bullet['bullet_a'])) #cos
                direction_y_bullet = -math.sin(math.radians(bullet['bullet_a'])) #sin
                bullet['position_x_b'] += direction_x_bullet * self.speed_bullet
                bullet['position_y_b'] += direction_y_bullet * self.speed_bullet
                bullet['bullet_rect'] = bullet['bullet'].get_rect(center = (bullet['position_x_b'],bullet['position_y_b']))

                if bullet['position_x_b'] <= 0:
                    self.bullet_list.remove(bullet)
    
                if bullet['position_x_b'] >= 1920:
                    self.bullet_list.remove(bullet)

                if bullet['position_y_b'] <= 0:
                    self.bullet_list.remove(bullet)

                if bullet['position_y_b'] >= 1015:
                    self.bullet_list.remove(bullet)

    def mouse(self):
        mouse_position = pygame.mouse.get_pos()
        mouse_position_x = mouse_position[0]
        mouse_position_y = mouse_position[1]

        difference_mouse_turett_x = mouse_position_x - self.position_x_turett
        difference_mouse_turett_y = -(mouse_position_y - self.position_y_turett)

        mouse_angle = math.degrees(math.atan2(difference_mouse_turett_y, difference_mouse_turett_x))

        if mouse_angle > self.turett_angle and buttom[2] == False:
            self.turett_angle += 2
            self.turett_rotate()
            self.rect()
        
        if mouse_angle < self.turett_angle and buttom[2] == False:
            self.turett_angle -= 2
            self.turett_rotate()
            self.rect()
            

    def enemies_tank(enemy_tank):
        global enemies
        for enemy in enemies:
            enemy_tank = Tank()
            id = enemy['id']
            enemy_tank.position_x_hull = enemy['pos_x']
            enemy_tank.position_x_turett = enemy_tank.position_x_hull
            enemy_tank.position_y_hull = enemy['pos_y']
            enemy_tank.position_y_turett = enemy_tank.position_y_hull
            enemy_tank.hull_angle = enemy['hull_a']
            enemy_tank.turett_angle = enemy['turett_a']
            enemy_tank.hull_rotate()
            enemy_tank.turett_rotate()
            enemy_tank.rect()
            screen.blit(enemy_tank.hull, enemy_tank.tank_hull_rect)
            screen.blit(enemy_tank.turett, enemy_tank.tank_turett_rect)
            
            try:
                enemy_tank.bullet_list = enemy['bullet_lst']
                for bullet in enemy_tank.bullet_list:
                    print(enemy_tank.bullet_list)
                    bullet_angle = bullet[0]
                    position_x_bullet = bullet[1]
                    position_y_bullet = bullet[2]
                    bullet_texture = pygame.transform.rotate(enemy_tank.o_bullet, bullet_angle)
                    bullet_rect = bullet_texture.get_rect(center = (position_x_bullet, position_y_bullet))
                    screen.blit(bullet_texture,bullet_rect)
            except:
                continue

tank = Tank()
tank.rect()
#tło
map = pygame.surface.Surface((1920, 1080))
map.fill((138, 154, 91))

class Rock:

    global rocks
    rocks = []

    def __init__(self, left = float, top = float, height = int, width = int):
        self.height = height
        self.width = width
        self.left = left
        self.top = top
        rock = pygame.Rect(self.left, self.top, self.height, self.width)
        rocks.append(rock)
    
    
        
    
    def draw(self):
        for rock in rocks:
            pygame.draw.rect(screen, "grey", rock)
        

rock = Rock(100, 100 , 100, 100)
rock = Rock(763, 432 , 100, 100)
rock = Rock(414, 987 , 100, 100)
rock = Rock(123, 432 , 100, 100)
rock = Rock(763, 432 , 100, 100)
rock = Rock(100, 324 , 100, 100)
rock = Rock(200, 100 , 100, 100)
rock = Rock(400, 100 , 100, 100)
rock = Rock(763, 800 , 100, 100)

print('Connecting...')
Thread = threading.Thread(target=information_exchange)
Thread.start()

# #Wyświetlanie obrazu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    tank.hull_rotate()
    tank.turett_rotate()
    

    #Wyświetlanie tekstur i hitboxy
    screen.blit(map, (0,0))
    Rock.draw(self = rocks)
    if tank.bullet_list != []:
        for bullet in tank.bullet_list:
            screen.blit(bullet['bullet'], bullet['bullet_rect'])
    screen.blit(tank.hull,tank.tank_hull_rect)
    screen.blit(tank.turett,tank.tank_turett_rect)

    Tank.enemies_tank(enemy_tank = Tank())

    
    #Sterowanie czołgiem.
    keys = pygame.key.get_pressed()
    buttom = pygame.mouse.get_pressed()
    #Gracz 1


    tank.mouse()
    
    if keys[pygame.K_w]:
        tank.movement_front()
        tank.rect()
        

    if keys[pygame.K_s]:
        tank.movement_back()
        tank.rect()

    if keys[pygame.K_a]:
        if buttom[2] == False:
            tank.turett_angle += 2
        tank.hull_angle += 2
        tank.hull_rotate()
        tank.turett_rotate()
        tank.rect()
        

    if keys[pygame.K_d]:
       if buttom[2] == False:
           tank.turett_angle -= 2
       tank.hull_angle -= 2
       tank.hull_rotate()
       tank.turett_rotate()
       tank.rect()

    if buttom[0] == True:
        tank.shoot()

    tank.reload -= 10
    tank.after_shoot()
    #Granica mapy

    #Gracz 1
    
    if tank.position_x_hull and tank.position_x_turett <= 0:
        tank.position_x_hull += 5
        tank.position_x_turett += 5
    
    if tank.position_x_hull and tank.position_x_turett >= 1920:
        tank.position_x_hull -= 5
        tank.position_x_turett -= 5

    if tank.position_y_hull and tank.position_y_turett <= 0:
        tank.position_y_hull += 5
        tank.position_y_turett += 5

    if tank.position_y_hull and tank.position_y_turett >= 1015:
        tank.position_y_hull -= 5
        tank.position_y_turett -= 5

    #Map rocks

    


    pygame.display.update()
    clock.tick(60)


