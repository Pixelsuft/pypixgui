from setuptools import setup, find_packages
from urllib.request import urlretrieve as download_file
from os import remove as del_file
from os import name as os_type
from os import system as cmd_run
from os import access as file_exists
from os import F_OK as file_exists_param


download_file('https://github.com/Pixelsuft/pypixgui/raw/main/README.MD', 'README.MD')
temp_file = open('README.MD', 'r')
readme = temp_file.read()
temp_file.close()
if not file_exists('setup.py', file_exists_param):
    del_file('README.MD')

req = ['pyautogui', 'pynput', 'pygame', 'Pillow', 'PySDL2', 'pysdl2-dll', 'mss', 'clear-cache']
if os_type == 'nt':
    req.append('pywin32')
elif os_type == 'posix':
    cmd_run('sudo apt-get install libsdl2-dev python3-sdl2')

setup(
    name='pypixgui',
    version='0.1.4',
    author='Pixelsuft',
    description='Python GUI Package.',
    keywords='pypixgui',
    py_modules=['pypixgui'],
    url='https://github.com/Pixelsuft/pypixgui',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    license='GPL',
    packages=find_packages(),
    install_requires=req,
)
