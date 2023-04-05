import chess

from common_names import *
from common_resources import *
from common_functions import *
from sprite import Sprite


class Board :
    fen_pieces_map = {'r' : 'black_rook', 'n' : 'black_knight', 'b' : 'black_bishop',
        'q' : 'black_queen', 'k' : 'black_king', 'p' : 'black_pawn',

        'R' : 'white_rook', 'N' : 'white_knight', 'B' : 'white_bishop', 'Q' : 'white_queen',
        'K' : 'white_king', 'P' : 'white_pawn', }

    board_coordination_map = []

    for letter in 'abcdefgh' :
        for digit in '12345678' :
            board_coordination_map.append(letter + digit)


    def __init__( self, rect: FRect ) :
        self.brain = chess.Board()
        self.update_board_by_fen()

        self.rect = rect
        self.border_size = 0
        self.black_color = Colors.GRAY.lerp(Colors.GREEN, 0.3).lerp(Colors.RED, 0.1)
        self.white_color = Colors.WHITE.lerp(Colors.GREEN, 0.1).lerp(Colors.RED, 0.3)
        self.content_rect = self.rect.copy()

        self.board_dict = {}
        self.valid_moves = []

        self.pieces = {}
        self.board_surface: Optional[Surface] = None
        self.pieces_surface: Optional[Surface] = None
        self.selected = None
        self.selected_color = Colors.BLUE.lerp(Colors.GREEN, 0.3)
        self.selected_color.a = 100
        self.move_color = Colors.GRAY.lerp(Colors.BLUE,0.5)
        self.take_color = Colors.GRAY.lerp(Colors.RED,0.7)
        self.move_color.a = 155
        self.take_color.a = 155
        self.check_color = Colors.RED.lerp(Colors.WHITE,0.5)
        self.check_color.a = 255
        self.move_radius = self.content_rect.w / 8 * 0.125

        self.update_board_size()
        self.init()


    def update_board_size( self ) :
        self.content_rect = self.get_content_rect()
        self.move_radius = self.content_rect.w / 8 * 0.125


    def init( self ) :
        self.init_board()
        self.init_pieces()


    def init_board( self ) :
        size = self.content_rect.w, self.content_rect.h
        self.board_surface = Surface(size)
        w, h = self.content_rect.w / 8, self.content_rect.h / 8

        is_black = False

        for x, letter in zip(range(8), 'abcdefgh') :
            for y, digit in zip(range(8), '87654321') :
                color = self.white_color
                if is_black :
                    color = self.black_color

                rect = FRect(x * w , y * h , w , h)
                self.board_dict[letter + digit] = rect
                pg.draw.rect(self.board_surface, color, rect)

                is_black = not is_black
            is_black = not is_black


    def init_pieces( self ) :
        size = self.content_rect.w, self.content_rect.h
        self.pieces_surface = Surface(size).convert_alpha()
        self.pieces_surface.fill(Colors.GLASS)

        w, h = self.content_rect.w / 8, self.content_rect.h / 8

        tallest_piece = sprites['black_queen']
        max_y = 0
        for key in sprites :
            surface = sprites[key].raw_surface
            if surface.get_height() > max_y :
                max_y = surface.get_height()
                tallest_piece = sprites[key]

        tallest_piece.transform_by_height(h * 0.95)
        raw_size = tallest_piece.raw_surface.get_size()
        transize = tallest_piece.transformed_surface.get_size()

        scale = (transize[0] / raw_size[0], transize[1] / raw_size[1])

        for piece in sprites :
            sprites[piece].transform_by_scale(scale[0], scale[1])

        self.update_board_by_fen()

        self.update_pieces_surface()


    def get_content_rect( self ) :
        rect = self.rect.copy()
        rect.x += self.border_size
        rect.w -= self.border_size * 2
        rect.y += self.border_size
        rect.h -= self.border_size * 2

        return rect


    def update_pieces_surface( self ) :
        self.pieces_surface.fill(Colors.GLASS)
        # self.pieces_surface = self.board_surface.copy()

        checkers = self.get_checkers_coordination()



        if self.selected is not None :
            pg.draw.rect(self.pieces_surface, self.selected_color, self.board_dict[self.selected])
            for move in self.valid_moves:
                take = move in self.pieces
                color = self.move_color
                if take:
                    color = self.take_color

                pg.draw.circle(self.pieces_surface, color,
                    self.board_dict[move].center,self.move_radius)

                pg.draw.rect(self.pieces_surface, color, self.board_dict[move],
                    width=int(self.board_dict[move].w*0.05))

        for checker in checkers:
            color = self.check_color
            pg.draw.rect(self.pieces_surface, color, self.board_dict[checker],
                width=int(self.board_dict[checker].w * 0.1)
            )


        turn = self.get_turn()

        for coord in self.pieces :
            piece_name = self.pieces[coord]
            rect = self.board_dict[coord]
            surface: Surface = sprites[piece_name].transformed_surface.copy()
            if turn == 'black':
                surface = pg.transform.flip(surface,flip_x=False,flip_y=True)

            surface_rect = surface.get_rect()
            surface_rect.center = rect.center
            self.pieces_surface.blit(surface, surface_rect)

        if turn == 'black':
            # self.pieces_surface = pg.transform.flip(self.pieces_surface, flip_x=True, flip_y=True)
            self.pieces_surface = pg.transform.flip(self.pieces_surface,True,True)

    def update_valid_moves( self ) :
        s = self.selected
        coord_board = Board.board_coordination_map.copy()
        coord_board.remove(s)
        all_moves = [s + i for i in coord_board]

        self.valid_moves = [i[2:] for i in all_moves if
            self.is_legal(i)]

    @staticmethod
    def expand_fen_row( row ) :
        text = ""
        for i in row :
            if i.isnumeric() :
                for c in range(int(i)) :
                    text += '0'
            else :
                text += i

        return text

    def find_piece( self,name ):
        for coord in self.pieces:
            piece = self.pieces[coord]
            if piece == name:
                return coord

    def undo( self ):
        self.selected = None
        try:
            self.brain.pop()
            self.update_board_by_fen()
            self.update_pieces_surface()
        except IndexError:
            ...

    def move( self,uci ):

        # Check if move is a pawn promotion
        if self.is_promotion(uci):
            uci+='q'

        if self.is_legal(uci):
            self.brain.push_uci(uci)
            return True

        return False

    def update_board_by_fen( self ) :
        fen = self.brain.board_fen()

        new_fen = [Board.expand_fen_row(i) for i in fen.split('/')]

        pieces = {}

        for row, digit in zip(new_fen, "87654321") :
            for column, letter in zip(row, "abcdefgh") :
                if column != '0' :
                    pieces[letter + digit] = Board.fen_pieces_map[column]

        self.pieces = pieces

    def is_promotion( self, uci ):
        # Check if move is a pawn promotion
        if self.pieces[uci[:2]].find('pawn') != -1 :
            if uci[3 :] in ['1', '8'] :
                return True

        return False

    def is_legal( self, uci ) :
        if self.is_promotion(uci):
            uci+='q'

        return chess.Move.from_uci(uci) in self.brain.legal_moves


    def get_board_collisions( self ) -> str :
        if not event_holder.mouse_focus : 'none'
        m_rect = event_holder.mouse_rect

        if self.get_turn() == 'black':
            m_rect.center = rotate_points(self.rect.center,m_rect.center,180)

        m_rect.x -= self.content_rect.x
        m_rect.y -= self.content_rect.y

        for key in self.board_dict :
            rect = self.board_dict[key]
            if m_rect.colliderect(rect) :
                return key


    def check_events( self ) :
        if K_SPACE in event_holder.pressed_keys:
            self.undo()

        if K_r in event_holder.pressed_keys:
            self.pieces_surface = pg.transform.flip(self.pieces_surface,True,True)

        if event_holder.mouse_pressed_keys[2] :
            self.selected = None
            self.update_pieces_surface()

        if event_holder.mouse_pressed_keys[0] :
            pre_selection = self.get_board_collisions()
            if pre_selection is not None and pre_selection != self.selected :
                if self.selected is None :  # Selection
                    if pre_selection in self.pieces :
                        self.selected = pre_selection
                        self.update_valid_moves()
                else :  # Action
                    uci_move = self.selected + pre_selection

                    if self.move(uci_move) :
                        self.selected = None
                        self.update_board_by_fen()

                self.update_pieces_surface()


    def get_turn( self ):
        if self.brain.turn:
            return 'white'
        return 'black'


    def get_checkers_coordination( self ):
        if not self.brain.is_check():
            return []

        checkers = str(self.brain.checkers()).split('\n')
        checkers = [[c for c in i if c != ' '] for i in checkers]
        result = []
        for row,digit in zip(checkers,'87654321'):
            for cell,letter in zip(row,'abcdefgh'):
                if cell == '1':
                    result.append(letter+digit)

        result.append(self.find_piece(self.get_turn()+"_king"))

        return result


    def render( self, surface: Surface ) :

        surface.blit(self.board_surface,self.content_rect)

        pieces_surface = self.pieces_surface

        surface.blit(pieces_surface, self.content_rect)

        if self.border_size:
            pg.draw.rect(surface, [50, 0, 0], self.rect, width=self.border_size)
