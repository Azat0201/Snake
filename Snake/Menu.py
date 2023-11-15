import pygame
import ctypes
import Snake
from Button import Button


with open('Colors') as colors:
    WINDOW_COLOR, TEXT_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR, ACTIVATED_BUTTON_COLOR = (colors.readline().split()[0] for _ in range(5))

DIFFICULTIES = ('Лёгкий', 'Средний', 'Сложный')
current_difficult = 1
current_size = 0
is_increase_food_time = True
can_crash_wall = False
can_crash_self = False
user32 = ctypes.windll.user32
MONITOR_WIDTH = user32.GetSystemMetrics(0)
MONITOR_HEIGHT = user32.GetSystemMetrics(1)
MONITOR_SIZE = ((MONITOR_WIDTH, MONITOR_HEIGHT),)
WINDOWS_SIZES = ((3840, 2160), (2560, 1440), (1920, 1080), (1680, 1050), (1600, 1200), (1600, 900), (1440, 900),
                 (1400, 1050), (1366, 768), (1366, 760), (1280, 1024), (1280, 960), (1280, 800), (1280, 768),
                 (1280, 720), (1280, 600), (1152, 864), (1024, 768), (800, 600), (720, 576), (720, 480), (640, 480),
                 (680, 400), (512, 384), (400, 300), (320, 240), (320, 200))
WINDOWS_SIZES = MONITOR_SIZE + tuple(filter(lambda x: x[0] <= MONITOR_WIDTH and x[1] <= MONITOR_HEIGHT and
                                                      x != MONITOR_SIZE[0], WINDOWS_SIZES))
FPS = 60


def start_game():
    global buttons
    if buttons[0].visible:
        show_settings()
    Snake.new_loop(WINDOWS_SIZES[current_size], current_difficult, is_increase_food_time, can_crash_wall, can_crash_self)


def change_difficult(button):
    global current_difficult
    current_difficult = (current_difficult + 1) % len(DIFFICULTIES)
    button._text = DIFFICULTIES[current_difficult]


def show_settings():
    global setting_buttons
    for button in setting_buttons:
        button.change_visible()


def show_choice_button():
    global choice_buttons
    for button in choice_buttons:
        button.visible = True


def hide_choice_button():
    global choice_buttons
    for button in choice_buttons:
        button.visible = False


def change_is_increase_food_time(button):
    global is_increase_food_time
    is_increase_food_time = not is_increase_food_time
    button._activator = is_increase_food_time


def change_can_crash_wall(button):
    global can_crash_wall
    can_crash_wall = not can_crash_wall
    button._activator = can_crash_wall


def change_can_crash_self(button):
    global can_crash_self
    can_crash_self = not can_crash_self
    button._activator = can_crash_self


def change_size_window(button):
    global current_size
    current_size = (current_size + 1) % len(WINDOWS_SIZES)
    button.title = f'{WINDOWS_SIZES[current_size][0]}x{WINDOWS_SIZES[current_size][1]}'
    new_loop()


def increase_size_window(button):
    global current_size
    current_size = (current_size - 1) % len(WINDOWS_SIZES)
    button.title = f'{WINDOWS_SIZES[current_size][0]}x{WINDOWS_SIZES[current_size][1]}'
    new_loop()


def activate(func):
    func()


def reset_record(button):
    global is_reset_record
    button.parameters = (reset_record_function,)
    show_choice_button()


def reset_record_function():
    with open('Score') as file:
        line = file.readline().split()
        line[0] = '0'

    with open('Score', 'w') as file:
        file.write(' '.join(line) + '\n')

    hide_choice_button()
    new_loop()


def move_window(x, y):
    size = pygame.display.get_wm_info()['window']
    ctypes.windll.user32.MoveWindow(size, x - 8, y - 31, WINDOWS_SIZES[current_size][0], WINDOWS_SIZES[current_size][1], False)


