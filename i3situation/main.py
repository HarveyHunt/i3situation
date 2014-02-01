#!/usr/bin/python3
import logging
from i3situation.core import status


def main():
    s = status.Status()
    logging.debug('Initialised Status object')
    s.run()

if __name__ == '__main__':
    main()
