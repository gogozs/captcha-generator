import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import numpy as np
import cv2
import string

from captcha_generator.captcha.base_factory import BaseFactory
from captcha_generator.conf.base_settings import settings, mc
from typing import Union

from captcha_generator.exception.exception import CaptchaException

ListTuple = Union[list, tuple]


class PicFactory(BaseFactory):

    def __init__(self, pic_dir="./output", prefix=None, img_size=(140, 32),
                 font_size=None, font_type=os.path.join(mc.FONT_DIR, 'Calibri.TTF'),
                 fg_color=settings.BLUE_COLOR, d_color=settings.BLACK_COLOR, bg_color=settings.WHITE_COLOR,
                 line_num=6, point_num=50, probability=2, charset=None):
        if not charset:
            self.set_charset(string.ascii_letters)
        super(PicFactory, self).__init__(pic_dir, prefix, img_size, font_size, font_type, fg_color, d_color, bg_color,
                                         line_num, point_num, probability)

    def generate(self, name=None, num=4):
        """
        生成验证码
        :param name: 图片名字
        :param num: captcha长度
        :return:
        """
        charset = self._random(num)
        return (charset, self.create_catpcha(charset, name))

    def set_charset_numbers(self):
        """
        设置字符集为纯数字
        """
        self.__charset = string.digits

    def set_charset_ascii(self):
        """
        设置字符集ascii_letters
        """
        self.__charset = string.ascii_letters

    def set_charset(self, charset: ListTuple):
        """
        自定义设置字符集
        """
        self.__charset = charset

    def set_size(self, img_size: ListTuple):
        """
        :param img_size: 图片尺寸
        :return:
        """
        if len(img_size) != 2:
            raise CaptchaException("invalid params")
        self.__img_size = img_size

    def _random(self, char_num: int):
        """
        随机生成字符串
        """
        if char_num <= 0:
            char_num = 4
        return "".join([random.choice(self.__charset) for _ in range(char_num)])

