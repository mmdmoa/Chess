import window

from common_names import *
from common_functions import *

pg.init()
from common_resources import *

from window import Window
from colors import Colors
from game import Game

size = 1000,640
size_scale = 1



Holder.window = Window(Pos(size[0] * size_scale, size[1] * size_scale))

game = Game()

while not event_holder.should_quit:
    Holder.window.surface.fill(Colors.GRAY)
    game.check_events()
    game.render(Holder.window.surface)

    event_holder.get_events()
    Holder.window.update()



