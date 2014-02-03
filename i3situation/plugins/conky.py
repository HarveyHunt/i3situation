import subprocess
from i3situation.plugins._plugin import Plugin

__all__ = 'ConkyPlugin'


class ConkyPlugin(Plugin):

    def __init__(self, config):
        self.options = {'command': '$uptime', 'interval': 1,
                'config': '~/.conkyrc'}
        super().__init__(config)

    def main(self):
        try:
            out = subprocess.check_output(['conky', '-i', '1', '-t',
                self.options['command'], '-c', self.options['config']]).decode('utf8')
        except subprocess.CalledProcessError:
            out = 'A non-zero exit status was returned.'
            self.output_options['color'] = '#FF0000'
        except FileNotFoundError:
            out = 'Conky isn\'t installed.'
            self.output_options['color'] = '#FF0000'

        return self.output(out, out)
