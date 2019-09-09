import random
import string
from io import StringIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import numpy as np
import cv2
from captcha_factory.conf.base_settings import settings, mc


class PicFactory():
    charset = ""  # 符号源
    img_size = (140, 32)  # 图片大小
    output_size = (int(img_size[0] / 4), int(img_size[1] / 4))

    def __init__(self, pic_dir=mc.CAPTCHA_OUTPUT, prefix=None, img_size=(140, 32),
                 font_size=None, font_type=os.path.join(mc.FONT_PATH, 'CALIBRII.TTF'),
                 fg_color=settings.BLUE_COLOR, d_color=settings.BLACK_COLOR, bg_color=settings.WHITE_COLOR,
                 line_num=6, point_num=50, probability=2):
        self.reset()
        self.flag = 1 # 编号
        self.pic_dir = pic_dir # 图片保存位置
        self.img_size = img_size # 验证码尺寸
        self.width, self.height = img_size  # 长，宽
        self.font_size = font_size or img_size[1]  # 字体大小
        self.font_type = font_type  # 字体类型
        self.fg_color = fg_color  # 字体颜色
        self.d_color = d_color  # 干扰颜色
        self.bg_color = bg_color  # 背景颜色
        self.line_num = line_num  # 干扰线条数
        self.point_num = point_num  # 干扰点数
        self.probability = probability  # 随机概率因子
        if prefix is None:
            self.prefix = 'pic'
        else:
            self.prefix = prefix

    def draw_text(self, charset, rand_color=False):
        """
        画画
        """
        charset = str(charset)
        hold = ImageFont.truetype(self.font_type, self.font_size)
        length = len(charset)
        gap = int(self.width / length)
        sy = 2

        for index, c in enumerate(charset):
            if rand_color:
                color = self.get_randcolor()
            else:
                color = self.fg_color
            self.draw.text((2 + index * gap, sy), c, font=hold, fill=color)

    def transform(self):
        """
        变换,还不太明白这个变换
        """
        params = [1 - float(random.randint(1, 2)) / 100, 0, 0, 0, 1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500, 0.001, float(random.randint(1, 2)) / 500]
        self.pic = self.pic.transform(self.img_size, Image.PERSPECTIVE, params)
        self.draw = ImageDraw.Draw(self.pic)

    def add_point(self):
        """
        增加干扰点
        """
        for i in range(self.width):
            for j in range(self.height):
                tmp = random.randint(0, 100)
                if (tmp <= self.probability):
                    self.draw.point((i, j), self.d_color)

    def add_line(self):
        """
        增加干扰线
        """
        for i in range(self.line_num):
            x1 = random.randint(0, self.width)
            x2 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            y2 = random.randint(0, self.height)
            self.draw.line(((x1, y1), (x2, y2)), self.d_color)

    def flush(self):
        """
        打磨润色
        """
        self.pic = self.pic.filter(ImageFilter.EDGE_ENHANCE_MORE)
        self.pic = self.pic.filter(ImageFilter.SMOOTH)

    def add_border(self, size=None, border_color=settings.RED_COLOR, border_width=1):
        """
        # 加边框 rectangle
        :param size:
        :param border_color:
        :param border_width:
        :return:
        """
        img = np.asarray(self.pic)
        if size:
            width, height = size
        else:
            width, height = self.width, self.height
        img = cv2.rectangle(img,
                            (0, 0),
                            (int(width - border_width), int(height - border_width)),
                            border_color, border_width)
        self.pic = Image.fromarray(np.uint8(img))

    def save(self, resize=False):
        """
        图片输出
        """
        name = f'{self.prefix}_{self.flag}.png'
        filename = os.path.join(self.pic_dir, name)
        self.pic.save(filename)
        self.flag += 1
        self.reset()
        if resize: self.resize(filename)
        return name

    def reset(self):
        """重置"""
        self.pic = Image.new('RGB', self.img_size, self.bg_color)  # 图片
        self.draw = ImageDraw.Draw(self.pic)  # 画笔

    def resize(self, filename):
        """调整大小"""
        c = cv2.imread(filename)
        new_image = cv2.resize(c, (self.output_size), interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(filename, new_image)

    def new_pic(self, charset, transform=False, add_point=False, add_line=True, border_color=settings.RED_COLOR):
        self.draw_text(charset)
        if transform: self.transform()
        if add_point: self.add_point()
        if add_line: self.add_line()
        if border_color: self.add_border(border_color=border_color)
        return self.save()

    # 生成随机颜色
    def get_randcolor(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)


if __name__ == '__main__':
    b = PicFactory()
    b.new_pic(154108)
