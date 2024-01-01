import pygame


class Button:
    width_class = None
    height_class = None
    gap_class = None
    color_class = None
    activated_color_class = None

    def __init__(self, x, y, function=None, text=None, visible=True, active=None, additional_text=None,
                 parameters=None, width=None, height=None, gap=None, color=None, activated_color=None):
        if text is None:
            text = ''
        if visible is None:
            visible = True
        if parameters is None:
            parameters = ()
        if width is None:
            width = self.__class__.width_class
        if height is None:
            height = self.__class__.height_class
        if gap is None:
            gap = self.__class__.gap_class
        if color is None:
            color = self.__class__.color_class
        if activated_color is None:
            activated_color = self.__class__.activated_color_class

        self._function = function
        self._text = text
        self._visible = visible
        self._active = active
        self._additional_text = additional_text
        self._parameters = (self,) if parameters == 'self' else parameters
        self._width = width
        self._height = height
        self._gap = gap
        self._color = color
        self._activated_color = activated_color

        self._pressed = False
        self._rect = pygame.Rect(x - self._width // 2, y - self._height // 2, self._width - self._gap // 2, self._height - self._gap // 2)
        self._frame = pygame.Rect(x - self._width // 2, y - self._height // 2, self._width, self._height)
        self._position = x, y

    def use_function(self):
        if self._function:
            self._function(*self._parameters)

    @property
    def color(self):
        if not self._function:
            return self._color
        active = self._pressed
        self._pressed = False
        return self._activated_color if self._active or active else self._color

    @property
    def rect(self):
        return self._rect

    @property
    def frame(self):
        return self._frame

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, other_text):
        self._text = other_text

    @property
    def additional_text(self):
        return self._additional_text

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, other_parameters):
        self._parameters = other_parameters
        
    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, other_function):
        self._function = other_function

    @property
    def position(self):
        return self._position

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, other):
        if isinstance(other, bool) or other is None:
            self._visible = other

    def change_pressed(self):
        self._pressed = True

    def change_visible(self):
        self._visible = not self._visible
