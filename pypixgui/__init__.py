import os
from sys import exit as exit_
from time import sleep as time_sleep
from urllib.request import urlretrieve as download_file
from pynput import mouse as py_mouse
from pyautogui import position as get_real_mouse_pos
from pyautogui import size as get_screen_size
from mss import mss as mss_sct
from ctypes import c_long, pointer


load_our_sdl2 = True
if load_our_sdl2:
    import pypixgui.mysdl2xd as sdl2
    import pypixgui.mysdl2xd.ext as ext
    from pypixgui.mysdl2xd.sdlttf import *
    sdl2.ext = ext
    from pypixgui.mysdl2xd.sdlttf import *
else:
    import sdl2
    import sdl2.ext
    from sdl2.sdlttf import *


from threading import Thread as NewThread
from PIL.Image import open as open_image
from PIL.Image import frombytes as open_image_from_bytes
from PIL.Image import new as create_image
from PIL import ImageDraw as NewImageDraw
from PIL import ImageFont as NewImageFont

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'True'

from pygame import cursors
from pygame.mouse import set_cursor as set_new_cursor
if not os.name == 'nt':
    import pygame
    pygame.init()
    del pygame


sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
TTF_Init()
w, h = get_screen_size()


enable_win_functions = False
if os.name == 'nt' and 'PYPIX_DISABLE_WIN_FUNCTIONS' not in os.environ:
    enable_win_functions = True
    try:
        from win32gui import EnumWindows as NewEnumWindows
        from win32gui import GetWindowText as GetHwndText
        from win32gui import IsWindowVisible as VisibleWindow
    except ImportError:
        print('Can\'t import pywin32')
        exit_(-1)
__module__ = os.path.dirname(__file__)
if not os.path.isdir(os.path.join(__module__, 'borders', 'xp')) or\
        not os.access(os.path.join(__module__, 'borders', 'xp', 'close.bmp'), os.F_OK)\
        and '__NO_AUTO_DOWNLOAD' not in os.environ:
    print('XP Border is not exists, downloading...')
    borders_to_download = [
        'close.bmp', 'close_click.bmp', 'close_hover.bmp', 'close_out.bmp', 'max.bmp',
        'max_click.bmp', 'max_hover.bmp', 'max_out.bmp', 'min.bmp', 'min_click.bmp', 'min_hover.bmp', 'min_out.bmp',
        'res.bmp', 'res_click.bmp', 'res_hover.bmp', 'res_out.bmp', 'temp_icon.bmp', 'temp_icon.ico',
        'v_center_down.bmp', 'v_center_top1.bmp', 'v_center_top1_max.bmp', 'v_center_top2.bmp',
        'v_center_top2_max.bmp', 'v_center_top3.bmp', 'v_center_top3_max.bmp', 'v_left_center.bmp',
        'v_left_down.bmp', 'v_left_top.bmp', 'v_right_center.bmp', 'v_right_down.bmp', 'v_right_top.bmp',
        'v_left_top.png', 'v_right_top.png'
    ]
    os.makedirs(os.path.join(__module__, 'borders'), exist_ok=True)
    os.makedirs(os.path.join(__module__, 'borders', 'xp'), exist_ok=True)
    for i in borders_to_download:
        download_file(
            f'https://github.com/Pixelsuft/pypixgui/raw/main/pypixgui/borders/xp/{i}',
            os.path.join(__module__, 'borders', 'xp', i)
        )
sct = mss_sct()
print_log_len = 20
print_log_text_len = None
try:
    print_log_text_len = 100 if os.get_terminal_size()[1] > 100 else 50
except OSError:
    print_log_text_len = 50
temp_path = os.environ['TEMP'] if os.name == 'nt' else __module__
temp_files = []
sdl2.ext.init()
cursors.sizer_yx_strings = (
    '     XXXXXXXX           ',
    '      X.....X           ',
    '       X....X           ',
    '        X...X           ',
    '       X.X..X           ',
    '      X.X X.X           ',
    'X    X.X   XX           ',
    'XX  X.X     X           ',
    'X.XX.X                  ',
    'X...X                   ',
    'X...X                   ',
    'X....X                  ',
    'X.....X                 ',
    'XXXXXXXX                ',
    '                        ',
    '                        ',
)


class NewImage:
    def __init__(self, type_id, window, path, pos=(0, 0)):
        self.img = window.factory.from_image(path)
        self.type = 'image'
        self.id = type_id
        self.left = pos[0]
        self.top = pos[1]
        self.width = self.img.size[0]
        self.height = self.img.size[1]
        self.mouse_on_me = False
        self.enabled = True
        window.objects.append(self)
        super(NewImage, self).__init__()

    def draw(self, window, ignore_out=False):
        if not ignore_out:
            if self.left <= 0:
                self.left = 0
            if self.left + self.width > window.client_width:
                self.left = window.client_width - self.width
            if self.top <= 0:
                self.top = 0
            if self.top + self.height > window.client_height:
                self.top = window.client_height - self.height
        renderer = window.factory.create_sprite_render_system(window.window)
        renderer.render(self.img, x=window.get_left(self.left), y=window.get_top(self.top))


