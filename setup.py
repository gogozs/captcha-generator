from setuptools import setup, find_packages

setup(
    name='captcha-generator',
    version='1.0',
    description='a simple generate captcha library',
    author='zs',
    license="MIT Licence",
    packages=['captcha_generator'],
    include_package_data=True,
    platforms='any',
    install_requires=['numpy>=1.17.2', 'opencv-python>=4.1.1.26', 'Pillow>=6.1.0'],
)
