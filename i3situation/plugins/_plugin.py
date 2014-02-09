import subprocess
import json

class Plugin():
    """
    A base class that should be inherited by all other plugins.
    It handles defaults, replacing options and managing lower level
    settings that a plugin developer need not bother with.

    config: A dictionary obtained from the config parser that has the
    user's configuration, as defined in their config file.
    """
    def __init__(self, config):
        self.output_options = {
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
        self.output_options.update((k, v) for k, v in config.items() if k in
                                   self.output_options)

    def output(self, full_text, short_text):
        """
        Output all of the options and data for a segment.

        full_text: A string representing the data that should be output to i3bar.
        short_text: A more concise version of full_text, in case there is minimal
        room on the i3bar.
        """
        self.output_options.update({'full_text': full_text, 'short_text': short_text})
        self.output_options = {k: v for k, v in self.output_options.items() if v}
        return self.output_options

    def on_click(self, event):
        """
        A function that should be overwritten by a plugin that wishes to react
        to events.

        event: A dictionary passed from i3bar (after being decoded from JSON)
        that has the folowing format:

        event = {'name': 'my_plugin', 'x': 231, 'y': 423}
        Note: It is also possible to have an instance key, but i3situation
        doesn't set it.
        """
        pass

    def position_dzen(self, x):
        """
        Calculate the correct position that dzen2 should appear, so as
        to prevent the pop up from going off the screen.

        The popup will be centered on the mouse click. Both sides of the
        monitor need to be checked to ensure that the pop up doesn't go off
        of the screen.

        x: The x value on the screen at which the click event took place.
        """
        if not '-x' in self.options['menu_command']:
            i3outputs = subprocess.check_output(['i3-msg', '-t', 'get_outputs'])
            i3outputs = json.loads(i3outputs.decode('utf-8'))
            monitor_width = [x['rect']['width'] for x in i3outputs if x['active']][0]
            cmd = self.options['menu_command'].split()
            dzen_width = int(cmd[cmd.index('-w') + 1])
            if x + (dzen_width // 2) > monitor_width:
                return self.options['menu_command'] + ' -x ' + str(monitor_width - dzen_width)
            elif x - (dzen_width // 2) < 0:
                return self.options['menu_command'] + ' -x ' + str(dzen_width)
            else:
                return self.options['menu_command'] + ' -x ' + str(x - (dzen_width // 2))
        else:
            return self.options['menu_command']

    def display_dzen(self, event):
        """
        Make a call to subprocess in order to display the dzen menu. May replace
        the use of shell=True.
        """
        subprocess.call(self.position_dzen(event['x']), shell=True)
