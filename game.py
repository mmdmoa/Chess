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

        self.board = Board(new_rect,self)

        # Unsafe code: This code works assuming the s.x is bigger than s.y
        self.left_text = Surface([(self.rect.w - self.board.rect.w)/2,self.rect.h]) # Unsafe
        self.right_text: Optional[Surface] = None

        self.update_board_data()

    @property
    def rect( self ):
        return FRect(Holder.window.surface.get_rect())

    def update_board_data( self ):
        if not 'board' in self.__dict__:
            return

        turn = self.board.get_turn()
        is_checkmate = self.board.brain.is_checkmate()



        self.left_text.fill(Colors.GREEN.lerp(Colors.GRAY,0.85))

        text = f"{turn.capitalize()}.'s turn"
        if is_checkmate:
            text = f"Checkmate, {turn.capitalize()} loses!"

        text_box = TextBox(
            text,Pos(0,0),
            self.left_text.get_width(),
            fonts_path[0],30,
            tuple(Colors.BLACK),tuple(Colors.GLASS),"ltr",
            False
        )

        text = text_box.text_surface

        text_rect = text.get_rect()
        text_rect.center = self.left_text.get_rect().center
        self.left_text.blit(text,text_rect)





    def check_events( self ):
        self.board.check_events()

    def render( self,surface:Surface ):
        self.board.render(surface)
        surface.blit(self.left_text,[0,0])
