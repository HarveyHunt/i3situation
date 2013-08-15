from plugins._plugin import Plugin
import time
import os

__all__ = 'DateTimePlugin'


class DateTimePlugin(Plugin):

    def __init__(self, config):
        self.options = {'timeZone': 'GMT', 'longFormat': '%d-%m-%Y %H:%M:%S',
                        'shortFormat': '%H:%M:%S'}
        super().__init__(config, self.options)

    def main(self):
        cur = time.time()
        os.environ['TZ'] = self.options['timeZone']
        time.tzset()
        longTime = time.strftime(self.options['longFormat'], time.localtime(cur))
        shortTime = time.strftime(self.options['shortFormat'], time.localtime(cur))
        return self.output(longTime, shortTime)
