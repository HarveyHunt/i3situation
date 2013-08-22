#!/usr/bin/python3
from core.status import Status
import argparse
import os
import logging

if __name__ == '__main__':
    defaultPath = os.path.join(os.path.expanduser('~'), '.i3-py3-status.conf')
    parser = argparse.ArgumentParser(description="""A replacement for i3status \
            written in pure Python 3. This application supports heavy \
            customisation through a simple plugin system. Developed by \
            Harvey Hunt <harveyhuntnexus@gmail.com>""")
    args = parser.parse_args()
    s = Status()
    logging.debug('Initialised Status object')
    while True:
        s.run()
