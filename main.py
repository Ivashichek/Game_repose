import pygame
pygame.init()
from random import *

win_width = 800
win_height = 800
tile = 50
FPS: int = 60
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Tanks1941')
bulletimg = pygame.transform.scale(pygame.image.load('img2.png'), (50, 50))
maintank = pygame.transform.scale(pygame.image.load('img2.png'), (50, 50))
maintank_right = pygame.transform.rotate(maintank, -90)
maintank_left = pygame.transform.rotate(maintank, 90)
maintank_down = pygame.transform.rotate(maintank, 180)
Enemy_main = pygame.transform.scale(pygame.image.load('img2.png'), (45, 45))
Enemy_right = pygame.transform.rotate(Enemy_main, -90)
Enemy_left = pygame.transform.rotate(Enemy_main, 90)
Enemy_up = pygame.transform.rotate(Enemy_main, 0)
Enemy_down = pygame.transform.rotate(Enemy_main, 180)

clock = pygame.time.Clock()

damage = 5
speed = 5
orange = (225, 80, 15)
gray = (178, 178, 178)
black = (0, 0, 0)


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, x, y, direction, player_speed, health, damage):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = player_speed
        self.direction = direction
        self.health = health
        self.damage = damage

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player1(GameSprite):
    def update(self):
        selfX, selfY = self.rect.topleft
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_d] and self.rect.x < win_width - 50:
            self.rect.x += self.speed
            self.image = maintank_right
            self.direction = 'right'
        if keyPressed[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.image = maintank_left
            self.direction = 'left'
        if keyPressed[pygame.K_s] and self.rect.y < win_height - 50:
            self.rect.y += self.speed
            self.image = maintank_down
            self.direction = 'down'
        if keyPressed[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
            self.image = maintank
            self.direction = 'up'
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                self.rect.topleft = selfX, selfY

    def shot(self):
        if self.direction == 'right':
            p = Bullet(self.rect.x + 15, self.rect.y + 20, 3, 1, 5, 0)
        elif self.direction == 'left':
            p = Bullet(self.rect.x + 15, self.rect.y + 20, 3, 1, -5, 0)
        elif self.direction == 'up':
            p = Bullet(self.rect.x + 15, self.rect.y + 20, 3, 1, 0, -5)
        else:
            p = Bullet(self.rect.x + 15, self.rect.y + 20, 3, 1, 0, 5)


class Enemy(GameSprite):
    def __init__(self, player_image, x, y, direction, player_speed, health, damage):
        super().__init__(player_image, x, y, direction, player_speed, health, damage)
        self.speedX = 0
        self.speedY = 0
        self.set_direction()

    def set_direction(self):
        b = randint(1, 4)
        if b == 1:
            self.direction = 'right'
            self.image = Enemy_right
            self.speedX = self.speed
            self.speedY = 0
        if b == 2:
            self.direction = 'up'
            self.image = Enemy_up
            self.speedX = 0
            self.speedY = -self.speed
        if b == 3:
            self.direction = 'left'
            self.image = Enemy_left
            self.speedX = -self.speed
            self.speedY = 0
        if b == 4:
            self.direction = 'down'
            self.image = Enemy_down
            self.speedY = self.speed
            self.speedX = 0
    def move(self):
        self.rect.x += self.speedX
        self.rect.y += self.speedY
        # selfX, selfY = self.rect.topleft
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                # self.rect.topleft = selfX, selfY
                if self.direction == 'up':
                    self.rect.top = obj.rect.bottom
                    p = Bullet(self.rect.x + 15, self.rect.y + 20, 3, 1, 0, -5)
                if self.direction == 'down':
                    self.rect.bottom = obj.rect.top
                    p = Bullet(self.rect.x + 15, self.rect.y + 20, 3, 1, 0, 5)
                if self.direction == 'right':
                    self.rect.right = obj.rect.left
                    p = Bullet(self.rect.x + 15, self.rect.y + 20, 3, 1, 5, 0)
                if self.direction == 'left':
                    self.rect.left = obj.rect.right
                    p = Bullet(self.rect.x + 15, self.rect.y + 20, 3, 1, -5, 0)
                self.set_direction()
                break
        if self.rect.x >= win_width - self.rect.width:
            self.rect.right = win_width
            self.set_direction()
        elif self.rect.y >= win_height - self.rect.height:
            self.rect.bottom = win_height
            self.set_direction()
        elif self.rect.x <= 0:
            self.rect.left = 0
            self.set_direction()
        elif self.rect.y <= 0:
            self.rect.top = 0
            # self.rect.topleft = selfX, selfY
            self.set_direction()

class Square(pygame.sprite.Sprite):
    def __init__(self, width, height, color1, color2, color3, health, y, x):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.image.fill((color1, color2, color3))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.health = health

    def refresh(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Block():
    def __init__(self, px, py, size, hp):
        objects.append(self)
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = hp

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(win, orange, self.rect)
        pygame.draw.rect(win, gray, self.rect, 2)


class Bullet():
    def __init__(self, x, y, size, damage, dx, dy):
        bullets.append(self)
        self.damage = damage
        self.dx = dx
        self.dy = dy
        self.rect = pygame.Rect(x, y, size, size)

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.x > win_width or self.rect.y > win_height:
            bullets.remove(self)
            # print('Bullet has been removed')
        elif self.rect.x == -1:
            bullets.remove(self)
            # print('Bullet has been removed')
        elif self.rect.y < -30:
            bullets.remove(self)
            # print('Bullet has been removed')

    def draw(self):
        pygame.draw.circle(win, gray, (self.rect.x, self.rect.y), 2)

    def collide_list(self, objects):
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                obj.hp -= self.damage
                bullets.remove(self)
                if obj.hp <= 0:
                    objects.remove(obj)


Enemy_create = Enemy(maintank, 600, 600, 'up', speed, 10, damage)
maintank_create = Player1(maintank, 10, 0, 'up', speed, 10, damage)
objects = []
bullets = []
for _ in range(50):
    while True:
        x = randint(0, win_width // tile - 1) * tile
        y = randint(0, win_height // tile - 1) * tile
        rect = pygame.Rect(x, y, tile, tile)
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect):
                fined = True
            elif rect.colliderect(maintank_create.rect):
                fined = True
            elif rect.colliderect(Enemy_create.rect):
                fined = True
        if not fined:
            break
    Block(x, y, tile, 1)

game = True
while game:
    win.fill(black)
    for obj in objects:
        obj.draw()
    for bullet in bullets:
        bullet.update()
        bullet.draw()
        bullet.collide_list(objects)
    Enemy_create.reset()
    Enemy_create.update()
    Enemy_create.move()
    maintank_create.reset()
    maintank_create.update()
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                maintank_create.shot()
                # print('Bullet has been arrived:', bullets)
        if e.type == pygame.QUIT:
            game = False
    clock.tick(FPS)
    pygame.display.update()