
from pygame import *
display.set_caption('игрулька')
window = display.set_mode((700,500))
background = transform.scale(image.load('galaxy_2.jpg'),(700,500))
win_height=500
win_width=700
monsters = sprite.Group()
bullets = sprite.Group()
# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))


        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
wall_1 = GameSprite('black1.png',80,180,200,250)



class Player(GameSprite):
    # метод, в котором реализовано управление спрайтом по кнопкам стрелочкам клавиатуры
    def __init__(
        self,
        player_image,
        player_x,
        player_y,
        size_x,
        size_y,
        player_x_speed,
        player_y_speed,
    ):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(
            self, player_image, player_x, player_y, size_x, size_y
        )


        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        """перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость"""
        # сначала движение по горизонтали
        if (
            packman.rect.x <= win_width - 80
            and packman.x_speed > 0
            or packman.rect.x >= 0
            and packman.x_speed < 0
        ):
            self.rect.x += self.x_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if (
            self.x_speed > 0
        ):  # идём направо, правый край персонажа - вплотную к левому краю стены
            for p in platforms_touched:
                self.rect.right = min(
                    self.rect.right, p.rect.left
                )  # если коснулись сразу нескольких, то правый край - минимальный из возможных
        elif (
            self.x_speed < 0
        ):  # идем налево, ставим левый край персонажа вплотную к правому краю стены
            for p in platforms_touched:
                self.rect.left = max(
                    self.rect.left, p.rect.right
                )  # если коснулись нескольких стен, то левый край - максимальный
        if (
            packman.rect.y <= win_height - 80
            and packman.y_speed > 0
            or packman.rect.y >= 0
            and packman.y_speed < 0
        ):
            self.rect.y += self.y_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:  # идем вниз
            for p in platforms_touched:
                # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:  # идём вверх
            for p in platforms_touched:
                self.rect.top = max(
                    self.rect.top, p.rect.bottom
                )  
    def fire(self):
        bullet = Bullet("pif.png", self.rect.right, self.rect.centery, 25, 30, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    side = "left"

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    # движение врага
    def update(self):
        if self.rect.x <= 420:  # w1.wall_x + w1.wall_width
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    # движение врага
    def update(self):
        self.rect.x += self.speed
        # исчезает, если дойдёт до края экрана
        if self.rect.x > win_width + 10:
            self.kill()

w1 = GameSprite(
 'black1.png', 150, 200, 300, 50
)
w2 = GameSprite('black1.png', 400, 150, 50, 400)
# создаем спрайты
packman = Player('nlo1.png', 5, win_height - 80, 80, 80, 0, 0)
# игровой цикл
fin = GameSprite('bh.png',win_width - 85, win_height - 100, 80, 80)
enemy = Enemy('astr.png',win_width - 80, 180, 70,70,5)
barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)
monsters.add(enemy)
run = True
finish = False
while run:
    # цикл срабатывает каждую 0.05 секунд
    time.delay(50)
    window.blit(background,(0,0))  # закрашиваем окно цветом


    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
    # рисуем объекты
    w1.reset()
    w2.reset()
    packman.reset()
    fin.reset()
    monsters.update()
    monsters.draw(window)
    sprite.groupcollide(monsters, bullets, True, True)
    sprite.groupcollide(bullets, barriers, True, False)
    bullets.draw(window)
    bullets.update()
    if sprite.collide_rect(packman, enemy):
            finish = True
            # вычисляем отношение
            img = image.load("gg.jpg")
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(
                transform.scale(img, (win_height * d, win_height)), (90, 0)
            )
    if sprite.collide_rect(packman, fin):
            finish = True
            img = image.load("yw.jpg")
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))



    # включаем движение
    packman.update()


    display.update()


