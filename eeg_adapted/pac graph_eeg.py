import os
import random
import pygame
import time
from breadth_first_search import bfs
from random_within_vicinity import rand
from client import thought

class Enemy(object):
    def __init__(self, typ):
        self.rect = pygame.Rect(16*(9+typ), 16*13, 16, 16)

    def set_path(self, bx, by, ex, ey, level, typ, key=[], ax=0, ay=0):
        if typ == 0:
            return bfs(bx, by, ex, ey, level)
        elif typ == 1:
            return rand(bx, by, ex, ey, level)
        elif typ == 2 or typ == 3:
            direct='n'
            movement=0
            if thought=="left":
                direct = 'x'
                movement = -1
            if thought=="right":
                direct = 'x'
                movement = 1
            if thought=="lift":
                direct = 'y'
                movement = -1
            if thought=="drop":
                direct = 'y'
                movement = 1
            ahead_count = 0
            x=ex
            y=ey
            while ahead_count<=5:
                ahead_count+=1
                if direct=='x':
                    if x+movement>=0 and x+movement<21 and level[y][x+movement]!='W':
                        x+=movement
                    else:
                        break
                if direct=='y':
                    if y+movement>=0 and y+movement<26 and level[y+movement][x]!='W':
                        y+=movement
                    else:
                        break
            if typ == 2:
                return bfs(bx, by, x, y, level)
            if typ == 3:
                pos_x = 2*ax - x
                pos_y = 2*ay - y
                if pos_x < 0:
                    pos_x = 0
                elif pos_x > 21:
                    pos_x = 20
                if pos_y < 0:
                    pos_y = 0
                elif pos_y > 26:
                    pos_y = 25
                while level[pos_y][pos_x]!='W':
                    if pos_x-1 < 0 and level[pos_y][pos_x-1]!='W':
                        pos_x -= 1
                    elif pos_x+1 > 21 and level[pos_y][pos_x+1]!='W':
                        pos_x += 1
                    elif pos_y-1 < 0 and level[pos_y-1][pos_x]!='W':
                        pos_y -= 1
                    elif pos_y+1 > 25 and level[pos_y+1][pos_x]!='W':
                        pos_y += 1
                    if level[pos_y][pos_x]!='W':
                        break
                return bfs(bx, by, pos_x, pos_y, level)
            
    def move(self, path):
        if path!=[]:
            direct, dist = path.pop()
            if direct == 'x':
                self.rect.x += dist*2
            if direct == 'y':
                self.rect.y += dist*2
            if self.rect.x < 0:
                self.rect.x = 16*20
            elif self.rect.x > 16*21:
                self.rect.x = 0

            if self.rect.y < 0:
                self.rect.y = 16*25
            elif self.rect.y > 16*26:
                self.rect.y = 0

            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if direct=="x" and dist > 0: 
                        self.rect.right = wall.rect.left
                    if direct=="x" and dist < 0: 
                        self.rect.left = wall.rect.right
                    if direct=="y" and dist > 0: 
                        self.rect.bottom = wall.rect.top
                    if direct=="y" and dist < 0: 
                        self.rect.top = wall.rect.bottom
    
