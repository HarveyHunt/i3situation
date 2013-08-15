class Plugin():
    """
    A base class that should be inherited by all other plugins.
    It handles defaults, replacing options and managing lower level
    settings that a plugin developer need not bother with.
    """
    def __init__(self, config, defaults):
        self._outputOptions = {
            'color': '#FFFFFF',
            'min_width': 1,
            'align': 'center',
            'name': '',
            'urgent': False,
            'seperator': True,
            'seperator_block_width': 9}
        # Replace default values with user defined ones.
        for k, v in config.items():
            self.options[k] = v
            if k in self._outputOptions.keys():
                self._outputOptions[k] = v

    def output(self, fullText, shortText):
        """
        Output all of the options and data for a segment.
        """
        self._outputOptions.update({'full_text': fullText, 'short_text': shortText})
        return self._outputOptions
