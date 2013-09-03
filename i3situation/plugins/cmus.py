from subprocess import check_output
import datetime
from i3situation.plugins._plugin import Plugin

__all__ = 'CmusPlugin'


class CmusPlugin(Plugin):

    def __init__(self, config):
        self.options = {'color': '#FFFFFF', 'interval': 1, 'format':
                'artist - album - position/duration'}
        super().__init__(config, self.options)
        # A sad americanism.
        self._outputOptions['color'] = self.options['color']

    def main(self):
        cmusOutput = check_output(['cmus-remote', '-Q']).decode('utf-8')
        status = self.convertCmusOutput(cmusOutput)
        outString = self.options['format']
        for k, v in status.items():
            outString = outString.replace(k, v)
        return self.output(outString, outString)

    def convertCmusOutput(self, cmusOutput):
        cmusOutput = cmusOutput.split('\n')
        cmusOutput = [x.replace('tag ', '') for x in cmusOutput if not x in '']
        cmusOutput = [x.replace('set ', '') for x in cmusOutput]
        status = {}
        for item in cmusOutput:
            status[item.partition(' ')[0]] = item.partition(' ')[2]
        status['duration'] = self.convertTime(status['duration'])
        status['position'] = self.convertTime(status['position'])
        return status

    def convertTime(self, time):
        timeString = str(datetime.timedelta(seconds=int(time)))
        if timeString.split(':')[0] == '0':
            timeString = timeString.partition(':')[2]
        return timeString
