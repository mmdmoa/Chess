from common_imports import *

from window import Window
from event_holder import EventHolder
from colors import Colors

size = 1000,640
size_scale = 1

window = Window(Pos(size[0]*size_scale,size[1]*size_scale))

event_holder = EventHolder()


while not event_holder.should_quit:
    window.surface.fill(Colors.GRAY)
    event_holder.get_events()
    window.update()



