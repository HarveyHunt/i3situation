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
    parser.add_argument('-c', '--config', action='store',
            help='The full path to the configuration file. \
                    Defaults to ~/.i3-py3-status.conf',
                        default=defaultPath)
    args = parser.parse_args()
    s = Status(args.config)
    while True:
        s.run()
