from i3situation.plugins._plugin import Plugin

__all__ = 'TextPlugin'


class TextPlugin(Plugin):

    def __init__(self, config):
        self.options = {'text': '', 'interval': 1}
        super().__init__(config)

    def main(self):
        return self.output(self.options['text'], self.options['text'])
