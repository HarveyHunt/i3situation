from i3situation.plugins._plugin import Plugin

__all__ = 'TextPlugin'


class TextPlugin(Plugin):

    def __init__(self, config):
        self.options = {'text': '', 'color': '#FFFFFF', 'interval': 1}
        super().__init__(config, self.options)
        # A sad americanism.
        self._outputOptions['color'] = self.options['color']

    def main(self):
        return self.output(self.options['text'], self.options['text'])
