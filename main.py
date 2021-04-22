import pygame
import time
import random
from pygame.locals import *

SIZE=40
SCREEN_SIZE = (1000, 600)
BACKGROUND_COLOR = (100, 165, 67)

class Apple:

    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load('resources/apple.jpg').convert()
        self.x = SIZE*3
        self.y = SIZE*3   

    def draw(self):   
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,SCREEN_SIZE[0]//SIZE -1)*SIZE
        self.y = random.randint(1,SCREEN_SIZE[1]//SIZE -1)*SIZE
        #print('(', self.x, self.y, ')')
        self.draw()

class Snake:

    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        #self.heads={i:pygame.image.load('resources/snake_heads/snake_head_'+i+'.jpg').convert() for i in ['up', 'left', 'right', 'down']}
        self.head = pygame.image.load('resources/snake_head2.jpg').convert()
        self.body = pygame.image.load('resources/snake_block.jpg').convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'right'

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        angles = {'up':180, 'down':0, 'right':90, 'left':270}
        self.parent_screen.blit(pygame.transform.rotate(self.head, angles.get(self.direction)), (self.x[0], self.y[0]))
        for i in range(1,self.length):
            self.parent_screen.blit(self.body, (self.x[i], self.y[i]))
        pygame.display.flip() 

    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'
    
    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):
        
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE

        self.draw()
    
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
            

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(SCREEN_SIZE)
        self.render_background()
        pygame.mixer.init()
        self.play_background_music()
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False   

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music.mp3')
        pygame.mixer.music.play()


    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(SCREEN_SIZE[0]-150,10))

    def play_sound(self, sound_file):
        sound = pygame.mixer.Sound(sound_file)
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load('resources/green_background2.jpg')
        self.surface.blit(bg, (0,0))
        #pygame.display.flip()

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("resources/ding.mp3")    
            self.apple.move()
            self.snake.increase_length()
            #print('Collision detected')

        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("resources/crash.mp3")
                raise 'Game Over'


    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"Game is Over .Your Score is: {self.snake.length}",True,(255,0, 0))
        self.surface.blit(line1, (SCREEN_SIZE[0]//2 -150, SCREEN_SIZE[1]//2))
        line2 = font.render(f"To play again, press Enter. To quit, press Escape",True,(255,255, 255))
        self.surface.blit(line2, (SCREEN_SIZE[0]//2 -200, SCREEN_SIZE[1]//2 +50))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN :
                    
                    if event.key == K_ESCAPE:
                        running = False   

                    if event.key == K_RETURN:             
                        pause = False
                        pygame.mixer.music.unpause()
                        self.reset()

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        elif event.key == K_DOWN:
                            self.snake.move_down()

                        elif event.key == K_LEFT:
                            self.snake.move_left()

                        elif event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                

            time.sleep(0.15)
                

if __name__== "__main__":
    
    game = Game()
    game.run()
    
