from common_names import *

class Colors:
    @staticmethod
    def random_color():
        return Color([random.randint(0,255) for _ in range(3)])


    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    GLASS = Color(0, 0, 0, 0)
    WHITE = Color(255, 255, 255)
    GRAY = Color(127, 127, 127)
    BLACK = Color(0, 0, 0)