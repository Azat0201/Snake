import pygame
from random import randint
from time import time
from Button import Button
from Menu import new_loop as go_menu

global foods, is_pause, snake
global game_over_text_line1, game_over_text_line2, best_score, font
global window_width, window_height, half_window_width, half_window_height, increase_speed_food, gap, end_x, end_y, \
    can_crash_wall, can_crash_self, window_centre_x, window_centre_y
global window_color, text_color, button_color, button_text_color, activated_button_color, game_over_text_color, \
    snake_color, eye_color, food_color
global fps, speed, speed_food, radius, diameter, radius_food, directions, button_width, button_height


def create_food():
    position = foods[0]
    timeout = time() + 1
    while position in foods:
        if time() > timeout:
            break
        position = (randint(radius, window_width - radius), randint(radius, window_height - radius))
        position = (position[0] - position[0] % diameter + radius,
                    position[1] - position[1] % diameter + radius)
        if position in snake:
            break
    else:
        foods.append(position)


def new_loop(window_size, difficult, increase_food_time, crash_wall, crash_self):
    global window_width, window_height, half_window_width, half_window_height, increase_speed_food, gap, end_x, end_y, \
        can_crash_wall, can_crash_self, window_centre_x, window_centre_y
    global window_color, text_color, button_color, button_text_color, activated_button_color, game_over_text_color, \
        snake_color, eye_color, food_color
    global fps, speed, speed_food, radius, diameter, radius_food, directions, button_width, button_height, best_score

    with open('settings') as settings, open('colors') as colors, open('score') as best_score_file:
        best_score = int(best_score_file.readline().split()[0])
        data = [int(settings.readline().split()[0]) for _ in range(3)]
        colors = [colors.readline().split()[0] for _ in range(9)]

    speed, difference_speed, speed_food = data
    window_color, text_color, button_color, button_text_color, activated_button_color, game_over_text_color, snake_color, eye_color, food_color = colors

    window_width, window_height = window_size
    half_window_width = window_width // 2
    half_window_height = window_height // 2
    gap = (window_width + window_height) // 200
    increase_speed_food = increase_food_time
    can_crash_wall = crash_wall
    can_crash_self = crash_self

    fps = 60
    speed -= (difficult * difference_speed)
    radius = (window_width + window_height) // 100
    diameter = radius * 2
    radius_food = radius // 2
    button_width = window_width // 5
    button_height = window_height // 10

    window_centre_x = half_window_width - half_window_width % diameter + radius
    window_centre_y = half_window_height - half_window_height % diameter + radius
    end_x = window_width - (window_width - radius) % diameter
    end_y = window_height - (window_height - radius) % diameter

    directions = {
        (pygame.K_w, pygame.K_UP): (1, 1, (0, -1)),
        (pygame.K_a, pygame.K_LEFT): (0, 1, (-1, 0)),
        (pygame.K_s, pygame.K_DOWN): (1, -1, (0, 1)),
        (pygame.K_d, pygame.K_RIGHT): (0, -1, (1, 0))
    }

    Button.width_class = button_width
    Button.height_class = button_height
    Button.gap_class = gap
    Button.color_class = button_color
    Button.activated_color_class = activated_button_color

    new_game()


def game_over():
    global game_over_text_line1, game_over_text_line2, best_score, font

    score = len(snake) - 5
    game_over_text_line1 = font.render(f'игра закончена! счёт: {len(snake) - 5}', True, game_over_text_color)
    if score <= best_score:
        game_over_text_line2 = font.render(f'рекорд: {best_score}', True, game_over_text_color)
    else:
        game_over_text_line2 = font.render(f'предыдущий рекорд: {best_score}', True, game_over_text_color)
        with open('score') as file:
            line = file.readline().split()
            line[0] = str(score)

        with open('score', 'w') as file:
            file.write(' '.join(line) + '\n')
        best_score = score


def continue_function():
    global is_pause
    is_pause = False


