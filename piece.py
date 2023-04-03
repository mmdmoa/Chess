from common_names import *

class Piece:
    loaded = {}

    def __init__(self,path:str):
        if path in Piece.loaded:
            self.raw_surface = Piece.loaded[path]
        else:
            self.raw_surface = Piece.loaded[path] = pg.image.load(path)

        self.transformed_surface = self.raw_surface.copy()

    def transform( self ):
        ...

    def render_at( self,surface:Surface ):
        ...