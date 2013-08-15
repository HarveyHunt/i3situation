import configparser
import os.path


class Config():
    """
    Provides a simplified interface to the configuration of the
    application.
    """
    def __init__(self, filepath):
        if filepath is None:
            self._filePath = os.path.join(os.path.expanduser('~'), '.i3-py3-status.conf')
        else:
            self._filePath = filepath
        self._conf = configparser.SafeConfigParser()
        self._conf.read(self._filePath)
        self.pluginSettings, self.generalSettings = self.reload()

    def reload(self):
        """
        Reload the configuration from the file. This is in its own function
        so that it can be called at any time by another class.
        """
        general = self._replaceDataTypes(dict(self._conf.items('general')))
        self._conf.remove_section('general')
        pluginSettings = []
        for index, section in enumerate(self._conf.sections()):
            pluginSettings.append(dict(self._conf.items(section)))
            pluginSettings[index].update({'name': section})
            pluginSettings[-1] = self._replaceDataTypes(pluginSettings[-1])
        return (pluginSettings, general)

    def _replaceDataTypes(self, dictionary):
        """
        Replaces strings with appropriate data types (int, boolean).
        """
        for k, v in dictionary.items():
            if v in ['true', 'True', 'on']:
                dictionary[k] = True
            elif v in ['false', 'False', 'off']:
                dictionary[k] = False
            elif isinstance(v, str) and v.isnumeric():
                dictionary[k] = int(v)
        return dictionary
