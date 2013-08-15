#!/usr/bin/python3
import os
from setuptools import setup
from setuptools import find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='i3-py3-status',
      packages=find_packages(),
      version='0.2',
      scripts=['i3-py3-status.py'],
      description='A replacement for i3status that allows for the use of plugins.',
      author='Harvey Hunt',
      author_email='harveyhuntnexus@gmail.com',
      license="GPLv3",
      keywords="python3 i3 i3wm i3status i3bar json",
      long_description=read('README.md')
    )
