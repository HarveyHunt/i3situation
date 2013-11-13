#!/usr/bin/python3
from i3situation.core import status
import logging


def main():
    s = status.Status()
    logging.debug('Initialised Status object')
    s.run()

if __name__ == '__main__':
    main()
