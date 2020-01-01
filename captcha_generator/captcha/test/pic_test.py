# -*- encoding: utf-8 -*-

import unittest

from captcha_generator import PicFactory


class PicTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pic_factory = PicFactory()

    def test_generate(self):
        res = self.pic_factory.generate()
        print(res)

