import chess

from common_names import *
from common_resources import *
from sprite import Sprite

class Board:

    fen_pieces_map = {
        'r':'black_rook',
        'n':'black_knight',
        'b':'black_bishop',
        'q':'black_queen',
        'k':'black_king',
        'p':'black_pawn',

        'R':'white_rook',
        'N':'white_knight',
        'B':'white_bishop',
        'Q':'white_queen',
        'K':'white_king',
        'P':'white_pawn',
    }

    def __init__(self,rect:FRect):

        self.brain = chess.Board()
        self.load_board_by_fen()

        self.rect = rect
        self.border_size = 10
        self.black_color = Colors.GRAY.lerp(Colors.GREEN,0.3).lerp(Colors.RED,0.1)
        self.white_color = Colors.WHITE.lerp(Colors.GREEN,0.1).lerp(Colors.RED,0.3)
        self.content_rect = self.rect.copy()

        self.board_dict = {}

        self.pieces = {}
        self.board_surface: Optional[Surface] = None
        self.pieces_surface: Optional[Surface] = None
        self.selected = None
        self.selected_color = Colors.BLUE.lerp(Colors.GREEN,0.3)
        self.selected_color.a = 100

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

        tallest_piece = sprites['black_queen']
        max_y = 0
        for key in sprites:
            surface = sprites[key].raw_surface
            if surface.get_height() > max_y:
                max_y = surface.get_height()
                tallest_piece = sprites[key]

        tallest_piece.transform_by_height(h*0.95)
        raw_size = tallest_piece.raw_surface.get_size()
        transize = tallest_piece.transformed_surface.get_size()

        scale = (transize[0] / raw_size[0],transize[1] / raw_size[1])

        for piece in sprites:
            sprites[piece].transform_by_scale(scale[0],scale[1])


        self.load_board_by_fen()

        self.update_pieces_surface()


    @staticmethod
    def expand_fen_row(row ):
        text = ""
        for i in row:
            if i.isnumeric():
                for c in range(int(i)):
                    text+='0'
            else:
                text+=i

        return text

    def load_board_by_fen( self ):
        fen = self.brain.board_fen()

        new_fen = [Board.expand_fen_row(i) for i in fen.split('/')]

        pieces = {}

        for row,digit in zip(new_fen,"87654321"):
            for column,letter in zip(row,"abcdefgh"):
                if column!='0':
                    pieces[letter+digit] = Board.fen_pieces_map[column]


        self.pieces = pieces







    def update_pieces_surface( self ):
        self.pieces_surface.fill(Colors.GLASS)

        if self.selected is not None:
            pg.draw.rect(self.pieces_surface,self.selected_color,self.board_dict[self.selected])

        for coord in self.pieces:
            piece_name = self.pieces[coord]
            rect = self.board_dict[coord]
            surface = sprites[piece_name].transformed_surface
            surface_rect = surface.get_rect()
            surface_rect.center = rect.center
            self.pieces_surface.blit(surface,surface_rect)



    def get_content_rect( self ):
        rect = self.rect.copy()
        rect.x += self.border_size
        rect.w -= self.border_size * 2
        rect.y += self.border_size
        rect.h -= self.border_size * 2

        return rect

    def is_legal( self,uci ):
        return chess.Move.from_uci(uci) in self.brain.legal_moves

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
        if event_holder.mouse_pressed_keys[2]:
            self.selected = None
            self.update_pieces_surface()

        if event_holder.mouse_pressed_keys[0]:
            pre_selection = self.get_board_collisions()
            if pre_selection is not None and pre_selection != self.selected:

                if self.selected is None: # Selection
                    if pre_selection in self.pieces:
                        self.selected = pre_selection
                else: # Action
                    uci_move = self.selected+pre_selection

                    if self.is_legal(uci_move):
                        self.selected = None
                        self.brain.push_uci(uci_move)
                        self.load_board_by_fen()

                self.update_pieces_surface()


    def render_board( self,surface:Surface ):
        ...

    def render( self,surface:Surface ):
        surface.blit(self.board_surface,self.content_rect)
        surface.blit(self.pieces_surface,self.content_rect)

        pg.draw.rect(surface,[50,0,0],self.rect,width=self.border_size)