from common_names import *
from common_resources import *

from board import Board

class Game:
    def __init__(self):
        s = Holder.window.size
        x_scale = 1
        y_scale = 1

        if s.x < s.y:
            y_scale = s.x / s.y
        elif s.x > s.y:
            x_scale = s.y / s.x

        board_size = Pos(s.x*x_scale,s.y*y_scale)
        new_rect = FRect(0,0,board_size.x,board_size.y)
        new_rect.center = Holder.window.center

        self.board = Board(new_rect)


    def check_events( self ):
        self.board.check_events()

    def render( self,surface:Surface ):
        self.board.render(surface)