import os
from pypixgui import *
import io

MainWindow = create_window()
MainWindow.set_size(f'{800}x{600}')
MainWindow.set_title('Test')
MainWindow.use_border_radius = True
MainWindow.set_border('themed')
MainWindow.icons_buttons = ['close', 'maximize', 'restore', 'minimize']
MainWindow.center_window()
MainWindow.is_maximized = False
MainWindow.reset(sdl2.SDL_WINDOW_BORDERLESS)


mouse_down = False


def draw():
    MainWindow.get_obj_by_id('image1').draw(MainWindow)
    MainWindow.get_obj_by_id('button1').draw(MainWindow)
    MainWindow.get_obj_by_id('label1').draw(MainWindow)


def on_mouse_move(obj_id, pos):
    if mouse_down:
        elem = MainWindow.get_obj_by_id('image1')
        MainWindow.clear()
        elem.left += pos[0] - MainWindow.last_mouse_x
        elem.top += pos[1] - MainWindow.last_mouse_y
        elem.draw(MainWindow, ignore_out=False)
        MainWindow.get_obj_by_id('button1').draw(MainWindow)
        MainWindow.get_obj_by_id('label1').draw(MainWindow)


def on_mouse_down(obj_id, pos):
    global mouse_down
    if obj_id == 'image1':
        mouse_down = True
    elif obj_id == 'button1':
        MainWindow.get_obj_by_id('button1').draw(MainWindow)


def on_mouse_up(obj_id, pos):
    global mouse_down
    if obj_id == 'image1':
        mouse_down = False
    elif obj_id == 'button1':
        MainWindow.get_obj_by_id('button1').draw(MainWindow)


def on_mouse_enter(obj_id, pos):
    if obj_id == 'button1':
        MainWindow.get_obj_by_id('button1').draw(MainWindow)


def on_mouse_leave(obj_id, pos):
    if obj_id == 'button1':
        MainWindow.get_obj_by_id('button1').draw(MainWindow)


def on_create():
    if not os.access('pixelsuft.png', os.F_OK):
        download_file('https://github.com/Pixelsuft/pypixgui/raw/main/pixelsuft.png', 'pixelsuft.png')
    NewImage('image1', MainWindow, "pixelsuft.png", pos=(100, 100))
    NewButton('button1', MainWindow, pos=(200, 200), size=(100, 40))
    a = NewLabel('label1', MainWindow, pos=(100, 400))
    a.font = 'SEGOESCB.TTF'.lower()
    a.text = 'Pixelsuft LOL :DD;DDD'
    a.font_size = 30
    a.stroke_width = 2
    a.stroke = (255, 0, 0)
    a.color = (0, 162, 232)
    a.update_cache(fix_height=5, fix_width=5)
    a.open_stream(MainWindow)


MainWindow.render = draw
MainWindow.on_mouse_move = on_mouse_move
MainWindow.on_mouse_down = on_mouse_down
MainWindow.on_mouse_up = on_mouse_up
MainWindow.on_mouse_enter = on_mouse_enter
MainWindow.on_mouse_leave = on_mouse_leave
MainWindow.on_create = on_create
MainWindow.show()
MainWindow.check_focused()
MainWindow.main_loop()
close()