def new_loop():
    global buttons, setting_buttons, choice_buttons
    pygame.init()

    WINDOW_WIDTH, WINDOW_HEIGHT = WINDOWS_SIZES[current_size]
    GAP = (WINDOW_WIDTH + WINDOW_HEIGHT) // 200
    SIZE_FONT = (WINDOW_WIDTH + WINDOW_HEIGHT) // 100

    BUTTON_WIDTH = WINDOW_WIDTH // 4
    BUTTON_HEIGHT = WINDOW_HEIGHT // 8
    BUTTON_X = WINDOW_WIDTH // 2
    BUTTON_X2 = BUTTON_X + BUTTON_WIDTH + GAP
    BUTTON_Y = BUTTON_HEIGHT + GAP
    FONT = pygame.font.SysFont('Verdana', SIZE_FONT)

    Button.width_class = BUTTON_WIDTH
    Button.height_class = BUTTON_HEIGHT
    Button.gap_class = GAP
    Button.color_class = BUTTON_COLOR
    Button.activated_color_class = ACTIVATED_BUTTON_COLOR

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    move_window((MONITOR_WIDTH - WINDOW_WIDTH) // 2, (MONITOR_HEIGHT - WINDOW_HEIGHT) // 2)
    pygame.display.set_caption('Snake menu')

    with open('Score') as file:
        score = file.readline().split()[0]

    # all sizes window
    transform_size_str = lambda x: f'{x[0]} x {x[1]}{" - current size" if x == WINDOWS_SIZES[current_size] else ""}'
    str_sizes = '-' * 28 + '\\n' + '\\n'.join(map(transform_size_str, WINDOWS_SIZES)) + ' ' + '-' * 28


    # parameters: (x, y, func, text, visible, activator(value at which active),
    # additional text (text which show when hovering cursor),
    # parameters (for func, in sequence, if 'self', parameter self func), width (not default), gap (not default),
    # color(not default), activated color (not default, color when button is active))
    BUTTONS_DATA = (
        (BUTTON_X, BUTTON_Y * 1, start_game, 'Начать игру'),
        (BUTTON_X, BUTTON_Y * 2, change_difficult, DIFFICULTIES[current_difficult], None, None, None, 'self'),
        (BUTTON_X, BUTTON_Y * 3, show_settings, 'Настройки'),
        (BUTTON_X, BUTTON_Y * 4, quit, 'Выйти'),
        (BUTTON_X2, BUTTON_Y * 1, change_is_increase_food_time, 'Увеличение времени создание еды от количества еды', False, is_increase_food_time, 'Увеличивает скорость появления еды для змейки в зависимости от количества её', 'self'),
        (BUTTON_X2, BUTTON_Y * 2, change_can_crash_wall, 'Врезаться в стены', False, can_crash_wall, 'Позволяет змейки проходить через стены', 'self'),
        (BUTTON_X2, BUTTON_Y * 3, change_can_crash_self, 'Врезаться в себя', False, can_crash_self, 'Позволяет змейки проходить через себя', 'self'),
        (BUTTON_X2 - BUTTON_WIDTH // 8, BUTTON_Y * 4, change_size_window, f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}', False, None, str_sizes, 'self', BUTTON_WIDTH - BUTTON_WIDTH // 4),
        (BUTTON_X2 + BUTTON_WIDTH / 2.5 - GAP // 2, BUTTON_Y * 4, increase_size_window, '/\\', False, None, str_sizes, 'self', BUTTON_WIDTH // 4 - GAP),
        (BUTTON_X2, BUTTON_Y * 5, reset_record, 'Сбросить рекорд', False,  None, 'Сбрасывает лучший результат'),
        ((BUTTON_X - BUTTON_WIDTH // 4) // 2, BUTTON_Y * 2, None, 'Вы уверенны?', False, None, None, None, None, None, None, None, False),
        ((BUTTON_X - BUTTON_WIDTH / 4 - BUTTON_WIDTH / 2 - GAP / 2) / 2, BUTTON_Y * 3, activate, 'Да', False, None, None, None, (BUTTON_WIDTH - GAP) / 2),
        ((BUTTON_X - BUTTON_WIDTH / 4 + BUTTON_WIDTH / 2 + GAP / 2) / 2, BUTTON_Y * 3, hide_choice_button, 'Нет', False, None, None, None, (BUTTON_WIDTH - GAP) / 2),
    )

    button_start = Button(*BUTTONS_DATA[0])
    button_difficulty = Button(*BUTTONS_DATA[1])
    button_show_settings = Button(*BUTTONS_DATA[2])
    button_exit = Button(*BUTTONS_DATA[3])
    button_increase = Button(*BUTTONS_DATA[4])
    button_can_wall = Button(*BUTTONS_DATA[5])
    button_can_self = Button(*BUTTONS_DATA[6])
    button_change_size = Button(*BUTTONS_DATA[7])
    button_increase_size = Button(*BUTTONS_DATA[8])
    button_reset_record = Button(*BUTTONS_DATA[9])
    button_no = Button(*BUTTONS_DATA[-1])
    button_yes = Button(*BUTTONS_DATA[-2])
    button_choice = Button(*BUTTONS_DATA[-3])

    button_reset_record.parameters = (button_yes,)

    setting_buttons = (button_increase, button_can_wall, button_can_self, button_change_size, button_increase_size, button_reset_record)
    choice_buttons = (button_choice, button_no, button_yes)
    buttons = (button_start, button_difficulty, button_show_settings, button_exit) + setting_buttons + choice_buttons


    def show_text(text, x, y, width, height, color=BUTTON_TEXT_COLOR, centered_x=True, centered_y=True):
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
            elif len(word) + sum(map(len, lines[count])) + len(lines[count]) > width / WINDOW_WIDTH * 100:
                count += 1
                lines.append([word])
            else:
                lines[count].append(word)

        gap = (height - count * SIZE_FONT) // 2
        for i, line in enumerate(lines):
            text_line = FONT.render(' '.join(line), True, color)
            pos = (x - (text_line.get_width() // 2 * centered_x), y + (gap * centered_y) - SIZE_FONT // 2 + i * SIZE_FONT)
            window.blit(text_line, pos)


    while True:
        pygame.time.Clock().tick(FPS)
        window.fill(WINDOW_COLOR)

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
                    button.change_active()
                    if button.additional_text is not None:
                        show_text(button.additional_text, GAP * 2, BUTTON_Y - BUTTON_HEIGHT // 2,
                                  BUTTON_WIDTH, BUTTON_HEIGHT * 3, TEXT_COLOR, False, False)

                pygame.draw.rect(window, ACTIVATED_BUTTON_COLOR, button.frame)
                pygame.draw.rect(window, button.color, button.rect)
                show_text(button.text, button.position[0], button.rect.y, button.width, button.height)

        score_text = FONT.render(f'Рекорд: {score}', True, TEXT_COLOR)
        window.blit(score_text, (GAP, GAP))

        pygame.display.update()


if __name__ == '__main__':
    new_loop()
