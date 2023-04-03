from common_names import *

class Board:
    def __init__(self,rect:FRect):
        self.rect = rect
        self.border_size = 10
        self.black_color = Colors.BLACK
        self.white_color = Colors.WHITE
        self.content_rect = self.rect.copy()

        self.update()

    def update( self ):
        self.content_rect = self.get_content_rect()

    def get_content_rect( self ):
        rect = self.rect.copy()
        rect.x += self.border_size
        rect.w -= self.border_size * 2
        rect.y += self.border_size
        rect.h -= self.border_size * 2

        return rect

    def render( self,surface:Surface ):
        w,h = self.content_rect.w / 8,self.content_rect.h / 8

        pg.draw.rect(surface,[0,0,50],self.content_rect)

        is_black = False

        origin_x = self.content_rect.x
        origin_y = self.content_rect.y

        for x in range(8):
            for y in range(8):
                color = self.white_color
                if is_black:
                    color = self.black_color

                pg.draw.rect(surface,color,FRect(origin_x+x*w-1,origin_y+y*h-1,w+1,h+1))

                is_black = not is_black
            is_black = not is_black

        pg.draw.rect(surface,[50,0,0],self.rect,width=self.border_size)