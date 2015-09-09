import pygame

# color definition
bg = (246, 246, 246)
danger = (248, 63, 63)
info = (62, 114, 255)
snake_color = (72, 227, 139)


# object definition
class Snake(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.body = [[self.x, self.y]]
        self.length = 2

    def draw(self, game_display):
        for pos in self.body:
            rect = [pos[0], pos[1], self.size, self.size]
            pygame.draw.rect(game_display, snake_color, rect)

    def move(self, x, y):
        if self.x + x < 0 or self.x + x > window_size[0]:
            return False
        if self.y + y < 0 or self.y + y > window_size[1]:
            return False
        self.x += x
        self.y += y
        self.body.insert(0, [self.x, self.y])
        self.body = self.body[0:self.length]
        return True

    def lengthen(self):
        self.length += 1



# some function
def message(game_display, font, message, location, color):
    text = font.render(message, True, color)
    textpos = text.get_rect()
    textpos.centerx = location[0]
    textpos.centery = location[1]
    game_display.blit(text, textpos)





# init
status = pygame.init()
if status[1] != 0:
    print("ERROR: fail to init PyGame")
    quit()

# game data
window_size = (800, 600)
FPS = 15
game_display = pygame.display.set_mode(window_size)
block_size = 10
# title
pygame.display.set_caption('Snake Eat Stuff')

# objects init
snake = Snake(window_size[0] / 2, window_size[1] / 2, block_size)
game_over_font = pygame.font.Font("./font/Ubuntu-B.ttf", 106)
prompt_font = pygame.font.Font("./font/Ubuntu-B.ttf", 36)
direction = 3
moving = False

# main loop
running = True
mode = 'gameover'
clock = pygame.time.Clock()
timing = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if direction != 1:
                    direction = 0
            elif event.key == pygame.K_DOWN:
                if direction != 0:
                    direction = 1
            elif event.key == pygame.K_LEFT:
                if direction != 3:
                    direction = 2
            elif event.key == pygame.K_RIGHT:
                if direction != 2:
                    direction = 3
            elif event.key == pygame.K_RETURN:
                if mode == 'play':
                    moving = True
                elif mode == 'gameover':
                    mode = 'play'


    if mode == 'play':
        move_success = True
        # move the snake
        if moving:
            if direction == 0:
                move_success = snake.move(0, -block_size)
            elif direction == 1:
                move_success = snake.move(0, block_size)
            elif direction == 2:
                move_success = snake.move(-block_size, 0)
            elif direction == 3:
                move_success = snake.move(block_size, 0)

        # update data
        if not move_success:
            mode = 'gameover'

        # drawing
        game_display.fill(bg)
        snake.draw(game_display)
    elif mode == 'menu':
        game_display.fill(bg)
    elif mode == 'gameover':
        game_display.fill(bg)

        game_over_location = (window_size[0] / 2, window_size[1] / 2 - 100)
        message(game_display, game_over_font, "Game Over", game_over_location, danger)

        if timing < 10:
            prompt_location = (window_size[0] / 2, window_size[1] / 2 + 120)
            message(game_display, prompt_font, "Press enter to continue", prompt_location, info)
            pass
        elif timing < 20:
            pass
        else:
            timing = 0
        timing += 1


    # update the screen
    pygame.display.update()

    # FPS control
    clock.tick(FPS)


# exit
pygame.quit()
quit()
