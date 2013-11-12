import subprocess
import json

class Plugin():
    """
    A base class that should be inherited by all other plugins.
    It handles defaults, replacing options and managing lower level
    settings that a plugin developer need not bother with.
    """
    def __init__(self, config):
        self._outputOptions = {
            'color': None,
            'min_width': None,
            'align': None,
            'name': None,
            'urgent': None,
            'seperator': None,
            'seperator_block_width': None}
        # Replace default values with user defined ones.
        self.options.update(config)
        # Allow output options to be overwritten by the user.
        self._outputOptions.update((k, v) for k, v in config.items() if k in
                                   self._outputOptions)

    def output(self, fullText, shortText):
        """
        Output all of the options and data for a segment.
        """
        self._outputOptions.update({'full_text': fullText, 'short_text': shortText})
        self._outputOptions = {k: v for k, v in self._outputOptions.items() if v}
        return self._outputOptions

    def onClick(self, event):
        """
        A function that should be overwritten by a plugin that wishes to react
        to events.
        """
        pass

    def positionDzen(self, x):
        """
        Calculate the correct position that dzen2 should appear, so as
        to prevent the pop up from going off the screen.

        The popup will be centered on the mouse click. Both sides of the
        monitor need to be checked to ensure that the pop up doesn't go off
        of the screen.
        """
        if not '-x' in self.options['menuCommand']:
            i3outputs = subprocess.check_output(['i3-msg', '-t', 'get_outputs'])
            i3outputs = json.loads(i3outputs.decode('utf-8'))
            monitorWidth = [x['rect']['width'] for x in i3outputs if x['active']][0]
            cmd = self.options['menuCommand'].split()
            dzenWidth = int(cmd[cmd.index('-w') + 1])
            if x + (dzenWidth // 2) > monitorWidth:
                return self.options['menuCommand'] + ' -x ' + str(monitorWidth - dzenWidth)
            elif x - (dzenWidth // 2) < 0:
                return self.options['menuCommand'] + ' -x ' + str(dzenWidth)
            else:
                return self.options['menuCommand'] + ' -x ' + str(x - (dzenWidth // 2))
        else:
            return self.options['menuCommand']

    def displayDzen(self, event):
        """
        Make a call to subprocess in order to display the dzen menu. May replace
        the use of shell=True.
        """
        subprocess.call(self.positionDzen(event['x']), shell=True)
