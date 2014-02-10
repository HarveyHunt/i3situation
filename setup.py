#!/usr/bin/python3
import os
from setuptools import setup
from setuptools import find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='i3situation',
      packages=find_packages(),
      version='1.0.2',
      description='A replacement for i3status that allows for the use of plugins.',
      author='Harvey Hunt',
      url='https://github.com/HarveyHunt/i3situation',
      author_email='harveyhuntnexus@gmail.com',
      license="GPLv3",
      keywords="python3 i3situation i3 i3wm i3status i3bar json",
      install_requires=['requests'],
      long_description=read('README.md'),
      entry_points={'console_scripts': ['i3situation=i3situation.main:main']})
