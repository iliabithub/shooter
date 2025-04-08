#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

win_width = 700
win_height = 500
win = display.set_mode((win_width,win_height))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'), (win_width,win_height))

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()

font.init() 
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',36)



FPS = 60
clock = time.Clock()

game = True

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        win.blit(self.image, (self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
        print(bullets)

lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


player = Player('rocket.png',350,250,65,65,5)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('asteroid.png',randint(80,520), -40,80,50,randint(2,5)/2)
    monsters.add(monster)
print(monsters)
bullets = sprite.Group()

score = 0

num_fire = 0
rel_time = False

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                       num_fire = num_fire + 1
                       #fire_sound.play()
                       player.fire()

                if num_fire  >= 5 and rel_time == False: #если игрок сделал 5 выстрелов
                       last_time = timer() #засекаем время, когда это произошло
                       rel_time = True #ставим флаг перезарядки
                       print(num_fire)
                
    3
    if rel_time == True:
        cur_time = timer()
        times = cur_time - last_time
        if times < 3:
            reload = font1.render('Wait, reloading...', 1, (150, 0, 0))
            win.blit(reload, (260, 460))
            print('Reload')
            
        else:
            num_fire = 0
            rel_time = False

    win.blit(background,(0,0))
    player.reset()
    player.update()

    text_lose = font1.render(
    'Lost:' + str(lost), 1, (255,255,255)
        )
    
    win.blit(text_lose,(10,10))

    monsters.update()
    monsters.draw(win)
    bullets.update()
    bullets.draw(win)

 
    collides = sprite.groupcollide(monsters, bullets, True, True)
    for c in collides:
     
        score = score + 1
        monster = Enemy('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
        monsters.add(monster)
        


    display.update()
    clock.tick(FPS)