import pygame
import random

# color definition
menu_color = (100, 203, 240)
bg = (246, 246, 246)
danger = (248, 63, 63)
highlight_color = (225, 245, 99)
info = (62, 114, 255)
rule_color = (57, 233, 177)
snake_color = (72, 227, 139)
stuff_color = (252, 43, 43)


# object definition
class Snake(object):
    def __init__(self, x, y, size):
        self.origx = x
        self.origy = y
        self.x = x
        self.y = y
        self.size = size
        self.body = [[self.x, self.y]]
        self.starting_length = 2
        self.length = self.starting_length

    def draw(self, game_display):
        for pos in self.body:
            rect = [pos[0], pos[1], self.size, self.size]
            pygame.draw.rect(game_display, snake_color, rect)

    def move(self, x, y):
        newx = self.x + x
        newy = self.y + y
        if newx < 0 or newx > window_size[0]:
            return False
        if newy < 0 or newy > window_size[1]:
            return False
        for bodypos in self.body:
            newpos = [newx, newy]
            if newpos == bodypos:
                return False
        self.x = newx
        self.y = newy
        self.body.insert(0, [self.x, self.y])
        self.body = self.body[0:self.length]
        return True

    def lengthen(self):
        self.length += 1

    def get_head_pos(self):
        return self.body[0]

    def reset(self):
        self.length = self.starting_length
        self.x = self.origx
        self.y = self.origy
        self.body = [[self.x, self.y]]


class Stuff(object):
    def __init__(self, window_size, size):
        self.window_size = window_size
        self.size = size

        xrange = self.window_size[0] / self.size
        yrange = self.window_size[1] / self.size

        x = random.randrange(0, xrange)
        y = random.randrange(0, yrange)
        self.pos = [x * self.size, y * self.size]

    def generate(self):
        xrange = self.window_size[0] / self.size
        yrange = self.window_size[1] / self.size

        x = random.randrange(0, xrange)
        y = random.randrange(0, yrange)
        self.pos = [x * self.size, y * self.size]

    def draw(self, game_display):
        rect = [self.pos[0], self.pos[1], self.size, self.size]
        pygame.draw.rect(game_display, stuff_color, rect)

    def get_pos(self):
        return self.pos


# some function
def message(game_display, font, message, location, color, highlight=False):
    text = font.render(message, True, color)
    textpos = text.get_rect()
    textpos.centerx = location[0]
    textpos.centery = location[1]

    if highlight:
        pygame.draw.rect(game_display, highlight_color, textpos)
    game_display.blit(text, textpos)

def get_rule(path):
    data = open(path, 'r')
    rule = []
    for line in data:
        rule.append(line[:-1])
    return rule


# init
status = pygame.init()
if status[1] != 0:
    print("ERROR: fail to init PyGame")
    quit()

# game data
window_size = (800, 600)
FPS = 12
game_display = pygame.display.set_mode(window_size)
block_size = 10
# title
title = 'Snake Eat Stuff'
pygame.display.set_caption(title)

# objects init
snake = Snake(window_size[0] / 2, window_size[1] / 2, block_size)
stuff = Stuff(window_size, block_size)
title_font = pygame.font.Font("./font/Ubuntu-B.ttf", 100)
prompt_font = pygame.font.Font("./font/Ubuntu-B.ttf", 36)
menu_font = pygame.font.Font("./font/Ubuntu-B.ttf", 46)
rule_font = pygame.font.Font("./font/Ubuntu-B.ttf", 30)
direction = 3
moving = False
rule = get_rule("./rule/rule.txt")

# main loop
running = True
mode = 'menu'
clock = pygame.time.Clock()
timing = 0
selected = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if mode == 'menu':
                    if selected > 0:
                        selected -= 1
                elif mode == 'play':
                    if direction != 1:
                        direction = 0
            elif event.key == pygame.K_DOWN:
                if mode == 'menu':
                    if selected < 2:
                        selected += 1
                elif mode == 'play':
                    if direction != 0:
                        direction = 1
            elif event.key == pygame.K_LEFT:
                if direction != 3:
                    direction = 2
            elif event.key == pygame.K_RIGHT:
                if direction != 2:
                    direction = 3
            elif event.key == pygame.K_RETURN:
                timing = 0
                if mode == 'play':
                    moving = True
                elif mode == 'gameover':
                    mode = 'play'
                elif mode == 'menu':
                    if selected == 0:
                        mode = 'play'
                    elif selected == 1:
                        mode = 'rule'
                    elif selected == 2:
                        running = False
                elif mode == 'rule':
                    mode = 'menu'


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
        if snake.get_head_pos() == stuff.get_pos():
            snake.lengthen()
            stuff.generate()

        # drawing
        game_display.fill(bg)
        snake.draw(game_display)
        stuff.draw(game_display)

        if not moving:
            if timing < 10:
                prompt_location = (window_size[0] / 2, window_size[1] / 2 + 120)
                text = "Press enter to start"
                message(game_display, prompt_font, text, prompt_location, info)
                pass
            elif timing < 20:
                pass
            else:
                timing = 0
            timing += 1
    elif mode == 'menu':
        game_display.fill(bg)

        title_location = (window_size[0] / 2, window_size[1] / 2 - 150)
        message(game_display, title_font, title, title_location, danger)

        menu_location = [window_size[0] / 2, window_size[1] / 2 + 90]
        message(game_display, menu_font, "Play", menu_location, menu_color, selected == 0)
        menu_location[1] += 60
        message(game_display, menu_font, "Rule", menu_location, menu_color, selected == 1)
        menu_location[1] += 60
        message(game_display, menu_font, "Exit", menu_location, menu_color, selected == 2)
    elif mode == 'gameover':
        snake.reset()
        stuff.generate()

        game_display.fill(bg)

        game_over_location = (window_size[0] / 2, window_size[1] / 2 - 150)
        message(game_display, title_font, "Game Over", game_over_location, danger)

        if timing < 10:
            prompt_location = (window_size[0] / 2, window_size[1] / 2 + 120)
            message(game_display, prompt_font, "Press enter to continue", prompt_location, info)
            pass
        elif timing < 20:
            pass
        else:
            timing = 0
        timing += 1
    elif mode == 'rule':
        game_display.fill(bg)

        rule_location = [window_size[0] / 2, window_size[1] / 2 - 150]
        message(game_display, title_font, "Rule", rule_location, danger)
        rule_location[1] += 120

        for line in rule:
            message(game_display, rule_font, line, rule_location, rule_color)
            rule_location[1] += 40

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
