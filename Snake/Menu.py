import pygame
import ctypes
import Snake
from Button import Button

global window, size_font, font
global buttons, setting_buttons, choice_buttons
global window_width, window_height


with open('Colors.txt') as colors:
    window_color, text_color, button_color, button_text_color, activated_button_color = (colors.readline().split()[0] for _ in range(5))

difficulties = ('Лёгкий', 'Средний', 'Сложный')
current_difficult = 1
current_size_ind = 0
is_increase_food_time = True
can_crash_wall = False
can_crash_self = False
user32 = ctypes.windll.user32
monitor_size = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
window_sizes = ((3840, 2160), (2560, 1440), (1920, 1080), (1680, 1050), (1600, 1200), (1600, 900), (1440, 900),
                (1400, 1050), (1366, 768), (1366, 760), (1280, 1024), (1280, 960), (1280, 800), (1280, 768),
                (1280, 720), (1280, 600), (1152, 864), (1024, 768), (800, 600), (720, 576), (720, 480), (640, 480),
                (680, 400), (512, 384), (400, 300), (320, 240), (320, 200))
window_sizes = (monitor_size, ) + tuple(filter(
    lambda x: x[0] <= monitor_size[0] and x[1] <= monitor_size[1] and x != monitor_size, window_sizes
))
fps = 60


def start_game(first_lunch=False):
    Snake.new_loop(window_sizes[current_size_ind], current_difficult,
                   is_increase_food_time, can_crash_wall, can_crash_self, first_lunch)


def change_difficult(button):
    global current_difficult
    current_difficult = (current_difficult + 1) % len(difficulties)
    button._text = difficulties[current_difficult]


def show_settings():
    for button in setting_buttons:
        button.change_visible()


def show_choice_button():
    for button in choice_buttons:
        button.visible = True


def hide_choice_button():
    for button in choice_buttons:
        button.visible = False
        
        
def change_active(button, value):
    value = not value
    button._active = value


def change_is_increase_food_time(button):
    global is_increase_food_time
    is_increase_food_time = not is_increase_food_time
    button._active = is_increase_food_time


def change_can_crash_wall(button):
    global can_crash_wall
    can_crash_wall = not can_crash_wall
    button._active = can_crash_wall


def change_can_crash_self(button):
    global can_crash_self
    can_crash_self = not can_crash_self
    button._active = can_crash_self


def activate(func):
    func()


def increase_size_window(button):
    global current_size_ind, setting_buttons
    current_size_ind = (current_size_ind + 1) % len(window_sizes)
    button.title = f'{window_sizes[current_size_ind][0]}x{window_sizes[current_size_ind][1]}'
    new_loop(setting_buttons[0].visible)


def decrease_size_window(button):
    global current_size_ind, setting_buttons
    current_size_ind = (current_size_ind - 1) % len(window_sizes)
    button.title = f'{window_sizes[current_size_ind][0]}x{window_sizes[current_size_ind][1]}'
    new_loop(setting_buttons[0].visible)
    

def reset_record(button):
    button.parameters = (reset_record_function,)
    show_choice_button()


def reset_record_function():
    with open('score.txt') as file:
        line = file.readline().split()
        line[0] = '0'

    with open('score.txt', 'w') as file:
        file.write(' '.join(line) + '\n')

    hide_choice_button()
    new_loop(setting_buttons[0].visible)


