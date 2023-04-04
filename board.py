from common_names import *
from common_resources import *

class Board:

    def __init__(self,rect:FRect):
        self.rect = rect
        self.border_size = 10
        self.black_color = Colors.BLACK
        self.white_color = Colors.WHITE
        self.content_rect = self.rect.copy()

        self.board_dict = {}

        self.pieces = {}
        self.board_surface: Optional[Surface] = None
        self.pieces_surface: Optional[Surface] = None

        self.update()
        self.init()

    def init( self ):
        self.init_board()
        self.init_pieces()

    def init_board( self ):
        size = self.content_rect.w,self.content_rect.h
        self.board_surface = Surface(size)
        w, h = self.content_rect.w / 8, self.content_rect.h / 8

        is_black = False

        for x,letter in zip(range(8),'abcdefgh') :
            for y,digit in zip(range(8),'87654321') :
                color = self.white_color
                if is_black :
                    color = self.black_color

                rect = FRect(x * w - 1, y * h - 1, w + 1, h + 1)
                self.board_dict[letter+digit] = rect
                pg.draw.rect(self.board_surface, color,
                    rect)

                is_black = not is_black
            is_black = not is_black

    def init_pieces( self ):
        size = self.content_rect.w, self.content_rect.h
        self.pieces_surface = Surface(size).convert_alpha()
        self.pieces_surface.fill(Colors.GLASS)

        w, h = self.content_rect.w / 8, self.content_rect.h / 8

        for piece in sprites:
            sprites[piece].transform(w,h)

        self.pieces = {
            "black_king":"e8",
            "black_queen":"d8",
            "black_rook":"a8",
            "black_bishop":"c8",
            "black_knight":"b8",
            "black_pawn":"a7",

            "white_king":"e1",
            "white_queen":"d1",
            "white_rook":"a1",
            "white_bishop":"c1",
            "white_knight":"b1",
            "white_pawn":"a2"
        }

        for key in self.pieces:
            coord = self.pieces[key]
            rect = self.board_dict[coord]
            surface = sprites[key].transformed_surface
            self.pieces_surface.blit(surface,rect)



    def get_content_rect( self ):
        rect = self.rect.copy()
        rect.x += self.border_size
        rect.w -= self.border_size * 2
        rect.y += self.border_size
        rect.h -= self.border_size * 2

        return rect

    def update( self ):
        self.content_rect = self.get_content_rect()

    def get_board_collisions( self ) -> str:
        if not event_holder.mouse_focus: 'none'
        m_rect = event_holder.mouse_rect
        m_rect.x -= self.content_rect.x
        m_rect.y -= self.content_rect.y

        for key in self.board_dict:
            rect = self.board_dict[key]
            if m_rect.colliderect(rect):
                return key



    def check_events( self ):
        if event_holder.mouse_pressed_keys[0]:
            selected = self.get_board_collisions()
            print(selected)

    def render_board( self,surface:Surface ):
        ...

    def render( self,surface:Surface ):
        surface.blit(self.board_surface,self.content_rect)
        surface.blit(self.pieces_surface,self.content_rect)

        pg.draw.rect(surface,[50,0,0],self.rect,width=self.border_size)