def new_game():
    global game_over_text_line1, game_over_text_line2, best_score, font
    global foods, is_pause, snake

    pygame.display.set_caption('Snake')
    window = pygame.display.set_mode((window_width, window_height))
    font = pygame.font.SysFont('verdana', (window_width + window_height) // 100)

    buttons_data = (
        (half_window_width - (button_width + gap) // 2, half_window_height, new_game, 'Заново'),
        (half_window_width + (button_width + gap) // 2, half_window_height, go_menu, 'Меню'),
        (half_window_width, half_window_height - (button_height + gap) * 2, continue_function, 'Продолжить'),
        (half_window_width, half_window_height - (button_height + gap) * 1, new_game, 'Заново'),
        (half_window_width, half_window_height - (button_height + gap) * 0, go_menu, 'Меню'),
        (half_window_width, half_window_height - (button_height + gap) * -1, quit, 'Выйти')
    )

    button_restart_game_over = Button(*buttons_data[0])
    button_menu_game_over = Button(*buttons_data[1])

    button_continue = Button(*buttons_data[2])
    button_restart_pause = Button(*buttons_data[3])
    button_menu_pause = Button(*buttons_data[4])
    button_quit = Button(*buttons_data[5])

    game_over_buttons = (button_restart_game_over, button_menu_game_over)
    pause_buttons = (button_continue, button_restart_pause, button_menu_pause, button_quit)

    foods = [(-radius_food, -radius_food)]
    direction = (1, 0)
    iter_food = 0
    iter_snake = 0
    is_pause = False
    snake = [(window_centre_x - i * diameter, window_centre_y) for i in range(5, 0, -1)]
    prev_snake = snake

    while True:
        pygame.time.Clock().tick(fps)
        window.fill(window_color)

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
                if event.type == pygame.quit:
                    quit()

            for food in foods:
                pygame.draw.circle(window, food_color, (food[0], food[1]), radius_food)

            for pos in snake:
                pygame.draw.circle(window, snake_color, (pos[0], pos[1]), radius)
            pygame.draw.circle(window, eye_color, (snake[-1][0], snake[-1][1]), radius_food)

            for button in pause_buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.change_pressed()
                text = font.render(button.text, True, button_text_color)
                pygame.draw.rect(window, activated_button_color, button.frame)
                pygame.draw.rect(window, button.color, button.rect)
                window.blit(text, text.get_rect(center=button.rect.center))
        else:
            iter_food += 10
            iter_snake += 10

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    for key, data in directions.items():
                        if event.key == key[0] and abs(direction[data[0]]) != abs(data[1]):
                            copy_snake = list(snake[1:]) + [(snake[-1][0] + diameter * data[2][0], snake[-1][1] + diameter * data[2][1])]
                            if copy_snake[-1] == copy_snake[-3]:
                                iter_snake = 0
                                snake = snake[1:] + [(snake[-1][0] + diameter * direction[0],
                                                      snake[-1][1] + diameter * direction[1])]
                            direction = data[2]
                    if event.key == pygame.K_ESCAPE:
                        game_over()
                        is_pause = True
                    if event.key == pygame.K_q:
                        game_over()
                if event.type == pygame.quit:
                    quit()

            if iter_snake >= speed:
                iter_snake = 0
                del snake[0]
                snake.append((snake[-1][0] + diameter * direction[0], snake[-1][1] + diameter * direction[1]))

            if iter_food >= speed_food + (increase_speed_food * 2) ** (len(foods)):
                iter_food = 0
                create_food()

            for food in foods:
                pygame.draw.circle(window, food_color, food, radius_food)
                if abs(food[0] - snake[-1][0]) < diameter and abs(food[1] - snake[-1][1]) < diameter:
                    foods.remove(food)
                    snake.insert(0, (snake[0][0] - (snake[1][0] - snake[0][0]),
                                     snake[0][1] - (snake[1][1] - snake[0][1])))

            if not can_crash_self and snake[-1] in snake[:-1]:
                game_over()
                break

            if not (0 <= snake[-1][0] <= window_width and 0 <= snake[-1][1] <= window_height):
                if not can_crash_wall:
                    game_over()
                    break
                if not (0 <= snake[-1][0] <= window_width):
                    change = end_x if snake[-1][0] < 0 else radius
                    snake[-1] = (change, snake[-1][1])
                if not (0 <= snake[-1][1] <= window_height):
                    change = end_y if snake[-1][1] < 0 else radius
                    snake[-1] = (snake[-1][0], change)

            for i, pos in enumerate(snake):
                pygame.draw.circle(window, snake_color, (pos[0], pos[1]), radius)
            pygame.draw.circle(window, eye_color, (snake[-1][0], snake[-1][1]), radius_food)

            prev_snake = list(snake)
        score_text = font.render(f'очки: {(len(snake) - 5)}', True, text_color)
        window.blit(score_text, (gap, gap))
        pygame.display.update()

    while True:
        pygame.time.Clock().tick(fps)
        window.fill(window_color)

        snake = prev_snake
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in game_over_buttons:
                    if button.rect.collidepoint(event.pos):
                        button.use_function()
            if event.type == pygame.quit:
                quit()

        for food in foods:
            pygame.draw.circle(window, food_color, (food[0], food[1]), radius_food)

        for i, pos in enumerate(snake):
            pygame.draw.circle(window, snake_color, (pos[0], pos[1]), radius)
        pygame.draw.circle(window, 'red', (snake[-1][0], snake[-1][1]), radius)
        pygame.draw.circle(window, eye_color, (snake[-1][0], snake[-1][1]), radius_food)

        score_text = font.render(f'очки: {(len(snake) - 5)}', True, text_color)
        window.blit(score_text, (10, 10))

        window.blit(game_over_text_line1, (half_window_width - game_over_text_line1.get_width() // 2,
                                           half_window_height - button_height - game_over_text_line1.get_height()))
        window.blit(game_over_text_line2, (half_window_width - game_over_text_line2.get_width() // 2,
                                           half_window_height - button_height))

        for button in game_over_buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.change_pressed()
            text = font.render(button.text, True, button_text_color)
            pygame.draw.rect(window, activated_button_color, button.frame)
            pygame.draw.rect(window, button.color, button.rect)
            window.blit(text, text.get_rect(center=button.rect.center))

        pygame.display.update()
