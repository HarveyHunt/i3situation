import subprocess
from i3situation.plugins._plugin import Plugin

__all__ = 'RunPlugin'


class RunPlugin(Plugin):
    """
    A plugin that runs arbitrary shell commands and outputs them to the bar.
    USE WITH CAUTION.
    """

    def __init__(self, config):
        self.options = {'command': 'echo No command', 'text': '',
                        'color': '#FFFFFF', 'interval': 1}
        super().__init__(config, self.options)
        # A sad americanism.
        self._outputOptions['color'] = self.options['color']

    def main(self):

        shellOutput = subprocess.check_output(self.options['command'].split(' '),
                                stderr=subprocess.STDOUT).decode('utf-8')
        return self.output(shellOutput, shellOutput)
