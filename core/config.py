import configparser
import logging


class Config():
    """
    Provides a simplified interface to the configuration of the
    application.
    """
    def __init__(self, filepath):
        self._filePath = filepath
        self.pluginSettings, self.generalSettings = self.reload()
        print(self.generalSettings)

    def reload(self):
        """
        Reload the configuration from the file. This is in its own function
        so that it can be called at any time by another class.
        """
        self._conf = configparser.SafeConfigParser()
        # Preserve the case of sections and keys.
        self._conf.optionxform = str
        self._conf.read(self._filePath)
        general = self._replaceDataTypes(dict(self._conf.items('general')))
        self._conf.remove_section('general')
        pluginSettings = []
        for index, section in enumerate(self._conf.sections()):
            pluginSettings.append(dict(self._conf.items(section)))
            pluginSettings[index].update({'name': section})
            pluginSettings[-1] = self._replaceDataTypes(pluginSettings[-1])
        logging.debug('Test')
        return (pluginSettings, general)

    def _replaceDataTypes(self, dictionary):
        """
        Replaces strings with appropriate data types (int, boolean).
        Also replaces the human readable logging levels with the integer form
        """
        loggingLevels = {'NONE': 0, 'NULL': 0, 'DEBUG': 10, 'INFO': 20, 'WARNING': 30,
                         'ERROR': 40, 'CRITICAL': 50}
        for k, v in dictionary.items():
            if v in ['true', 'True', 'on']:
                dictionary[k] = True
            elif v in ['false', 'False', 'off']:
                dictionary[k] = False
            elif v in loggingLevels:
                dictionary[k] = loggingLevels[v]
            elif isinstance(v, str) and v.isnumeric():
                dictionary[k] = int(v)
        return dictionary
