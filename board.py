from common_names import *

class Board:
    def __init__(self,rect:FRect):
        self.rect = rect
        self.border_size = 10
        self.black_color = None
        self.white_color = None

    @property
    def content_rect( self ):
        rect = self.rect.copy()
        rect.x += self.border_size
        rect.w -= self.border_size * 2
        rect.y += self.border_size
        rect.h -= self.border_size * 2

        return rect

    def render( self,surface:Surface ):
        pg.draw.rect(surface,[0,0,50],self.content_rect)
        pg.draw.rect(surface,[50,0,0],self.rect,width=self.border_size)