import subprocess
import datetime
from i3situation.plugins._plugin import Plugin

__all__ = 'CmusPlugin'


class CmusPlugin(Plugin):

    def __init__(self, config):
        """
        Possible format options are:

        status
        file
        duration
        position
        artist
        album
        title
        date
        genre
        tracknumber
        comment
        replaygain_track_gain
        aaa_mode
        continue
        play_library
        play_sorted
        replaygain
        replaygain_limit
        replaygain_preamp
        repeat
        repeat_current
        shuffle
        softvol
        vol_left
        vol_right
        """
        self.options = {'interval': 1, 'format':
                'artist - title - position/duration'}
        super().__init__(config)

    def main(self):
        """
        A compulsary function that gets the output of the cmus-remote -Q command
        and converts it to unicode in order for it to be processed and finally
        output.
        """
        try:
            # Setting stderr to subprocess.STDOUT seems to stop the error
            # message returned by the process from being output to STDOUT.
            cmusOutput = subprocess.check_output(['cmus-remote', '-Q'],
                                    stderr=subprocess.STDOUT).decode('utf-8')
        except subprocess.CalledProcessError:
            return self.output('Cmus is not running', 'Cmus is not running')
        status = self.convertCmusOutput(cmusOutput)
        outString = self.options['format']
        for k, v in status.items():
            outString = outString.replace(k, v)
        return self.output(outString, outString)

    def convertCmusOutput(self, cmusOutput):
        """
        Change the newline separated string of output data into
        a dictionary which can then be used to replace the strings in the config
        format.
        """
        cmusOutput = cmusOutput.split('\n')
        cmusOutput = [x.replace('tag ', '') for x in cmusOutput if not x in '']
        cmusOutput = [x.replace('set ', '') for x in cmusOutput]
        status = {}
        partitioned = (item.partition(' ') for item in cmusOutput)
        status = {item[0]: item[2] for item in partitioned}
        status['duration'] = self.convertTime(status['duration'])
        status['position'] = self.convertTime(status['position'])
        return status

    def convertTime(self, time):
        """
        A helper function to convert seconds into hh:mm:ss for better
        readability.
        """
        timeString = str(datetime.timedelta(seconds=int(time)))
        if timeString.split(':')[0] == '0':
            timeString = timeString.partition(':')[2]
        return timeString
