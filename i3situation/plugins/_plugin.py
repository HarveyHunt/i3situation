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
            'separator': None,
            'separator_block_width': None}
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
        to events, if it wants to perform any action other than running the
        supplied command related to a button.

        event: A dictionary passed from i3bar (after being decoded from JSON)
        that has the folowing format:

        event = {'name': 'my_plugin', 'x': 231, 'y': 423}
        Note: It is also possible to have an instance key, but i3situation
        doesn't set it.
        """
        if event['button'] == 1 and 'button1' in self.options:
            subprocess.call(self.options['button1'].split())
        elif event['button'] == 2 and 'button2' in self.options:
            subprocess.call(self.options['button2'].split())
        elif event['button'] == 3 and 'button3' in self.options:
            subprocess.call(self.options['button3'].split())
