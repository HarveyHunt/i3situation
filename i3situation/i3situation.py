#!/usr/bin/python3
from i3situation.core.status import Status
import logging


def main():
    s = Status()
    logging.debug('Initialised Status object')
    s.run()

if __name__ == '__main__':
    main()
