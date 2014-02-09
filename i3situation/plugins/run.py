import subprocess
from i3situation.plugins._plugin import Plugin

__all__ = 'RunPlugin'


class RunPlugin(Plugin):
    """
    A plugin that runs arbitrary shell commands and outputs them to the bar.
    USE WITH CAUTION.
    """

    def __init__(self, config):
        self.options = {'command': 'echo No command',
                        'interval': 1}
        super().__init__(config)

    def main(self):
        shell_output = subprocess.check_output(self.options['command'].split(' '),
                                stderr=subprocess.STDOUT).decode('utf-8')
        return self.output(shell_output, shell_output)
