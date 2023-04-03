from common_imports import *

class EventHolder :
    LANGUAGE_PERSIAN = -1
    LANGUAGE_ENGLISH = 1

    def __init__( self,check_exit=True ) :
        self.pressed_keys = []
        self.released_keys = []
        self.held_keys = []
        self.check_exit = check_exit

        self.mouse_moved = False
        self.mouse_pos = Pos(0, 0)
        self.mouse_pressed_keys = [False, False, False]
        self.mouse_released_keys = [False, False, False]
        self.mouse_held_keys = [False, False, False]
        self.mouse_focus = False

        self.is_dev = False
        self.should_render_debug = False
        self.should_run_game = False
        self.should_quit = False
        self.game_over = False
        self.determined_fps = 60
        self.menu_fps = 25
        self.final_fps = 0
        self.current_level = 1
        self.language = EventHolder.LANGUAGE_ENGLISH


    def get_events( self ) :
        self.pressed_keys.clear()
        self.released_keys.clear()
        self.mouse_pressed_keys = [False, False, False]
        self.mouse_released_keys = [False, False, False]
        self.mouse_focus = pg.mouse.get_focused()
        self.mouse_moved = False



        for i in pg.event.get() :
            if i.type == WINDOWENTER or MOUSEMOTION :
                self.mouse_pos = Pos(pg.mouse.get_pos())

            if self.check_exit:
                if i.type == QUIT or i.type == KEYDOWN and i.key == K_ESCAPE:
                    self.should_quit = True

            if i.type == MOUSEMOTION :
                self.mouse_moved = True

            if i.type == KEYDOWN :
                self.pressed_keys.append(i.key)
                if i.key not in self.held_keys :
                    self.held_keys.append(i.key)

            if i.type == KEYUP :
                self.released_keys.append(i.key)
                if i.key in self.held_keys :
                    self.held_keys.remove(i.key)

            if i.type == MOUSEBUTTONDOWN :
                self.mouse_pressed_keys = list(pg.mouse.get_pressed())
                self.mouse_held_keys = list(pg.mouse.get_pressed())

            if i.type == MOUSEBUTTONUP :
                self.mouse_released_keys = list(pg.mouse.get_pressed())
                self.mouse_held_keys = list(pg.mouse.get_pressed())


event_holder = EventHolder()