class Player(object):
    
    def __init__(self):
        self.rect = pygame.Rect(16*11, 16*16, 16, 16)

    def move(self, dx, dy, level, prev_dx, prev_dy):
        global move_count
        move_count=move_count+1
        change_check = True

        if dx == prev_dx and dy == prev_dy:
            self.move_single_axis(dx, 0)
            self.move_single_axis(0, dy)
        elif dx!=0 and level[self.rect.y//16][self.rect.x//16+dx]!='W':
                self.move_single_axis(dx, 0)
        elif dy!=0 and level[self.rect.y//16+dy][self.rect.x//16]!='W':
                self.move_single_axis(0, dy)
        else:
            self.move_single_axis(prev_dx, 0)
            self.move_single_axis(0, prev_dy)
            change_check = False
        
        return (dx, dy, change_check)
    
    def move_single_axis(self, dx, dy):
        
        self.rect.x += dx*2.05
        self.rect.y += dy*2.05

        if self.rect.x < 0:
            self.rect.x = 16*21
        elif self.rect.x > 16*21:
            self.rect.x = 0

        if self.rect.y < 0:
            self.rect.y = 16*26
        elif self.rect.y > 16*26:
            self.rect.y = 0

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0: 
                    self.rect.left = wall.rect.right
                if dy > 0: 
                    self.rect.bottom = wall.rect.top
                if dy < 0: 
                    self.rect.top = wall.rect.bottom

class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

class Point(object):

    def __init__(self, pos):
        points.append(self)
        point_is_visible.append(True)
        self.rect = pygame.Rect(pos[0]+8, pos[1]+8, 4, 4)

class Cherry(object):

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 16, 16)

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
pygame.font.init()

pygame.display.set_caption("Pac Graph")
screen = pygame.display.set_mode((22*16, 30*16))

clock = pygame.time.Clock()
walls = []
points = []
point_is_visible = []
player = Player()
enemy = [Enemy(0), Enemy(3), Enemy(1), Enemy(2)]
path = []
path1 = []
path2 = []
path3 = []
move_count = 9
score = 0
add_score = 0
BLUE = (0, 60, 130)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 200, 0)
font = pygame.font.SysFont("Ariel Black", 24)
title_font = pygame.font.SysFont("Ariel Black", 48)
small_font = pygame.font.SysFont("Ariel Black", 18)
lives = 3
sprite_keys = ["player", "left", "right", "up", "down"]
enemy_sprite = pygame.transform.scale(pygame.image.load("img/bfs_enemy.png"), (16, 16)).convert_alpha()
enemy1_sprite = pygame.transform.scale(pygame.image.load("img/rnd_enemy.png"), (16, 16)).convert_alpha()
enemy2_sprite = pygame.transform.scale(pygame.image.load("img/cut_enemy.png"), (16, 16)).convert_alpha()
enemy3_sprite = pygame.transform.scale(pygame.image.load("img/rft_enemy.png"), (16, 16)).convert_alpha()
life_sprite = pygame.transform.scale(pygame.image.load("img/player.png"), (16, 16)).convert_alpha()
display_sprite = pygame.transform.scale(pygame.image.load("img/right.png"), (16, 16)).convert_alpha()
cherry_sprite = pygame.transform.scale(pygame.image.load("img/fruit.png"), (16, 16)).convert_alpha()
spr_index = 0
points_total = 0
prev_key = []
prev_spr = life_sprite
prev_dx, prev_dy = 0, 0
pygame.mixer.music.load('audio/menu_song.mp3')
pygame.mixer.music.play(0)
start_flag = False
end_flag = False
cherry_pos = []
cherry_timer = 0
effect = pygame.mixer.Sound('audio/bite.wav')

level = [
"WWWWWWWWWWXXWWWWWWWWWW",
"W                    W",
"W WWWWWWWWWWWWWWWWWW W",
"W W                W W",
"W W WWWWWW  WWWWWW W W",
"W W      W  W      W W",
"W W WWWW W  W WWWW W W",
"W W    W W  W W    W W",
"W WWWW W      W WWWW W",
"W      W WWWW W      W",
"W WWWWWW      WWWWWW W",
"W W      WXXW      W W",
"W WWWWW WWXXWW WWWWW W",
"X       WXXXXW       X",
"W WWWWW WWWWWW WWWWW W",
"W W                W W",
"W WWWWWW   X  WWWWWW W",
"W      W WWWW W      W",
"W WWWW W      W WWWW W",
"W W    W W  W W    W W",
"W W WWWW W  W WWWW W W",
"W W      W  W      W W",
"W W WWWWWW  WWWWWW W W",
"W W                W W",
"W WWWWWWWWWWWWWWWWWW W",
"W                    W",
"WWWWWWWWWWXXWWWWWWWWWW",
]

x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        elif col == " ":
            Point((x, y))
            points_total += 1
            cherry_pos.append((x, y))
        x += 16
    y += 16
    x = 0

exit_flag = False