class NewButton:
    def __init__(self, type_id, window, text='', pos=(0, 0), size=(40, 40)):
        self.type = 'button'
        self.id = type_id
        self.left = pos[0]
        self.top = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.enabled = True
        self.mouse_on_me = False
        self.text = text
        self.border_color = sdl2.SDL_Color(173, 173, 173)
        self.color = sdl2.SDL_Color(221, 221, 221)
        self.hover_border_color = sdl2.SDL_Color(0, 120, 215)
        self.hover_color = sdl2.SDL_Color(229, 241, 251)
        self.click_border_color = sdl2.SDL_Color(0, 86, 157)
        self.click_color = sdl2.SDL_Color(205, 229, 247)
        self.disabled_border_color = sdl2.SDL_Color(191, 191, 191)
        self.disabled_color = sdl2.SDL_Color(204, 204, 204)
        window.objects.append(self)
        super(NewButton, self).__init__()

    def draw(self, window, ignore_out=False):
        if not ignore_out:
            if self.left <= 0:
                self.left = 0
            if self.left + self.width > window.client_width:
                self.left = window.client_width - self.width
            if self.top <= 0:
                self.top = 0
            if self.top + self.height > window.client_height:
                self.top = window.client_height - self.height
        surface = window.window.get_surface()
        color = (self.border_color, self.color)
        if self.enabled:
            if window.mouse_is_down and self.id == window.clicked_object:
                color = (self.click_border_color, self.click_color)
            elif window.cur_obj == self.id:
                color = (self.hover_border_color, self.hover_color)
        else:
            color = (self.disabled_border_color, self.disabled_color)
        sdl2.ext.fill(
            surface,
            color[0],
            (window.get_left(self.left), window.get_top(self.top), self.width, self.height)
        )
        sdl2.ext.fill(
            surface,
            color[1],
            (window.get_left(self.left) + 1, window.get_top(self.top) + 1, self.width - 2, self.height - 2)
        )


class NewEmpty:
    def __init__(self, type_id, window, pos=(0, 0), size=(40, 40)):
        self.type = 'empty'
        self.id = type_id
        self.left = pos[0]
        self.top = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.enabled = True
        self.mouse_on_me = False
        window.objects.append(self)
        super(NewEmpty, self).__init__()


class NewLabel:
    def __init__(self, type_id, window, pos=(0, 0)):
        self.type = 'label'
        self.id = type_id
        self.left = pos[0]
        self.top = pos[1]
        self.width = 0
        self.height = 0
        self.text = 'Hallow, Worlds!'
        self.font = 'arial.ttf'
        self.stream = None
        self.font_size = 25
        self.color = (0, 255, 0)
        self.img_path = None
        self.mouse_on_me = False
        self.enabled = True
        self.stroke = None
        self.stroke_width = 0
        window.objects.append(self)
        super(NewLabel, self).__init__()

    def update_cache(self, fix_width=0, fix_height=0):
        fnt = NewImageFont.truetype(self.font, self.font_size)
        self.width, self.height = NewImageDraw.Draw(create_image('RGBA', (0, 0))).textsize(
            text=self.text,
            font=fnt
        )
        img = create_image('RGBA', (self.width + fix_width, self.height + fix_height))
        d = NewImageDraw.Draw(img)
        d.text(
            (0, 0),
            self.text,
            fill=self.color,
            stroke_width=self.stroke_width,
            stroke_fill=self.stroke,
            font=fnt
        )
        self.img_path = os.path.join(temp_path, f'pypixgui_{len(temp_files)}.png')
        temp_files.append(self.img_path)
        if os.access(self.img_path, os.F_OK):
            os.remove(self.img_path)
        img.save(self.img_path, 'PNG')

    def open_stream(self, window):
        self.stream = window.factory.from_image(self.img_path)

    def draw(self, window):
        r = window.factory.create_sprite_render_system(window.window)
        r.render(self.stream, x=self.left, y=self.top)