def show_text(text, x, y, width, height, color=button_text_color, centered_x=True, centered_y=True):
    words = text.split(' ')
    lines = [[]]
    count = 0
    for word in words:
        if r'\n' in word:
            index = word.index(r'\n')
            lines[count].append(word[:index])
            count += 1
            lines.append([])
            words.insert(words.index(word) + 1, word[index + 2:])
        elif len(word) + sum(map(len, lines[count])) + len(lines[count]) > width / window_width * 100:
            count += 1
            lines.append([word])
        else:
            lines[count].append(word)

    gap = (height - count * size_font) // 2
    for i, line in enumerate(lines):
        text_line = font.render(' '.join(line), True, color)
        pos = (x - (text_line.get_width() // 2 * centered_x), y + (gap * centered_y) - size_font // 2 + i * size_font)
        window.blit(text_line, pos)


def move_window(x, y):
    size = pygame.display.get_wm_info()['window']
    ctypes.windll.user32.MoveWindow(
        size, x - 8, y - 31, window_width, window_height, False  # 3, 26 - for .exe and 8, 31 - for .py
    )


def new_loop(show_buttons=False):
    global window, size_font, font
    global buttons, setting_buttons, choice_buttons
    global window_width, window_height
    pygame.init()

    window_width, window_height = window_sizes[current_size_ind]
    gap = (window_width + window_height) // 200
    size_font = (window_width + window_height) // 100

    button_width = window_width // 4
    button_height = window_height // 8
    button_x = window_width // 2
    button_x2 = button_x + button_width + gap
    button_y = button_height + gap
    font = pygame.font.SysFont('verdana', size_font)
    clock = pygame.time.Clock()

    Button.width_class = button_width
    Button.height_class = button_height
    Button.gap_class = gap
    Button.color_class = button_color
    Button.activated_color_class = activated_button_color

    window = pygame.display.set_mode((window_width, window_height))
    move_window((monitor_size[0] - window_width) // 2, (monitor_size[1] - window_height) // 2)
    pygame.display.set_caption('Menu')

    with open('score.txt') as file:
        score = file.readline().split()[0]

    str_sizes = '-' * 28 + '\\n' + '\\n'.join(map(
        lambda x: f'{x[0]} x {x[1]}{" - current size" if x == window_sizes[current_size_ind] else ""}', window_sizes)
    ) + ' ' + '-' * 28

    buttons_data = (
        (button_x, button_y * 1, start_game, 'Начать игру'),
        (button_x, button_y * 2, change_difficult, difficulties[current_difficult], None, None, None, 'self'),
        (button_x, button_y * 3, show_settings, 'Настройки'),
        (button_x, button_y * 4, quit, 'Выйти'),
        (button_x2, button_y * 1, change_is_increase_food_time, 'Увеличение времени создание еды от количества еды', show_buttons, is_increase_food_time, 'Увеличивает скорость появления еды для змейки в зависимости от количества её', 'self'),
        (button_x2, button_y * 2, change_can_crash_wall, 'Врезаться в стены', show_buttons, can_crash_wall, 'Позволяет змейки проходить через стены', 'self'),
        (button_x2, button_y * 3, change_can_crash_self, 'Врезаться в себя', show_buttons, can_crash_self, 'Позволяет змейки проходить через себя', 'self'),
        (button_x2 - button_width / 8, button_y * 4, increase_size_window, f'{window_width}x{window_height}', show_buttons, None, str_sizes, 'self', button_width - button_width // 4),
        (button_x2 + button_width / 2.5 - gap // 2, button_y * 4, decrease_size_window, '/\\', show_buttons, None, str_sizes, 'self', button_width // 4 - gap),
        (button_x2, button_y * 5, reset_record, 'Сбросить рекорд', show_buttons,  None, 'Сбрасывает лучший результат'),
        ((button_x - button_width / 4) / 2, button_y * 2, None, 'Вы уверенны?', False, None, None, None, None, None, None, None, False),
        ((button_x - button_width / 4 - button_width / 2 - gap / 2) / 2, button_y * 3, activate, 'Да', False, None, None, None, (button_width - gap) / 2),
        ((button_x - button_width / 4 + button_width / 2 + gap / 2) / 2, button_y * 3, hide_choice_button, 'Нет', False, None, None, None, (button_width - gap) / 2),
    )

    button_start = Button(*buttons_data[0])
    button_difficulty = Button(*buttons_data[1])
    button_show_settings = Button(*buttons_data[2])
    button_exit = Button(*buttons_data[3])
    button_increase = Button(*buttons_data[4])
    button_can_wall = Button(*buttons_data[5])
    button_can_self = Button(*buttons_data[6])
    button_change_size = Button(*buttons_data[7])
    button_increase_size = Button(*buttons_data[8])
    button_reset_record = Button(*buttons_data[9])
    button_no = Button(*buttons_data[-1])
    button_yes = Button(*buttons_data[-2])
    button_choice = Button(*buttons_data[-3])

    button_reset_record.parameters = (button_yes,)

    setting_buttons = (button_increase, button_can_wall, button_can_self, button_change_size, button_increase_size, button_reset_record)
    choice_buttons = (button_choice, button_no, button_yes)
    buttons = (button_start, button_difficulty, button_show_settings, button_exit) + setting_buttons + choice_buttons

    while True:
        clock.tick(fps)
        window.fill(window_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        hide_choice_button()
                        button.use_function()

        for button in buttons:
            if button.visible:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.change_pressed()
                    if button.additional_text is not None:
                        show_text(button.additional_text, gap * 2, button_y - button_height // 2,
                                  button_width, button_height * 3, text_color, False, False)

                pygame.draw.rect(window, activated_button_color, button.frame)
                pygame.draw.rect(window, button.color, button.rect)
                show_text(button.text, button.position[0], button.rect.y, button.width, button.height)

        score_text = font.render(f'рекорд: {score}', True, text_color)
        window.blit(score_text, (gap, gap))

        pygame.display.update()


if __name__ == '__main__':
    start_game(True)
    new_loop()
