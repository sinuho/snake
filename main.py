import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (92, 25, 62)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()

        self.length = 1
        self.x = [SIZE] * self.length
        self.y = [SIZE] * self.length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


    def draw(self):
        self.parent_screen.fill((92, 25, 62))  # clear screen
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        #self.y -= 10
        #self.draw()
        self.direction = 'up'

    def move_down(self):
        #self.y += 10
        #self.draw()
        self.direction = 'down'

    def move_left(self):
        #self.x -= 10
        #self.draw()
        self.direction = 'left'

    def move_right(self):
        #self.x += 10
        #self.draw()
        self.direction = 'right'

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
             self.x[0] += SIZE
        self.draw()




class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake v1.0")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill((92, 25, 62))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):

        pygame.mixer.music.load("resources/output.ogg")
        pygame.mixer.music.play()

    def play_sound(self, sound_name):
        if sound_name == 'ding':
            sound = pygame.mixer.Sound('resources/ding.ogg')
        elif sound_name == 'crash':
            sound = pygame.mixer.Sound('resources/crash.ogg')

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def collision(self, x_snake, y_snake, x_apple, y_apple):
        if x_snake >= x_apple and x_snake < x_apple + SIZE:
            if y_snake >= y_apple and y_snake < y_apple + SIZE:
                return True
        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake collidning with apple
        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.play_sound('ding')
            self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occured"

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over: your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"Enter to start again", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - 1}", True, (200, 200, 200))
        self.surface.blit(score, (800, 50))

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            #self.play( )
            time.sleep(.25)

if __name__ == "__main__":
    game = Game()
    game.run()

    # block_x = 100
    # block_y = 100

    # block_x, block_y = 100, 100


