#!/usr/bin/python3
from status import Status
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""A replacement for i3status \
            written in pure Python 3. This application supports heavy \
            customisation through a simple plugin system. Developed by \
            Harvey Hunt <harveyhuntnexus@gmail.com>""")
    parser.add_argument('-c', '--config', action='store',
            help='The full path to the configuration file. \
                    Defaults to ~/.i3-py3-status.conf')
    args = parser.parse_args()

    s = Status(args.config)
    while True:
        s.run()