while not exit_flag:

    if start_flag:
        
        clock.tick(60)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit_flag = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                exit_flag = True
                
        player_sprite = pygame.transform.scale(pygame.image.load("img/"+sprite_keys[spr_index]+".png"), (16, 16)).convert_alpha()

        if cherry_timer==0 and score>=1000:
            cherry_rand = random.randint(0, len(cherry_pos)*1200)
            if cherry_rand < len(cherry_pos) and not point_is_visible[cherry_rand]:
                cherry = Cherry(cherry_pos[cherry_rand][0], cherry_pos[cherry_rand][1])
                cherry_timer = 7*60
        elif cherry_timer>0 and score>=1000:
            cherry_timer-=1                    
                
        key = pygame.key.get_pressed()
        
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT] and not key[pygame.K_UP] and not key[pygame.K_DOWN] and prev_key!=[]:
            key = prev_key
        if key!=prev_key:
            if player.rect.x%16<16-player.rect.x%16:
                player.rect.x -= player.rect.x%16
            else:
                player.rect.x += 16-player.rect.x%16
            if player.rect.y%16<16-player.rect.y%16:
                player.rect.y -= player.rect.y%16
            else:
                player.rect.y += 16-player.rect.y%16
            prev_key = key
            
        if thought=="left":
            if player.move(-1, 0, level, prev_dx, prev_dy)[2]:
                prev_dx = -1
                prev_dy = 0
                spr_index = 1
        elif thought=="right":
            if player.move(1, 0, level, prev_dx, prev_dy)[2]:
                prev_dx = 1
                prev_dy = 0
                spr_index = 2
        elif thought=="lift":
            if player.move(0, -1, level, prev_dx, prev_dy)[2]:
                prev_dx = 0
                prev_dy = -1
                spr_index = 3
        elif thought=="drop":
            if player.move(0, 1, level, prev_dx, prev_dy)[2]:
                prev_dx = 0
                prev_dy = 1
                spr_index = 4

        if path == []:
            path = enemy[0].set_path(enemy[0].rect.x//16, enemy[0].rect.y//16, player.rect.x//16, player.rect.y//16, level, 0)
        if path1 == []:
            path1 = enemy[1].set_path(enemy[1].rect.x//16, enemy[1].rect.y//16, player.rect.x//16, player.rect.y//16, level, 1)
        if path2 == []:
            path2 = enemy[2].set_path(enemy[2].rect.x//16, enemy[2].rect.y//16, player.rect.x//16, player.rect.y//16, level, 2, prev_key)
        if path3 == []:
            path3 = enemy[3].set_path(enemy[3].rect.x//16, enemy[3].rect.y//16, player.rect.x//16, player.rect.y//16, level, 3, prev_key, enemy[0].rect.x//16, enemy[0].rect.y//16)
        enemy[0].move(path)
        enemy[1].move(path1)
        enemy[2].move(path2)
        enemy[3].move(path3)

        collision_check = False
              
        for i in range(4):
            if player.rect.colliderect(enemy[i].rect):
                if not collision_check:
                    lives -= 1
                    collision_check = True
                if lives>0:
                    player.rect.x = 16*11
                    player.rect.y = 16*16
                    enemy[0].rect.x = 16*9
                    enemy[0].rect.y = 16*13
                    enemy[1].rect.x = 16*12
                    enemy[1].rect.y = 16*13
                    enemy[2].rect.x = 16*10
                    enemy[2].rect.y = 16*13
                    enemy[3].rect.x = 16*11
                    enemy[3].rect.y = 16*13
                    pygame.mixer.music.play(-1)
                    time.sleep(2)
                elif not end_flag:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('audio/end_song.mp3')
                    pygame.mixer.music.play(0)
                    time.sleep(2)
                    end_flag = True

        for p in range(len(points)):
            if player.rect.colliderect(points[p].rect):
                if point_is_visible[p]:
                    score+=10
                    point_is_visible[p] = False
                    effect.play()
                    
        if cherry_timer > 0 and player.rect.colliderect(cherry.rect):
            add_score+=1000
            cherry_timer=0
        if score==points_total*10 and not end_flag:
                pygame.mixer.music.stop()
                pygame.mixer.music.load('audio/end_song.mp3')
                pygame.mixer.music.play(0)
                time.sleep(2)
                end_flag = True
    else:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit_flag = True
            if e.type == pygame.KEYDOWN:
                start_flag = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load('audio/soundtrack.mp3')
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)
                time.sleep(2)
        
    screen.fill(BLACK)
    for wall in walls:
        pygame.draw.rect(screen, BLUE, wall.rect)
    for point in range(len(points)):
        if point_is_visible[point]:
            pygame.draw.ellipse(screen, WHITE, points[point].rect, 0)
            
    if start_flag:
        if lives <= 0:
            game_over = title_font.render("GAME OVER", 5, WHITE)
            text = font.render("SCORE: "+str(score+add_score), 5, WHITE)
            text2 = font.render("LIVES: "+str(lives), 5, WHITE)
            pygame.draw.rect(screen, BLACK, (16, 16, 16*20, 16*25))
            screen.blit(game_over, (16*4.5, 16*10))
            screen.blit(text, (16*8, 16*14))
            screen.blit(text2, (16*8.5, 16*16))
            pygame.display.flip()
            pygame.time.delay(4)
            while not exit_flag:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        exit_flag = True
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                        exit_flag = True
        elif score==points_total*10:
            game_over = title_font.render("YOU WIN", 5, WHITE)
            text = font.render("SCORE: "+str(score+add_score), 5, WHITE)
            text2 = font.render("LIVES: "+str(lives), 5, WHITE)
            pygame.draw.rect(screen, BLACK, (16, 16, 16*20, 16*25))
            screen.blit(game_over, (16*6, 16*10))
            screen.blit(text, (16*8, 16*14))
            screen.blit(text2, (16*8.5, 16*16))
            pygame.display.flip()
            pygame.time.delay(4)
            while not exit_flag:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        exit_flag = True
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                        exit_flag = True
        else:
            screen.blit(enemy_sprite, (enemy[0].rect[0], enemy[0].rect[1]))
            screen.blit(enemy1_sprite, (enemy[1].rect[0], enemy[1].rect[1]))
            screen.blit(enemy2_sprite, (enemy[2].rect[0], enemy[2].rect[1]))
            screen.blit(enemy3_sprite, (enemy[3].rect[0], enemy[3].rect[1]))
            if move_count%8==0:
                prev_spr = player_sprite
            elif move_count%4==0:
                prev_spr = life_sprite
            if cherry_timer > 0:
                screen.blit(cherry_sprite, (cherry.rect[0], cherry.rect[1]))
            screen.blit(prev_spr, (player.rect[0], player.rect[1]))
            text = font.render("SCORE: "+str(score+add_score), 5, WHITE)
            text2 = font.render("LIVES: ", 5, WHITE)
            screen.blit(text, (16, 16*28))
            screen.blit(text2, (16*13, 16*28))
            for l in range(lives):
                screen.blit(display_sprite, (16*17+l*16*1.5, 16*28))
    else:
        game_start = title_font.render("PAC GRAPH", 5, YELLOW)
        text = font.render("[PRESS ANY KEY TO BEGIN]", 5, WHITE)
        text2 = small_font.render("Created by Kevin Junyang Cui 2019", 5, WHITE)
        pygame.draw.rect(screen, BLACK, (16, 16, 16*20, 16*25))
        screen.blit(game_start, (16*4.5, 16*10))
        screen.blit(text, (16*4, 16*14))
        screen.blit(display_sprite, (16*6, 16*18))
        screen.blit(enemy_sprite, (16*8, 16*18))
        screen.blit(enemy1_sprite, (16*14, 16*18))
        screen.blit(enemy2_sprite, (16*10, 16*18))
        screen.blit(enemy3_sprite, (16*12, 16*18))
        screen.blit(text2, (16*4.5, 16*28))
    pygame.display.flip()
    pygame.time.delay(4)

pygame.quit()

           
