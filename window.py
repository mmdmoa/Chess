from common_imports import *

class Window:
    def __init__(self,size:Pos):
        self.size = size
        self.surface = pg.display.set_mode(self.size,SCALED | FULLSCREEN)


    @property
    def center( self ):
        return Pos(self.surface.get_rect().center)


    def update( self ):
        pg.display.update()

