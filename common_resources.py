from common_names import *

from window import Window
from assets import sprites,fonts,fonts_path
from event_holder import EventHolder, event_holder

stockfish_engine = Stockfish(path="/home/yolo/stockfish/stockfish_15.1_linux_x64_avx2/"
                                    "stockfish-ubuntu-20.04-x86-64-avx2", depth=18,
    parameters={"Threads" : 2, "Minimum Thinking Time" : 30}
)

class Holder:
    window: Optional[Window] = None

