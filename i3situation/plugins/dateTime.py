import time
import subprocess
import os
from i3situation.plugins._plugin import Plugin

__all__ = 'DateTimePlugin'


class DateTimePlugin(Plugin):

    def __init__(self, config):
        self.options = {'timeZone': 'GMT', 'longFormat': '%d-%m-%Y %H:%M:%S',
                'shortFormat': '%H:%M:%S', 'interval': 1, 'menuCommand': ''}
        super().__init__(config)

    def main(self):
        cur = time.time()
        os.environ['TZ'] = self.options['timeZone']
        time.tzset()
        longTime = time.strftime(self.options['longFormat'], time.localtime(cur))
        shortTime = time.strftime(self.options['shortFormat'], time.localtime(cur))
        return self.output(longTime, shortTime)

    def onClick(self, event):
        if self.options['menuCommand'] != '':
            self.displayDzen(event)
