import time
import subprocess
import os
from i3situation.plugins._plugin import Plugin

__all__ = 'DateTimePlugin'


class DateTimePlugin(Plugin):

    def __init__(self, config):
        self.options = {'time_zone': 'GMT', 'long_format': '%d-%m-%Y %H:%M:%S',
                'short_format': '%H:%M:%S', 'interval': 1, 'menu_command': ''}
        super().__init__(config)

    def main(self):
        cur = time.time()
        os.environ['TZ'] = self.options['time_zone']
        time.tzset()
        long_time = time.strftime(self.options['long_format'], time.localtime(cur))
        short_time = time.strftime(self.options['short_format'], time.localtime(cur))
        return self.output(long_time, short_time)

    def on_click(self, event):
        if self.options['menu_command'] != '':
            self.display_dzen(event)
