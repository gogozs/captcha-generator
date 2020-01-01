# -*- encoding: utf-8 -*-
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import numpy as np
import cv2
from captcha_generator.conf.base_settings import settings, mc
import base64
from io import BytesIO


class BaseFactory(object):
    charset = ""  # 符号源

    def __init__(self, pic_dir, prefix, img_size, font_size, font_type, fg_color, d_color, bg_color, line_num,
                 point_num, probability):
        self.pic_dir = pic_dir  # 图片保存位置
        self.img_size = img_size  # 验证码尺寸
        self.out_size = (int(self.img_size[0] / 4), int(self.img_size[1] / 4))
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
            self.prefix = ''
        else:
            self.prefix = prefix

    def _check_dir(self):
        if not os.path.exists(self.pic_dir):
            os.mkdir(self.pic_dir, mode=755)

    def draw_text(self, charset, rand_color=False):
        """
        写文字
        """
        charset = str(charset)
        print(self.font_type)
        hold = ImageFont.truetype(self.font_type, self.font_size)
        # hold = ImageFont.truetype(r'/Users/zs/projects/py/captcha-generator/captcha_generator/font/Calibri.ttf', self.font_size)
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
        """变换"""
        params = [1 - float(random.randint(1, 2)) / 100, 0, 0, 0, 1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500, 0.001, float(random.randint(1, 2)) / 500]
        self.pic = self.pic.transform(self.img_size, Image.PERSPECTIVE, params)
        self.draw = ImageDraw.Draw(self.pic)

    def add_point(self):
        """增加干扰点"""
        for i in range(self.width):
            for j in range(self.height):
                tmp = random.randint(0, 100)
                if (tmp <= self.probability):
                    self.draw.point((i, j), self.d_color)

    def add_line(self):
        """增加干扰线"""
        for i in range(self.line_num):
            x1 = random.randint(0, self.width)
            x2 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            y2 = random.randint(0, self.height)
            self.draw.line(((x1, y1), (x2, y2)), self.d_color)

    def flush(self):
        """打磨润色"""
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

    def _save(self, name, resize=False):
        """
        保存图片
        """
        self._check_dir()
        name = f'{self.prefix}-{name}.png' if self.prefix else f'{name}.png'
        filename = os.path.join(self.pic_dir, name)
        self.pic.save(filename)
        self.reset()
        if resize: self.resize(filename)
        return name

    def _base64(self):
        """获得image base64"""
        buffered = BytesIO()
        self.pic.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue())

    def reset(self):
        """重置"""
        self.pic = Image.new('RGB', self.img_size, self.bg_color)  # 图片
        self.draw = ImageDraw.Draw(self.pic)  # 画笔

    def resize(self, filename):
        """调整大小"""
        c = cv2.imread(filename)
        new_image = cv2.resize(c, (self.out_size), interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(filename, new_image)

    def create_catpcha(self, charset, name=None, transform=False, add_point=False, add_line=True,
                       border_color=settings.RED_COLOR):
        """
        :param charset: 验证码内容
        :param name:
        :param is_base64:
        :param transform:
        :param add_point:
        :param add_line:
        :param border_color:
        :return:
        """
        self.reset()
        self.draw_text(charset)
        if transform: self.transform()
        if add_point: self.add_point()
        if add_line: self.add_line()
        if border_color: self.add_border(border_color=border_color)
        return self._save(name) if name else self._base64()

    def get_randcolor(self):
        """生成随机颜色"""
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)
