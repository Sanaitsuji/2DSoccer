import os, sys, pygame
from random import randint

class Pad(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((12, 30)).convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.max_speed = 10
        self.speed = 0

    def move_up(self):
        self.speed = self.max_speed * -1

    def move_down(self):
        self.speed = self.max_speed * 1

    def stop(self):
        self.speed = 0

    def update(self):
        self.rect.move_ip(0, self.speed)

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = pygame.Surface((10, 10)).convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed_x = 0
        self.speed_y = 0

    def change_y(self):
        self.speed_y *= -1

    def change_x(self):
        self.speed_x *= -1

    def start(self, speed_x, speed_y,signo):
        self.speed_x = speed_x * signo
        self.speed_y = speed_x * signo

    def stop(self):
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.rect.move_ip(self.speed_x, self.speed_y)

    def reset(self):
        self.rect = self.image.get_rect(center=self.pos)


class Score(pygame.sprite.Sprite):
    def __init__(self, font, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.pos = pos
        self.score = 0
        self.image = self.font.render(str(self.score), 0, (255, 255, 255))
        self.rect = self.image.get_rect(center=self.pos)

    def score_up(self):
        self.score += 1

    def update(self):
        self.image = self.font.render(str(self.score), 0, (255, 255, 255))
        self.rect = self.image.get_rect(center=self.pos)

def main():
    pygame.init()

    size = width, height = 700, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Pong Pygame')

    try:
        filename = os.path.join(
            os.path.dirname(__file__),
            'assets',
            'graphics',
            'Canchita.png')
        background = pygame.image.load(filename)
        background = background.convert()
    except pygame.error as e:
        print ('Cannot load image: ', filename)
        raise SystemExit(str(e))

    pad_left = Pad((width/6, height/4))
    pad_right = Pad((5*width/6, 3*height/4))

    ball = Ball((width/2, height/2))

    if not pygame.font:
        raise SystemExit('Pygame does not support fonts')

    try:
        filename = os.path.join(
            os.path.dirname(__file__),
            'assets',
            'fonts',
            'wendy.ttf')
        font = pygame.font.Font(filename, 90)
    except pygame.error as e:
        print ('Cannot load font: ', filename)
        raise SystemExit(str(e))

    left_score = Score(font, (width/3, height/8))
    right_score = Score(font, (2*width/3, height/8))

    sprites = pygame.sprite.Group(pad_left, pad_right, ball, left_score, right_score)

    clock = pygame.time.Clock()
    fps = 60

    pygame.key.set_repeat(1, int(1000/fps))
    
    cont = 0

    top = pygame.Rect(0, 0, width, 5)
    bottom = pygame.Rect(0, height-5, width, 5)
    cornerLeftTop = pygame.Rect(0, 0, 5, 170)
    cornerRightTop = pygame.Rect(width-5, 0, 5, 170)
    cornerLeftBottom = pygame.Rect(0, 330, 5, height)
    cornerRightBottom = pygame.Rect(width-5, 330, 5, height)
    left = pygame.Rect(0, 170, 50, 160)
    right = pygame.Rect(width-50, 170, 50, 160)
    postLeftTop = pygame.Rect(0, 165, 50, 5)
    postRightTop = pygame.Rect(width-50, 165, 50, 5)
    postLeftBottom = pygame.Rect(0, 330, 50, 5)
    postRightBottom = pygame.Rect(width-50, 330, 50, 5)

    velIni = 3
    contColl = 0

    padOrien = True

    while 1:
        clock.tick(fps)

        pad_left.stop()
        pad_right.stop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and cont == 0:
                cont = 1
                valRan = randint(1, 2)
                if valRan == 1:
                    signo = -1
                else:
                    signo = 1

                ball.start(velIni, velIni,signo)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                pad_left.rect.move_ip(0, -10)
            elif keys[pygame.K_s]:
                pad_left.rect.move_ip(0, 10)
            elif keys[pygame.K_a]:
                pad_left.rect.move_ip(-10, 0)
            elif keys[pygame.K_d]:
                pad_left.rect.move_ip(10, 0)
    
            if keys[pygame.K_UP]:
                pad_right.move_up()
            elif keys[pygame.K_DOWN]:
                pad_right.move_down()

        if ball.rect.colliderect(top) or ball.rect.colliderect(bottom) or ball.rect.colliderect(postLeftTop) or ball.rect.colliderect(postRightTop) or ball.rect.colliderect(postLeftBottom) or ball.rect.colliderect(postRightBottom):
            ball.change_y()
        elif ball.rect.colliderect(cornerLeftTop) or ball.rect.colliderect(cornerRightTop) or ball.rect.colliderect(cornerLeftBottom) or ball.rect.colliderect(cornerRightBottom):
            ball.change_x()
        elif ball.rect.colliderect(pad_left.rect) or ball.rect.colliderect(pad_right.rect):
            ball.change_x()
            contColl = contColl + 1
            if contColl == 10:
                 velIni = velIni + 1

        """pad_left.rect.move_ip(screen_rect)
        pad_right.rect.move_ip(screen_rect)"""

        if ball.rect.colliderect(left):
            right_score.score_up()
            ball.reset()
            ball.stop()
            cont = 0
        elif ball.rect.colliderect(right):
            left_score.score_up()
            ball.reset()
            ball.stop()
            cont = 0

        sprites.update()

        screen.blit(background, (0, 0))
        sprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
