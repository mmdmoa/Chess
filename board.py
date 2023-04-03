from common_names import *

class Board:
    def __init__(self,rect:FRect):
        self.rect = rect
        self.border_size = 0
        self.black_color = None
        self.white_color = None


    def render( self,surface:Surface ):
        pg.draw.rect(surface,[0,0,50],self.rect)