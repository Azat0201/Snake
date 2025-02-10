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


START_LEN_SNAKE = 5


def create_food():
    position = foods[0]
    timeout = time() + 0.1
    while position in foods:
        if time() > timeout:
            break
        position = (randint(radius, window_width - radius), randint(radius, window_height - radius))
        position = (position[0] - position[0] % diameter + radius,
                    position[1] - position[1] % diameter + radius)
        if position in snake or position in foods:
            continue
    else:
        foods.append(position)
    

def new_loop(window_size, difficult, increase_food_time, crash_wall, crash_self, first_lunch=False):
    global window_width, window_height, half_window_width, half_window_height, increase_speed_food, gap, end_x, end_y, \
        can_crash_wall, can_crash_self, window_centre_x, window_centre_y
    global window_color, text_color, button_color, button_text_color, activated_button_color, game_over_text_color, \
        snake_color, eye_color, food_color
    global fps, speed, speed_food, radius, diameter, radius_food, directions, button_width, button_height, best_score

    if first_lunch:
        go_menu()

    with open('settings.txt') as settings, open('colors.txt') as colors, open('score.txt') as best_score_file:
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
    speed += ((2 - difficult) * difference_speed * (window_width + window_height / 2) / 2000)
    if speed <= 0:
        speed = 0.1
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
        (pygame.K_w, pygame.K_UP): (1, (0, -1)),
        (pygame.K_a, pygame.K_LEFT): (0, (-1, 0)),
        (pygame.K_s, pygame.K_DOWN): (1, (0, 1)),
        (pygame.K_d, pygame.K_RIGHT): (0, (1, 0))
    }

    Button.width_class = button_width
    Button.height_class = button_height
    Button.gap_class = gap
    Button.color_class = button_color
    Button.activated_color_class = activated_button_color

    new_game()


def write_best_score():
    global snake, best_score
    best_score = max(len(snake) - START_LEN_SNAKE, best_score)
    with open('score.txt') as file:
        line = file.readline().split()
        line[0] = str(best_score)

    with open('score.txt', 'w') as file:
        file.write(' '.join(line) + '\n')


def continue_button_function():
    global is_pause
    is_pause = False
    
    
def restart_button_function():
    write_best_score()
    new_game()


def go_menu_button_function():
    write_best_score()
    go_menu()


def quit_button_function():
    write_best_score()
    quit()


def new_game():
    global game_over_text_line1, game_over_text_line2, best_score, font
    global foods, is_pause, snake

    pygame.init()
    pygame.display.set_caption('Snake')
    window = pygame.display.set_mode((window_width, window_height))
    font = pygame.font.SysFont('verdana', (window_width + window_height) // 100)
    clock = pygame.time.Clock()

    snake = [(window_centre_x - i * diameter, window_centre_y) for i in range(START_LEN_SNAKE, 0, -1)]
    prev_snake = snake
    speed_snake = 0

    buttons_data = (
        (half_window_width - (button_width + gap) // 2, half_window_height, restart_button_function, 'Заново'),
        (half_window_width + (button_width + gap) // 2, half_window_height, go_menu_button_function, 'Меню'),
        (half_window_width, half_window_height - (button_height + gap) * 2, continue_button_function, 'Продолжить'),
        (half_window_width, half_window_height - (button_height + gap) * 1, restart_button_function, 'Заново'),
        (half_window_width, half_window_height - (button_height + gap) * 0, go_menu_button_function, 'Меню'),
        (half_window_width, half_window_height - (button_height + gap) * -1, quit_button_function, 'Выйти')
    )

    button_restart_game_over = Button(*buttons_data[0])
    button_menu_game_over = Button(*buttons_data[1])

    button_continue = Button(*buttons_data[2])
    button_restart_pause = Button(*buttons_data[3])
    button_menu_pause = Button(*buttons_data[4])
    button_quit = Button(*buttons_data[5])

    game_over_buttons = (button_restart_game_over, button_menu_game_over)
    pause_buttons = (button_continue, button_restart_pause, button_menu_pause, button_quit)

    foods = [(-window_width, -window_height)]
    speed_food_game = 0
    direction = (1, 0)
    iter_food = 0
    iter_snake = 0
    is_pause = False

    while True:
        clock.tick(fps)
        window.fill(window_color)

        if not is_pause:
            iter_food += 1
            iter_snake += 1

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    for key, data in directions.items():
                        if event.key in key and abs(direction[data[0]]) != 1:
                            copy_snake = list(snake[1:]) + [(snake[-1][0] + diameter * data[1][0], snake[-1][1] + diameter * data[1][1])]
                            if copy_snake[-1] == copy_snake[-3]:
                                iter_snake = 0
                                snake = snake[1:] + [(snake[-1][0] + diameter * direction[0],
                                                      snake[-1][1] + diameter * direction[1])]
                            direction = data[1]
                    if not speed_snake and pygame.key != pygame.K_ESCAPE:
                        speed_snake = speed
                        speed_food_game = speed_food
                    if event.key == pygame.K_ESCAPE:
                        is_pause = True
                if event.type == pygame.QUIT:
                    quit()

            if iter_snake >= speed_snake > 0:
                iter_snake = 0
                del snake[0]
                snake.append((snake[-1][0] + diameter * direction[0], snake[-1][1] + diameter * direction[1]))

            if iter_food >= speed_food_game + (increase_speed_food * 2) ** (len(foods)) and speed_food_game > 0:
                iter_food = 0
                create_food()

            for food in foods:
                pygame.draw.circle(window, food_color, food, radius_food)
                if abs(food[0] - snake[-1][0]) < diameter and abs(food[1] - snake[-1][1]) < diameter:
                    foods.remove(food)
                    snake.insert(0, (snake[0][0] - (snake[1][0] - snake[0][0]),
                                     snake[0][1] - (snake[1][1] - snake[0][1])))

            if not can_crash_self and snake[-1] in snake[:-1]:
                break

            if not (0 <= snake[-1][0] <= window_width and 0 <= snake[-1][1] <= window_height):
                if not can_crash_wall:
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
        else:
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

        score_text = font.render(f'Очки: {(len(snake) - START_LEN_SNAKE)}', True, text_color)
        window.blit(score_text, (gap, gap))
        pygame.display.update()

    while True:
        clock.tick(fps)
        window.fill(window_color)

        snake = prev_snake
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in game_over_buttons:
                    if button.rect.collidepoint(event.pos):
                        button.use_function()
            if event.type == pygame.QUIT:
                quit()

        for food in foods:
            pygame.draw.circle(window, food_color, (food[0], food[1]), radius_food)

        for i, pos in enumerate(snake):
            pygame.draw.circle(window, snake_color, (pos[0], pos[1]), radius)
        pygame.draw.circle(window, 'red', (snake[-1][0], snake[-1][1]), radius)
        pygame.draw.circle(window, eye_color, (snake[-1][0], snake[-1][1]), radius_food)

        score = len(snake) - START_LEN_SNAKE
        game_over_text_line1 = font.render(f'Игра закончена! Счёт: {len(snake) - 5}', True, game_over_text_color)
        if score <= best_score:
            game_over_text_line2 = font.render(f'Рекорд: {best_score}', True, game_over_text_color)
        else:
            game_over_text_line2 = font.render(f'Предыдущий рекорд: {best_score}', True, game_over_text_color)

        score_text = font.render(f'Очки: {(len(snake) - 5)}', True, text_color)
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


if __name__ == '__main__':
    go_menu()
