from common_names import *

class Sprite:
    loaded = {}

    def __init__(self,path:str):
        if path in Sprite.loaded:
            self.raw_surface = Sprite.loaded[path]
        else:
            self.raw_surface = Sprite.loaded[path] = pg.image.load(path)

        self.transformed_surface = self.raw_surface.copy()

    def transform( self,new_w,new_h ):
        self.transformed_surface = pg.transform.scale(self.raw_surface,(new_w,new_h))

    def transform_by_height( self,new_h ):
        current_h = self.raw_surface.get_height()
        new_w = self.raw_surface.get_width() * (new_h / current_h)

        self.transformed_surface = pg.transform.scale(self.raw_surface,(new_w,new_h))

    def transform_by_scale( self,scale_x,scale_y ):
        new_w,new_h = self.raw_surface.get_size()
        new_w *= scale_x
        new_h *= scale_y

        self.transformed_surface = pg.transform.scale(self.raw_surface,(new_w,new_h))



    def render_at( self,surface:Surface ):
        ...