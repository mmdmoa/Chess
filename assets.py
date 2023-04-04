import pygame as pg
from sprite import Sprite

root = "./assets/"

sprites_path = [(name, root + "chess_pieces/" + name + ".png") for name in
    ["black_king", "black_queen", "black_rook", "black_bishop", "black_knight", "black_pawn",
        "white_king", "white_queen", "white_rook", "white_bishop", "white_knight", "white_pawn"]]

sprites = {key : value for key, value in [(name, Sprite(path)) for name, path in sprites_path]}
