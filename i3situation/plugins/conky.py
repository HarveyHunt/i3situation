import subprocess
from i3situation.plugins._plugin import Plugin

__all__ = 'ConkyPlugin'


class ConkyPlugin(Plugin):

    def __init__(self, config):
        self.options = {'command': '$uptime', 'interval': 1,
                'config': '~/.conkyrc'}
        super().__init__(config)

    def main(self):
        out = subprocess.check_output(['conky', '-i', '1', '-t',
            self.options['command'], '-c', self.options['config']]).decode('utf8')
        return self.output(out, out)
