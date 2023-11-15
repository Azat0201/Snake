import pygame


class Button:
    width_class = None
    height_class = None
    gap_class = None
    color_class = None
    activated_color_class = None

    def __init__(self, x, y, function=None, text=None, visible=True, activator=None, additional_text=None,
                 parameters=None, width=None, height=None, gap=None, color=None, activated_color=None):
        if text is None:
            text = ''
        if visible is None:
            visible = True
        if parameters is None:
            parameters = ()
        for par in ('width', 'height', 'gap', 'color', 'activated_color'):
            if eval(par) is None:
                value = self.__class__.__dict__[par + '_class']
            else:
                value = eval(par)
            self.__dict__['_' + par] = value
        self._active = False
        self._visible = visible
        self._rect = pygame.Rect(x - self._width // 2, y - self._height // 2, self._width - self._gap // 2, self._height - self._gap // 2)
        self._frame = pygame.Rect(x - self._width // 2, y - self._height // 2, self._width, self._height)
        self._function = function
        self._text = text
        self._additional_text = additional_text
        self._parameters = (self,) if parameters == 'self' else parameters
        self._activator = activator
        self._position = x, y

    def use_function(self):
        if self._function:
            self._function(*self._parameters)

    @property
    def color(self):
        if not self._function:
            return self._color
        active = self._active
        self._active = False
        return self._activated_color if self._activator or active else self._color

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

    def change_active(self):
        self._active = not self._active

    def change_visible(self):
        self._visible = not self._visible
