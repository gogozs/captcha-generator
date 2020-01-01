## 一个python简易的验证码库

## 安装说明

```shell
# git install
git clone git@github.com:go-zs/captcha-generator.git
cd captcha-generator
python setup install

# pip install
pip install captcha-generator
```

## 使用说明
```python
# example
import captcha_generator
pic_factory = captcha_generator.PicFactory()
pic_factory.generate()
```