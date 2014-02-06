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
            cmus_output = subprocess.check_output(['cmus-remote', '-Q'],
                                    stderr=subprocess.STDOUT).decode('utf-8')
        except subprocess.CalledProcessError:
            return self.output(None, None)
        if 'duration' in cmus_output:
            status = self.convert_cmus_output(cmus_output)
            out_string = self.options['format']
            for k, v in status.items():
                out_string = out_string.replace(k, v)
        else:
            out_string = None
        return self.output(out_string, out_string)

    def on_click(self, event):
        """
        Handle click events.
        Left mouse: Pause/play
        Middle mouse: Back a track/Display menu
        Right mouse: Forward a track
        """
        if self.options['menu_command'] == '':
            if event['button'] == 1:
                subprocess.call(['cmus-remote', '-u'])
            elif event['button'] == 2:
                subprocess.call(['cmus-remote', '-r'])
            else:
                subprocess.call(['cmus-remote', '-n'])
        else:
            if event['button'] == 1:
                subprocess.call(['cmus-remote', '-u'])
            elif event['button'] == 2:
                self.display_dzen(event)
            else:
                subprocess.call(['cmus-remote', '-n'])


    def convert_cmus_output(self, cmus_output):
        """
        Change the newline separated string of output data into
        a dictionary which can then be used to replace the strings in the config
        format.

        cmus_output: A string with information about cmus that is newline
        seperated. Running cmus-remote -Q in a terminal will show you what
        you're dealing with.
        """
        cmus_output = cmus_output.split('\n')
        cmus_output = [x.replace('tag ', '') for x in cmus_output if not x in '']
        cmus_output = [x.replace('set ', '') for x in cmus_output]
        status = {}
        partitioned = (item.partition(' ') for item in cmus_output)
        status = {item[0]: item[2] for item in partitioned}
        status['duration'] = self.convert_time(status['duration'])
        status['position'] = self.convert_time(status['position'])
        return status

    def convert_time(self, time):
        """
        A helper function to convert seconds into hh:mm:ss for better
        readability.

        time: A string representing time in seconds.
        """
        time_string = str(datetime.timedelta(seconds=int(time)))
        if time_string.split(':')[0] == '0':
            time_string = time_string.partition(':')[2]
        return time_string
