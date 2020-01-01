import os

class _Settings():
    BG_COLOR = (255, 255, 255)  # 背景颜色
    FG_COLOR = (0, 0, 255)  # 字体颜色
    RED_COLOR = (255, 0, 0)  # 字体颜色
    GREEN_COLOR = (0, 255, 0)  # 字体颜色
    BLUE_COLOR = (0, 0, 255)  # 字体颜色
    WHITE_COLOR = (255, 255, 255)  # 字体颜色
    BLACK_COLOR = (0, 0, 0)  # 字体颜色
    COLOR_LIST = ['red', 'green', 'blue']



class _ModuleConstants():
    FONT_DIR = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "font/")

# 引入
settings = _Settings()
mc =_ModuleConstants()
