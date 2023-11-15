import pygame
from random import randint
from time import time
from Button import Button
from Menu import new_loop as go_menu


def create_food():
    global foods, snake
    position = foods[0]
    timeout = time() + 1
    while position in foods:
        if time() > timeout:
            break
        position = (randint(RADIUS, WINDOW_WIDTH - RADIUS), randint(RADIUS, WINDOW_HEIGHT - RADIUS))
        position = (position[0] - position[0] % DIAMETER + RADIUS,
                    position[1] - position[1] % DIAMETER + RADIUS)
        if position in snake:
            break
    else:
        foods.append(position)


def new_loop(window_size, difficult, increase_food_time, can_crash_wall, can_crash_self):
    global WINDOW_WIDTH, WINDOW_HEIGHT, HALF_WINDOW_WIDTH, HALF_WINDOW_HEIGHT, INCREASE_SPEED_FOOD, GAP, END_X, END_Y, \
        CAN_CRASH_WALL, CAN_CRASH_SELF, WINDOW_CENTRE_X, WINDOW_CENTRE_Y
    global WINDOW_COLOR, TEXT_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR, ACTIVATED_BUTTON_COLOR, GAME_OVER_TEXT_COLOR, \
        SNAKE_COLOR, EYE_COLOR, FOOD_COLOR
    global FPS, SPEED, SPEED_FOOD, RADIUS, DIAMETER, RADIUS_FOOD, DIRECTIONS, BUTTON_WIDTH, BUTTON_HEIGHT, best_score

    with open('Settings') as settings, open('Colors') as colors, open('Score') as best_score:
        best_score = int(best_score.readline().split()[0])
        data = [int(settings.readline().split()[0]) for _ in range(3)]
        colors = [colors.readline().split()[0] for _ in range(9)]

    SPEED, DIFFERENCE_SPEED, SPEED_FOOD = data
    WINDOW_COLOR, TEXT_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR, ACTIVATED_BUTTON_COLOR, GAME_OVER_TEXT_COLOR, \
     SNAKE_COLOR, EYE_COLOR, FOOD_COLOR = colors

    WINDOW_WIDTH, WINDOW_HEIGHT = window_size
    HALF_WINDOW_WIDTH = WINDOW_WIDTH // 2
    HALF_WINDOW_HEIGHT = WINDOW_HEIGHT // 2
    GAP = (WINDOW_WIDTH + WINDOW_HEIGHT) // 200
    INCREASE_SPEED_FOOD = increase_food_time
    CAN_CRASH_WALL = can_crash_wall
    CAN_CRASH_SELF = can_crash_self

    FPS = 60
    SPEED -= (difficult * DIFFERENCE_SPEED)
    RADIUS = (WINDOW_WIDTH + WINDOW_HEIGHT) // 100
    DIAMETER = RADIUS * 2
    RADIUS_FOOD = RADIUS // 2
    BUTTON_WIDTH = WINDOW_WIDTH // 5
    BUTTON_HEIGHT = WINDOW_HEIGHT // 10

    WINDOW_CENTRE_X = HALF_WINDOW_WIDTH - HALF_WINDOW_WIDTH % DIAMETER + RADIUS
    WINDOW_CENTRE_Y = HALF_WINDOW_HEIGHT - HALF_WINDOW_HEIGHT % DIAMETER + RADIUS
    END_X = WINDOW_WIDTH - (WINDOW_WIDTH - RADIUS) % DIAMETER
    END_Y = WINDOW_HEIGHT - (WINDOW_HEIGHT - RADIUS) % DIAMETER

    DIRECTIONS = {
        (pygame.K_w, pygame.K_UP): (1, 1, (0, -1)),
        (pygame.K_a, pygame.K_LEFT): (0, 1, (-1, 0)),
        (pygame.K_s, pygame.K_DOWN): (1, -1, (0, 1)),
        (pygame.K_d, pygame.K_RIGHT): (0, -1, (1, 0))
    }

    Button.width_class = BUTTON_WIDTH
    Button.height_class = BUTTON_HEIGHT
    Button.gap_class = GAP
    Button.color_class = BUTTON_COLOR
    Button.activated_color_class = ACTIVATED_BUTTON_COLOR

    new_game()


def continue_function():
    global is_pause
    is_pause = False