class NewWindow:
    def __init__(self, **kwargs):
        self.flags = sdl2.SDL_WINDOW_RESIZABLE
        self.title = 'PyPix GUI!'
        self.temp_screen = screen_shot()
        self.window = sdl2.ext.Window(self.title, size=(640, 480), flags=self.flags)
        self.use_border_radius = False
        self.last_size = (0, 0)
        self.last_pos = (0, 0)
        self.width = 0
        self.height = 0
        self.left = 0
        self.top = 0
        self.client_width = 0
        self.client_height = 0
        self.enabled = True
        self.mouse_in_window = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.id = 'self'
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.full_mouse_x = 0
        self.full_mouse_y = 0
        self.last_real_x = 0
        self.last_real_y = 0
        self.min_width = 320
        self.min_height = 200
        self.max_width = 0
        self.max_height = 0
        self.mouse_is_moving = False
        self.window_focused = True
        self.default_cursor = cursors.arrow
        self.icons_buttons = ['close', 'maximize', 'restore', 'minimize']
        self.background_color = sdl2.ext.Color(236, 233, 216)
        self.factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        self.border_path_dir = get_borders_path('xp')
        self.border_path = sdl2.ext.Resources(self.border_path_dir)
        self.border = 'default'
        self.looping_check_focus = False
        self.is_maximized = False
        self.for_maximize = (0, 0, 0, 0)
        self.before_maximize = (0, 0, 0, 0)
        self.test_maximize()
        self.cur_obj = 'self'
        self.objects = []
        self.border_icons = self.load_icons(self.border_path)
        self.processor = sdl2.ext.TestEventProcessor()
        self.mouse_is_down = False
        self.last_click = False
        self.trans = (
            5,
            3,
            2,
            1,
            1
        )
        self.clicked_object = 'self'
        self.enum_first = False
        self.looping = False
        self.current_border = ''
        self.cur_icon = ''
        self.icons_pos = {
            'close': 0,
            'maximize': 0,
            'restore': 0,
            'minimize': 0
        }
        self.set_cursor(self.default_cursor)
        self.py_mouse_listener = py_mouse.Listener(
            on_click=self.python_mouse_event,
        )
        self.py_mouse_listener.start()
        super(NewWindow, self).__init__(**kwargs)

    def center_window(self):
        self.window.position = (
            int(w / 2 - self.window.size[0] / 2),
            int(h / 2 - self.window.size[1] / 2)
        )

    def del_object(self, obj_id):
        log(self.objects)
        for i in self.objects:
            if i.id == obj_id:
                self.objects.remove(i)
                break

    def enum_handler(self, hwnd, ctx):
        if self.enum_first and VisibleWindow(hwnd):
            strip_text = GetHwndText(hwnd).strip()
            if strip_text:
                self.enum_first = False
                if GetHwndText(hwnd).strip() == self.title.strip():
                    if not self.window_focused:
                        self.window_focused = True
                        if self.use_border_radius:
                            try:
                                self.draw_border_radius(self.window.get_surface())
                            except sdl2.ext.common.SDLError:
                                pass
                        self.on_focus_enter()
                elif self.window_focused:
                    self.window_focused = False
                    if self.use_border_radius:
                        try:
                            screen_shot()
                        except sdl2.ext.common.SDLError:
                            pass
                    self.on_focus_leave()

    def test_maximize(self):
        self.maximize()
        self.for_maximize = (
            self.window.position[0],
            self.window.position[1],
            self.window.size[0],
            self.window.size[1],
        )
        self.window.test_restore()
        if self.for_maximize[1] == 23:
            self.for_maximize = (
                self.for_maximize[0],
                0,
                self.for_maximize[2],
                self.for_maximize[3] + 23
            )

    def __focus_check(self):
        while self.looping_check_focus:
            self.enum_first = True
            NewEnumWindows(self.enum_handler, None)

    def check_focused(self):
        if enable_win_functions:
            self.looping_check_focus = True
            NewThread(target=self.__focus_check).start()

    def break_focus_check(self):
        self.looping_check_focus = False

    def load_icons(self, icons_path):
        result = (
            4,
            30,
            26,
            4,
            4,
            self.factory.from_image(icons_path.get_path("close.bmp")),
            self.factory.from_image(icons_path.get_path("close_hover.bmp")),
            self.factory.from_image(icons_path.get_path("close_click.bmp")),
            self.factory.from_image(icons_path.get_path("max.bmp")),
            self.factory.from_image(icons_path.get_path("max_hover.bmp")),
            self.factory.from_image(icons_path.get_path("max_click.bmp")),
            self.factory.from_image(icons_path.get_path("res.bmp")),
            self.factory.from_image(icons_path.get_path("res_hover.bmp")),
            self.factory.from_image(icons_path.get_path("res_click.bmp")),
            self.factory.from_image(icons_path.get_path("min.bmp")),
            self.factory.from_image(icons_path.get_path("min_hover.bmp")),
            self.factory.from_image(icons_path.get_path("min_click.bmp")),
            self.factory.from_image(icons_path.get_path("v_left_top.bmp")),
            self.factory.from_image(icons_path.get_path("v_center_top1.bmp")),
            [],
            self.factory.from_image(icons_path.get_path("v_center_top3.bmp")),
            self.factory.from_image(icons_path.get_path("v_right_top.bmp")),
            [],
            [],
            self.factory.from_image(icons_path.get_path("v_left_down.bmp")),
            [],
            self.factory.from_image(icons_path.get_path("v_right_down.bmp")),
            self.factory.from_image(icons_path.get_path("v_center_top1_max.bmp")),
            [],
            self.factory.from_image(icons_path.get_path("v_center_top3_max.bmp")),
            self.factory.from_image(icons_path.get_path("v_left_top.png")),
            self.factory.from_image(icons_path.get_path("v_right_top.png"))
        )
        v_center_top2_max = open_image(icons_path.get_path('v_center_top2_max.bmp')).convert('RGB')
        v_center_top2 = open_image(icons_path.get_path('v_center_top2.bmp')).convert('RGB')
        v_left_center = open_image(icons_path.get_path('v_left_center.bmp')).convert('RGB')
        v_right_center = open_image(icons_path.get_path('v_right_center.bmp')).convert('RGB')
        v_center_down = open_image(icons_path.get_path('v_center_down.bmp')).convert('RGB')
        for i in range(26):
            r, g, b = v_center_top2_max.getpixel((1, i))[:3]
            result[28].append(
                sdl2.ext.Color(r, g, b)
            )
        for i in range(30):
            r, g, b = v_center_top2.getpixel((1, i))[:3]
            result[19].append(
                sdl2.ext.Color(r, g, b)
            )
        for i in range(4):
            r1, g1, b1 = v_left_center.getpixel((i, 1))[:3]
            r2, g2, b2 = v_right_center.getpixel((i, 1))[:3]
            result[22].append(
                sdl2.ext.Color(r1, g1, b1)
            )
            result[23].append(
                sdl2.ext.Color(r2, g2, b2)
            )
        for i in range(4):
            r, g, b = v_center_down.getpixel((1, i))[:3]
            result[25].append(
                sdl2.ext.Color(r, g, b)
            )
        return result

    def set_border(self, new_border):
        new_border_lower = new_border.lower()
        if new_border_lower in ['none', 'themed', 'default']:
            self.border = new_border_lower
        else:
            log(f'Unknown border type: {new_border}', 'Error')

    def set_size(self, *args):
        if type(*args) == str:
            split_size = str(*args).strip().replace(' ', '').replace(',', 'x').split('x')
            self.window.size = (int(split_size[0]), int(split_size[1]))
        else:
            log('Size must be a string, for example: \'800x600\'', 'Error')

    def set_cursor(self, cursor_name, zero_pos=False):
        if type(cursor_name[0]) == str:
            set_new_cursor(
                (len(cursor_name[0]), len(cursor_name)),
                (0, 0) if zero_pos else(int(len(cursor_name[0]) / 3), int(len(cursor_name) / 3)),
                *cursors.compile(cursor_name, black='.', white='X', xor='o')
            )
        else:
            set_new_cursor(*cursor_name)

    def program_screenshot(self, return_pillow=True):
        monitor = {
            'left': self.get_left(self.left),
            'top': self.get_top(self.top),
            'width': self.client_width,
            'height': self.client_height
        }
        screenshot = sct.grab(monitor)
        if return_pillow:
            return open_image_from_bytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        else:
            return screenshot

    def reset(self, flags='Use default flags.'):
        if flags == 'Use default flags.':
            flags = self.flags
        self.flags = flags
        self.window = sdl2.ext.Window(
            self.window.title, size=self.window.size, position=self.window.position, flags=self.flags
        )

    def get_left(self, old_left):
        if self.border == 'themed' and not self.is_maximized:
            return old_left + self.border_icons[0]
        else:
            return old_left

    def get_top(self, old_top):
        if self.border == 'themed':
            if self.is_maximized:
                return old_top + self.border_icons[2]
            else:
                return old_top + self.border_icons[1]
        else:
            return old_top

    def set_title(self, args):
        self.title = args
        self.window.title = self.title

    def show(self):
        self.window.show()

    def hide(self):
        self.window.hide()

    def maximize(self):
        self.is_maximized = True
        self.window.maximize()

    def minimize(self):
        self.window.minimize()

    def restore(self):
        self.window.test_restore()
        self.is_maximized = False

    def on_resize(self, size, pos):
        log(f'Change Size: {size[0]}x{size[1]}')

    def on_repos(self, pos, size):
        log(f'Change Position: {pos[0]}x{pos[1]}')

    def on_close(self):
        log('Close')
        self.break_loop()
        self.break_focus_check()

    def on_maximize(self):
        self.before_maximize = (
            self.window.position[0],
            self.window.position[1],
            self.window.size[0],
            self.window.size[1]
        )
        self.window.position = (
            self.for_maximize[0],
            self.for_maximize[1]
        )
        self.window.size = (
            self.for_maximize[2],
            self.for_maximize[3]
        )
        self.is_maximized = True
        self.draw()
        self.draw_border()
        log('Maximize')

    def on_restore(self):
        self.window.position = (
            self.before_maximize[0],
            self.before_maximize[1]
        )
        self.window.size = (
            self.before_maximize[2],
            self.before_maximize[3]
        )
        self.is_maximized = False
        self.draw()
        self.draw_border()
        log('Restore')

    def on_minimize(self):
        log('Minimize')
        self.minimize()

    def on_focus_enter(self):
        log('Focus Enter')

    def on_focus_leave(self):
        log('Focus Leave')

    def on_mouse_enter(self, obj_id, pos):
        log(f'Mouse Enter ({obj_id}): {pos[0]}x{pos[1]}')

    def on_mouse_leave(self, obj_id, pos):
        log(f'Mouse Leave ({obj_id}): {pos[0]}x{pos[1]}')

    def on_mouse_move(self, obj_id, pos):
        log(f'Mouse Move ({obj_id}): {pos[0]}x{pos[1]}, Last: {self.last_mouse_x}x{self.last_mouse_y}')

    def on_mouse_down(self, obj_id, pos):
        log(f'Mouse Down ({obj_id}): {pos[0]}x{pos[1]}')

    def on_mouse_up(self, obj_id, pos):
        log(f'Mouse Up ({obj_id}): {pos[0]}x{pos[1]}')

    def sleep_double_click(self):
        time_sleep(5)
        self.last_click = False

    def python_mouse_event(self, x, y, button, pressed):
        if not pressed:
            if self.mouse_is_down:
                self.mouse_button_up()
            return False

    def check_mouse(self):
        real_pos_x, real_pos_y = get_real_mouse_pos()
        pos_x = real_pos_x - self.left
        pos_y = real_pos_y - self.top
        self.full_mouse_x = pos_x
        self.full_mouse_y = pos_y
        if self.border == 'themed':
            pos_x -= self.border_icons[0]
            if self.is_maximized:
                pos_y -= self.border_icons[2]
            else:
                pos_y -= self.border_icons[1]
        temp_wh = (
            self.width - self.border_icons[3] if self.border == 'themed' else self.width,
            self.height - self.border_icons[4] if self.border == 'themed' else self.height
        )
        if self.border == 'themed':
            border_updated = False
            if not self.mouse_is_down:
                if self.cur_icon == 'close_click':
                    self.on_close()
                if self.cur_icon == 'max_click':
                    self.on_maximize()
                if self.cur_icon == 'res_click':
                    self.on_restore()
                if self.cur_icon == 'min_click':
                    self.on_minimize()
            all_y = 6
            if self.is_maximized:
                all_y = 2
            if 'close' in self.icons_buttons and all_y <= self.full_mouse_y <= \
                    21 + all_y and self.icons_pos['close'] + 21 >= self.full_mouse_x >= self.icons_pos['close']:
                if not self.cur_icon == 'close_hover' and not self.mouse_is_down:
                    self.cur_icon = 'close_hover'
                    border_updated = True
            elif 'maximize' in self.icons_buttons and all_y <= self.full_mouse_y <= \
                    21 + all_y and self.icons_pos['maximize'] + 21 >= self.full_mouse_x >= self.icons_pos['maximize']:
                if not self.cur_icon == 'maximize_hover' and not self.mouse_is_down:
                    self.cur_icon = 'max_hover'
                    border_updated = True
            elif 'restore' in self.icons_buttons and all_y <= self.full_mouse_y <= \
                    21 + all_y and self.icons_pos['restore'] + 21 >= self.full_mouse_x >= self.icons_pos['restore']:
                if not self.cur_icon == 'res_hover' and not self.mouse_is_down:
                    self.cur_icon = 'res_hover'
                    border_updated = True
            elif 'minimize' in self.icons_buttons and all_y <= self.full_mouse_y <= \
                    21 + all_y and self.icons_pos['minimize'] + 21 >= self.full_mouse_x >= self.icons_pos['minimize']:
                if not self.cur_icon == 'min_hover' and not self.mouse_is_down:
                    self.cur_icon = 'min_hover'
                    border_updated = True
            else:
                if self.is_maximized:
                    if self.full_mouse_y <= 26:
                        self.current_border = 'maximize_top'
                        self.set_cursor(cursors.arrow)
                        can_set_default = False
                    if self.mouse_is_down and self.current_border == 'maximize_top' and self.mouse_is_moving:
                        last_x1 = self.window.position[0]
                        last_y1 = self.window.position[1]
                        last_x2 = real_pos_x - last_x1
                        last_y2 = real_pos_y - last_y1
                        self.restore()
                        self.on_restore()
                        self.window.position = (
                            real_pos_x - last_x2 if last_x2 < self.window.size[0] else self.window.size[0] - 30,
                            real_pos_y - last_y2 if last_y2 < self.window.size[1] else self.window.size[1] - 30
                        )
                        self.current_border = 'center_top_move'
                else:
                    if self.mouse_is_down:
                        tmp_x = real_pos_x - self.last_real_x
                        tmp_y = real_pos_y - self.last_real_y
                        if self.current_border == 'left_center':
                            self.window.size = (self.window.size[0] - tmp_x, self.window.size[1])
                            self.window.position = (self.window.position[0] + tmp_x, self.window.position[1])
                        elif self.current_border == 'right_center':
                            self.window.size = (self.window.size[0] + tmp_x, self.window.size[1])
                            if tmp_x < 0:
                                self.draw_border(only_border=True)
                        elif self.current_border == 'center_top':
                            self.window.size = (self.window.size[0], self.window.size[1] - tmp_y)
                            self.window.position = (self.window.position[0], self.window.position[1] + tmp_y)
                        elif self.current_border == 'center_down':
                            self.window.size = (self.window.size[0], self.window.size[1] + tmp_y)
                        elif self.current_border == 'left_top':
                            self.window.size = (self.window.size[0] - tmp_x, self.window.size[1])
                            self.window.position = (self.window.position[0] + tmp_x, self.window.position[1])
                            self.window.size = (self.window.size[0], self.window.size[1] - tmp_y)
                            self.window.position = (self.window.position[0], self.window.position[1] + tmp_y)
                        elif self.current_border == 'right_down':
                            self.window.size = (self.window.size[0] + tmp_x, self.window.size[1])
                            self.window.size = (self.window.size[0], self.window.size[1] + tmp_y)
                            if tmp_x < 0:
                                self.draw_border(only_border=True)
                        elif self.current_border == 'right_top':
                            self.window.size = (self.window.size[0] + tmp_x, self.window.size[1])
                            self.window.size = (self.window.size[0], self.window.size[1] - tmp_y)
                            self.window.position = (self.window.position[0], self.window.position[1] + tmp_y)
                            if tmp_x < 0:
                                self.draw_border(only_border=True)
                        elif self.current_border == 'left_down':
                            self.window.size = (self.window.size[0] - tmp_x, self.window.size[1])
                            self.window.position = (self.window.position[0] + tmp_x, self.window.position[1])
                            self.window.size = (self.window.size[0], self.window.size[1] + tmp_y)
                        elif self.current_border == 'center_top_move':
                            self.window.position = (self.window.position[0] + tmp_x, self.window.position[1])
                            self.window.position = (self.window.position[0], self.window.position[1] + tmp_y)
                    else:
                        if self.full_mouse_x <= 4 and 30 < self.full_mouse_y < self.height - 4 and not border_updated:
                            self.current_border = 'left_center'
                            self.set_cursor(cursors.sizer_x_strings)
                            can_set_default = False
                        elif self.full_mouse_x >= self.width - 4 and not border_updated and\
                                30 < self.full_mouse_y < self.height - 4:
                            self.current_border = 'right_center'
                            self.set_cursor(cursors.sizer_x_strings)
                            can_set_default = False
                        elif self.full_mouse_x <= 5 and self.full_mouse_y <= 30 and not border_updated:
                            self.current_border = 'left_top'
                            self.set_cursor(cursors.sizer_xy_strings)
                            can_set_default = False
                        elif self.full_mouse_y <= 30 and self.full_mouse_x >= self.width - 5:
                            self.current_border = 'right_top'
                            self.set_cursor(cursors.sizer_yx_strings)
                            can_set_default = False
                        elif self.full_mouse_y <= 10:
                            self.current_border = 'center_top'
                            self.set_cursor(cursors.sizer_y_strings)
                            can_set_default = False
                        elif self.full_mouse_y <= 30:
                            self.current_border = 'center_top_move'
                            self.set_cursor(cursors.arrow)
                            can_set_default = False
                        elif self.full_mouse_y >= self.height - 4 and self.full_mouse_x <= 4:
                            self.current_border = 'left_down'
                            self.set_cursor(cursors.sizer_yx_strings)
                            can_set_default = False
                        elif self.full_mouse_y >= self.height - 4 and self.full_mouse_x >= self.width - 4:
                            self.current_border = 'right_down'
                            self.set_cursor(cursors.sizer_xy_strings)
                            can_set_default = False
                        elif self.full_mouse_y >= self.height - 4:
                            self.current_border = 'center_down'
                            self.set_cursor(cursors.sizer_y_strings)
                            can_set_default = False
                        elif self.current_border:
                            self.current_border = ''
                            can_set_default = False
                if self.window.size[0] < self.min_width:
                    lets_find_plussed_law = self.window.size[0] - self.min_width
                    if 'left' in self.current_border:
                        self.window.position =\
                            (self.window.position[0] + lets_find_plussed_law, self.window.position[1])
                    self.window.size = (self.min_width, self.window.size[1])
                    self.draw_border()
                    self.draw()
                if self.window.size[1] < self.min_height:
                    lets_find_plussed_law = self.window.size[1] - self.min_height
                    self.window.size = (self.window.size[0], self.min_height)
                    if 'top' in self.current_border:
                        self.window.position =\
                            (self.window.position[0], self.window.position[1] + lets_find_plussed_law)
                    self.draw_border()
                    self.draw()
                if 0 < self.max_width < self.window.size[0]:
                    self.window.size = (self.max_width, self.window.size[1])
                    self.draw_border()
                    self.draw()
                if 0 < self.max_height < self.window.size[1]:
                    self.window.size = (self.window.size[0], self.max_height)
                    self.draw_border()
                    self.draw()
                if self.window.position[0] < 0:
                    self.window.position = (0, self.window.position[1])
                if self.window.position[1] < 0:
                    self.window.position = (self.window.position[0], 0)
                if not self.cur_icon == '' and not self.mouse_is_down:
                    self.cur_icon = ''
                    border_updated = True
            if not self.mouse_is_down and not self.current_border:
                self.set_cursor(self.default_cursor)
            if border_updated:
                self.current_border = ''
                self.set_cursor(self.default_cursor)
                self.draw_border(only_buttons=True)
        if pos_x < 0 or pos_y < 0 or pos_x > temp_wh[0] or pos_y > temp_wh[1]:
            if self.mouse_in_window:
                self.mouse_in_window = False
                self.last_mouse_x = self.mouse_x
                self.last_mouse_y = self.mouse_y
                self.mouse_x = pos_x
                self.mouse_y = pos_y
                self.mouse_is_moving = False
                if self.use_border_radius:
                    try:
                        self.draw_border_radius(self.window.get_surface())
                    except sdl2.ext.common.SDLError:
                        pass
                self.on_mouse_leave('self', (self.last_mouse_x, self.last_mouse_y))
        else:
            if not self.mouse_x == pos_x or not self.mouse_y == pos_y:
                self.last_mouse_x = self.mouse_x
                self.last_mouse_y = self.mouse_y
                self.mouse_x = pos_x
                self.mouse_y = pos_y
                self.mouse_is_moving = True
                cur_obj = 'self'
                for i in self.objects:
                    if i.left < self.mouse_x < i.left + i.width and i.top < self.mouse_y < i.top + i.height:
                        cur_obj = i.id
                self.cur_obj = cur_obj
                if self.use_border_radius:
                    self.draw_border_radius(self.window.get_surface())
                self.on_mouse_move(cur_obj, (pos_x, pos_y))
            if not self.mouse_in_window:
                self.mouse_in_window = True
                if self.use_border_radius:
                    try:
                        self.draw_border_radius(self.window.get_surface())
                    except sdl2.ext.common.SDLError:
                        pass
                self.on_mouse_enter('self', (pos_x, pos_y))
        for i in self.objects:
            if i.mouse_on_me:
                if i.enabled and not i.left < self.mouse_x < i.left + i.width or not\
                        i.top < self.mouse_y < i.top + i.height:
                    i.mouse_on_me = False
                    self.on_mouse_leave(i.id, (self.mouse_x, self.mouse_y))
            else:
                if i.enabled and i.left < self.mouse_x < i.left + i.width and i.top < self.mouse_y < i.top + i.height:
                    i.mouse_on_me = True
                    self.on_mouse_enter(i.id, (self.mouse_x, self.mouse_y))
        self.last_real_x, self.last_real_y = real_pos_x, real_pos_y

    def draw_border_radius(self, surface):
        for i in range(len(self.trans)):
            for j in range(self.trans[i]):
                try:
                    r1, g1, b1 = self.temp_screen.getpixel((self.window.position[0] + j, self.window.position[1] + i))
                    sdl2.ext.fill(
                        surface,
                        sdl2.ext.Color(r1, g1, b1),
                        (
                            j,
                            i,
                            1,
                            1
                        )
                    )
                except IndexError:
                    pass
                except sdl2.ext.common.SDLError:
                    pass
                try:
                    r2, g2, b2 = self.temp_screen.getpixel((self.window.position[0] + self.window.size[0] + j, self.window.position[1] + i))
                    sdl2.ext.fill(
                        surface,
                        sdl2.ext.Color(r2, g2, b2),
                        (
                            self.window.size[0] - j,
                            i,
                            1,
                            1
                        )
                    )
                except IndexError:
                    pass
                except sdl2.ext.common.SDLError:
                    pass

    def draw_border(self, only_buttons=False, only_border=False):
        r = self.factory.create_sprite_render_system(self.window)
        surface = self.window.get_surface()
        if self.is_maximized:
            self.icons_pos['close'] = self.icons_pos['maximize'] = \
                self.icons_pos['restore'] = self.icons_pos['minimize'] = self.width - 23
            if not only_buttons:
                r.render(self.border_icons[27], x=0, y=0)
                for i in range(26):
                    sdl2.ext.fill(
                        surface, self.border_icons[28][i], (45, i, self.width - 55, 1)
                    )
                r.render(self.border_icons[29], x=self.width - 10, y=0)
            if not only_border:
                if 'close' in self.icons_buttons:
                    if self.cur_icon == 'close_hover':
                        r.render(self.border_icons[6], x=self.icons_pos['close'], y=2)
                    elif self.cur_icon == 'close_click':
                        r.render(self.border_icons[7], x=self.icons_pos['close'], y=2)
                    else:
                        r.render(self.border_icons[5], x=self.icons_pos['close'], y=2)
                    self.icons_pos['restore'] -= 23
                    self.icons_pos['minimize'] -= 23
                if 'restore' in self.icons_buttons:
                    if self.cur_icon == 'res_hover':
                        r.render(self.border_icons[12], x=self.icons_pos['restore'], y=2)
                    elif self.cur_icon == 'res_click':
                        r.render(self.border_icons[13], x=self.icons_pos['restore'], y=2)
                    else:
                        r.render(self.border_icons[11], x=self.icons_pos['restore'], y=2)
                    self.icons_pos['minimize'] -= 23
                if self.cur_icon == 'min_hover':
                    r.render(self.border_icons[15], x=self.icons_pos['minimize'], y=2)
                elif self.cur_icon == 'min_click':
                    r.render(self.border_icons[16], x=self.icons_pos['minimize'], y=2)
                else:
                    r.render(self.border_icons[14], x=self.icons_pos['minimize'], y=2)
        else:
            self.icons_pos['close'] = self.icons_pos['maximize'] = \
                self.icons_pos['restore'] = self.icons_pos['minimize'] = self.width - 27
            if not only_buttons:
                r.render(
                    self.border_icons[30] if self.use_border_radius else self.border_icons[17], x=0, y=0
                )
                r.render(self.border_icons[18], x=5, y=0)
                for i in range(30):
                    sdl2.ext.fill(
                        surface, self.border_icons[19][i], (60, i, self.width - 95, 1)
                    )
                r.render(self.border_icons[20], x=self.width - 35, y=0)
                r.render(
                    self.border_icons[31] if self.use_border_radius else self.border_icons[21], x=self.width - 5, y=0
                )
                for i in range(4):
                    sdl2.ext.fill(
                        surface, self.border_icons[22][i], (i, 30, 1, self.height - 31)
                    )
                    sdl2.ext.fill(
                        surface, self.border_icons[23][i], (self.width - 4 + i, 30, 1, self.height - 31)
                    )
                for i in range(4):
                    sdl2.ext.fill(
                        surface, self.border_icons[25][i], (4, self.height - 4 + i, self.width - 8, 1)
                    )
                r.render(self.border_icons[24], x=0, y=self.height - 4)
                r.render(self.border_icons[26], x=self.width - 4, y=self.height - 4)
            if not only_border:
                if 'close' in self.icons_buttons:
                    if self.cur_icon == 'close_hover':
                        r.render(self.border_icons[6], x=self.icons_pos['close'], y=6)
                    elif self.cur_icon == 'close_click':
                        r.render(self.border_icons[7], x=self.icons_pos['close'], y=6)
                    else:
                        r.render(self.border_icons[5], x=self.icons_pos['close'], y=6)
                    self.icons_pos['maximize'] -= 23
                    self.icons_pos['minimize'] -= 23
                if 'maximize' in self.icons_buttons:
                    if self.cur_icon == 'max_hover':
                        r.render(self.border_icons[9], x=self.icons_pos['maximize'], y=6)
                    elif self.cur_icon == 'max_click':
                        r.render(self.border_icons[10], x=self.icons_pos['maximize'], y=6)
                    else:
                        r.render(self.border_icons[8], x=self.icons_pos['maximize'], y=6)
                    self.icons_pos['minimize'] -= 23
                if 'minimize' in self.icons_buttons:
                    if self.cur_icon == 'min_hover':
                        r.render(self.border_icons[15], x=self.icons_pos['minimize'], y=6)
                    elif self.cur_icon == 'min_click':
                        r.render(self.border_icons[16], x=self.icons_pos['minimize'], y=6)
                    else:
                        r.render(self.border_icons[14], x=self.icons_pos['minimize'], y=6)

    def async_main_loop(self):
        NewThread(target=self.main_loop).start()

    def draw(self):
        surface = self.window.get_surface()
        sdl2.ext.fill(
            surface,
            self.background_color,
            (self.get_left(0), self.get_top(0), self.client_width, self.client_height)
        )
        self.render()

    def clear(self):
        surface = self.window.get_surface()
        sdl2.ext.fill(
            surface,
            self.background_color,
            (self.get_left(0), self.get_top(0), self.client_width, self.client_height)
        )

    def render(self):
        pass

    def tick(self):
        pass

    def on_create(self):
        pass

    def main_loop(self):
        self.looping = True
        self.on_create()
        while self.looping:
            self.window.refresh()
            self.tick()
            if not self.last_size == self.window.size:
                self.last_size = self.window.size
                if self.use_border_radius:
                    self.draw_border_radius(self.window.get_surface())
                self.window_resized(self.window.size, self.window.position)
            if not self.last_pos == self.window.position:
                self.last_pos = self.window.position
                if self.use_border_radius:
                    self.draw_border_radius(self.window.get_surface())
                self.window_reposed(self.window.size, self.window.position)
            self.check_mouse()
            for event in sdl2.ext.get_events():
                if event.type == sdl2.SDL_QUIT:
                    self.on_close()
                    break
                if event.type == sdl2.SDL_WINDOWEVENT_MAXIMIZED:
                    self.is_maximized = True
                    self.on_maximize()
                if event.type == sdl2.SDL_WINDOWEVENT_RESTORED:
                    self.on_restore()
                if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    self.mouse_button_down()
                if event.type == sdl2.SDL_MOUSEBUTTONUP:
                    self.mouse_button_up()

    def break_loop(self):
        self.looping = False

    def mouse_button_down(self):
        if self.border == 'themed':
            border_updated = False
            if 'close' in self.icons_buttons and 2 <= self.full_mouse_y <= \
                    23 and self.icons_pos['close'] + 21 >= self.full_mouse_x >= self.icons_pos['close']:
                if not self.cur_icon == 'close_click':
                    self.cur_icon = 'close_click'
                    border_updated = True
            elif 'maximize' in self.icons_buttons and 2 <= self.full_mouse_y <= \
                    23 and self.icons_pos['maximize'] + 21 >= self.full_mouse_x >= self.icons_pos['maximize']:
                if not self.cur_icon == 'maximize_click':
                    self.cur_icon = 'max_click'
                    border_updated = True
            elif 'restore' in self.icons_buttons and 2 <= self.full_mouse_y <= \
                    23 and self.icons_pos['restore'] + 21 >= self.full_mouse_x >= self.icons_pos['restore']:
                if not self.cur_icon == 'res_click':
                    self.cur_icon = 'res_click'
                    border_updated = True
            elif 'minimize' in self.icons_buttons and 2 <= self.full_mouse_y <= \
                    23 and self.icons_pos['minimize'] + 21 >= self.full_mouse_x >= self.icons_pos['minimize']:
                if not self.cur_icon == 'min_click':
                    self.cur_icon = 'min_click'
                    border_updated = True
            if border_updated:
                self.mouse_is_down = True
                self.draw_border(only_buttons=True)
        self.mouse_is_down = True
        if self.mouse_in_window:
            cur_obj = 'self'
            for i in self.objects:
                if i.left < self.mouse_x < i.left + i.width and i.top < self.mouse_y < i.top + i.height:
                    cur_obj = i.id
            self.clicked_object = cur_obj
            self.on_mouse_down(cur_obj, (self.mouse_x, self.mouse_y))

    def get_obj_by_id(self, obj_id):
        obj = self if obj_id == 'self' else None
        for i in self.objects:
            if i.id == obj_id:
                obj = i
                break
        return obj

    def mouse_button_up(self):
        if self.border == 'themed':
            if self.current_border:
                self.draw_border()
                self.draw()
        if self.mouse_is_down:
            self.mouse_is_down = False
            self.on_mouse_up(self.clicked_object, (self.mouse_x, self.mouse_y))
            self.clicked_object = 'self'

    def window_reposed(self, size, pos):
        self.left = pos[0]
        self.top = pos[1]
        self.on_repos(pos, size)
        self.window.refresh()

    def window_resized(self, size, pos):
        self.width = size[0]
        self.height = size[1]
        self.client_width = size[0]
        self.client_height = size[1]
        self.on_resize(pos, size)
        if self.border == 'themed':
            if self.is_maximized:
                self.client_width = self.width
                self.client_height = self.height - 26
            else:
                self.client_width = self.width - 8
                self.client_height = self.client_height - 34
        self.draw()
        if self.border == 'themed':
            self.draw_border()
        self.window.refresh()


def create_window(*args, **kwargs):
    return NewWindow()


def close():
    for i in temp_files:
        os.remove(i)
    sdl2.ext.quit()


def get_borders_path(border_name):
    return os.path.join(__module__, 'borders', str(border_name))


def log(string_to_log, caller='Log', use_len_for_text=True):
    print(
        f'[{caller}{" " * (print_log_len - len(caller))}]:'
        f' {string_to_log}{" " * (print_log_text_len - len(str(string_to_log)))}; \n',
        end=''
    )

def screen_shot():
    screenshot = sct.grab({
        'left': 0,
        'top': 0,
        'width': w,
        'height': h
    })
    return open_image_from_bytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