def new_game():
    pygame.display.set_caption('Snake game')
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    FONT = pygame.font.SysFont('Verdana', (WINDOW_WIDTH + WINDOW_HEIGHT) // 100)

    BUTTONS_DATA = (
        (HALF_WINDOW_WIDTH - (BUTTON_WIDTH + GAP) // 2, HALF_WINDOW_HEIGHT, new_game, 'Заново'),
        (HALF_WINDOW_WIDTH + (BUTTON_WIDTH + GAP) // 2, HALF_WINDOW_HEIGHT, go_menu, 'Меню'),
        (HALF_WINDOW_WIDTH, HALF_WINDOW_HEIGHT - (BUTTON_HEIGHT + GAP) * 2, continue_function, 'Продолжить'),
        (HALF_WINDOW_WIDTH, HALF_WINDOW_HEIGHT - (BUTTON_HEIGHT + GAP) * 1, new_game, 'Заново'),
        (HALF_WINDOW_WIDTH, HALF_WINDOW_HEIGHT - (BUTTON_HEIGHT + GAP) * 0, go_menu, 'Меню'),
        (HALF_WINDOW_WIDTH, HALF_WINDOW_HEIGHT - (BUTTON_HEIGHT + GAP) * -1, quit, 'Выйти')
    )

    button_restart_game_over = Button(*BUTTONS_DATA[0])
    button_menu_game_over = Button(*BUTTONS_DATA[1])

    button_continue = Button(*BUTTONS_DATA[2])
    button_restart_pause = Button(*BUTTONS_DATA[3])
    button_menu_pause = Button(*BUTTONS_DATA[4])
    button_quit = Button(*BUTTONS_DATA[5])

    game_over_buttons = (button_restart_game_over, button_menu_game_over)
    pause_buttons = (button_continue, button_restart_pause, button_menu_pause, button_quit)

    global foods, is_pause, snake
    foods = [(-100, -100)]
    direction = (1, 0)
    iter_food = 0
    iter_snake = 0
    is_pause = False
    snake = [(WINDOW_CENTRE_X - i * DIAMETER, WINDOW_CENTRE_Y) for i in range(5, 0, -1)]


    def game_over():
        global game_over_text_line1, game_over_text_line2, best_score
        score = len(snake) - 5
        game_over_text_line1 = FONT.render(f'Игра закончена! Счёт: {len(snake) - 5}', True, GAME_OVER_TEXT_COLOR)
        if score <= best_score:
            game_over_text_line2 = FONT.render(f'Рекорд: {best_score}', True, GAME_OVER_TEXT_COLOR)
        else:
            game_over_text_line2 = FONT.render(f'Предыдущий рекорд: {best_score}', True, GAME_OVER_TEXT_COLOR)
            with open('Score') as file:
                line = file.readline().split()
                line[0] = str(score)

            with open('Score', 'w') as file:
                file.write(' '.join(line) + '\n')
            best_score = score


    while True:
        pygame.time.Clock().tick(FPS)
        window.fill(WINDOW_COLOR)

        if is_pause:
            snake = prev_snake
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    is_pause = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in pause_buttons:
                        if button.rect.collidepoint(event.pos):
                            button.use_function()
                if event.type == pygame.QUIT:
                    quit()

            for food in foods:
                pygame.draw.circle(window, FOOD_COLOR, (food[0], food[1]), RADIUS_FOOD)

            for i, pos in enumerate(snake):
                pygame.draw.circle(window, SNAKE_COLOR, (pos[0], pos[1]), RADIUS)
            pygame.draw.circle(window, EYE_COLOR, (snake[-1][0], snake[-1][1]), RADIUS_FOOD)

            for button in pause_buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.change_active()
                text = FONT.render(button.text, True, BUTTON_TEXT_COLOR)
                pygame.draw.rect(window, ACTIVATED_BUTTON_COLOR, button.frame)
                pygame.draw.rect(window, button.color, button.rect)
                window.blit(text, text.get_rect(center=button.rect.center))
        else:
            iter_food += 1
            iter_snake += 10

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    for key, data in DIRECTIONS.items():
                        if event.key in key and direction[data[0]] != data[1]:
                            copy_snake = list(snake[1:]) + [(snake[-1][0] + DIAMETER * data[2][0], snake[-1][1] + DIAMETER * data[2][1])]
                            if copy_snake[-1] == copy_snake[-3]:
                                iter_snake = 0
                                snake = snake[1:] + [(snake[-1][0] + DIAMETER * direction[0],
                                                      snake[-1][1] + DIAMETER * direction[1])]
                            direction = data[2]
                    if event.key == pygame.K_ESCAPE:
                        game_over()
                        is_pause = True
                    if event.key == pygame.K_q:
                        game_over()
                if event.type == pygame.QUIT:
                    quit()

            if iter_snake >= SPEED:
                iter_snake = 0
                del snake[0]
                snake.append((snake[-1][0] + DIAMETER * direction[0], snake[-1][1] + DIAMETER * direction[1]))

            if iter_food >= SPEED_FOOD + (INCREASE_SPEED_FOOD * 2) ** (len(foods)):
                iter_food = 0
                create_food()

            for food in foods:
                pygame.draw.circle(window, FOOD_COLOR, food, RADIUS_FOOD)
                if abs(food[0] - snake[-1][0]) < DIAMETER and abs(food[1] - snake[-1][1]) < DIAMETER:
                    foods.remove(food)
                    snake.insert(0, (snake[0][0] - (snake[1][0] - snake[0][0]),
                                     snake[0][1] - (snake[1][1] - snake[0][1])))

            if not CAN_CRASH_SELF and snake[-1] in snake[:-1]:
                game_over()
                break

            if not (0 <= snake[-1][0] <= WINDOW_WIDTH and 0 <= snake[-1][1] <= WINDOW_HEIGHT):
                if not CAN_CRASH_WALL:
                    game_over()
                    break
                if not (0 <= snake[-1][0] <= WINDOW_WIDTH):
                    change = END_X if snake[-1][0] < 0 else RADIUS
                    snake[-1] = (change, snake[-1][1])
                if not (0 <= snake[-1][1] <= WINDOW_HEIGHT):
                    change = END_Y if snake[-1][1] < 0 else RADIUS
                    snake[-1] = (snake[-1][0], change)

            for i, pos in enumerate(snake):
                pygame.draw.circle(window, SNAKE_COLOR, (pos[0], pos[1]), RADIUS)
            pygame.draw.circle(window, EYE_COLOR, (snake[-1][0], snake[-1][1]), RADIUS_FOOD)

            prev_snake = list(snake)
        score_text = FONT.render(f'Очки: {(len(snake) - 5)}', True, TEXT_COLOR)
        window.blit(score_text, (GAP, GAP))
        pygame.display.update()

    while True:
        pygame.time.Clock().tick(FPS)
        window.fill(WINDOW_COLOR)

        snake = prev_snake
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in game_over_buttons:
                    if button.rect.collidepoint(event.pos):
                        button.use_function()
            if event.type == pygame.QUIT:
                quit()

        for food in foods:
            pygame.draw.circle(window, FOOD_COLOR, (food[0], food[1]), RADIUS_FOOD)

        for i, pos in enumerate(snake):
            pygame.draw.circle(window, SNAKE_COLOR, (pos[0], pos[1]), RADIUS)
        pygame.draw.circle(window, 'red', (snake[-1][0], snake[-1][1]), RADIUS)
        pygame.draw.circle(window, EYE_COLOR, (snake[-1][0], snake[-1][1]), RADIUS_FOOD)

        score_text = FONT.render(f'Очки: {(len(snake) - 5)}', True, TEXT_COLOR)
        window.blit(score_text, (10, 10))

        window.blit(game_over_text_line1, (HALF_WINDOW_WIDTH - game_over_text_line1.get_width() // 2,
                                           HALF_WINDOW_HEIGHT - BUTTON_HEIGHT - game_over_text_line1.get_height()))
        window.blit(game_over_text_line2, (HALF_WINDOW_WIDTH - game_over_text_line2.get_width() // 2,
                                           HALF_WINDOW_HEIGHT - BUTTON_HEIGHT))

        for button in game_over_buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.change_active()
            text = FONT.render(button.text, True, BUTTON_TEXT_COLOR)
            pygame.draw.rect(window, ACTIVATED_BUTTON_COLOR, button.frame)
            pygame.draw.rect(window, button.color, button.rect)
            window.blit(text, text.get_rect(center=button.rect.center))

        pygame.display.update()
        