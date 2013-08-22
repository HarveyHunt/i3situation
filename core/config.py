import os
import errno
import configparser
import logging


class Config():
    """
    Provides a simplified interface to the configuration of the application.
    """
    def __init__(self):
        folderLocations = [os.path.join(os.path.expanduser('~'), '.i3-py3-status'),
                '/etc/i3-py3-status']
        for path in folderLocations:
            if os.path.isdir(path):
                self._folderPath = path
                break
        else:
            self._folderPath = folderLocations[0]
            self._touchDir(self._folderPath)
        self.pluginPath = os.path.join(self._folderPath, 'plugins')
        self._touchDir(self.pluginPath)
        self.configPath = os.path.join(self._folderPath, 'config')
        if not os.path.isfile(self.configPath):
            open(self.configPath, 'w').close()
        self.pluginSettings, self.generalSettings = self.reload()

    def _touchDir(self, path):
        """
        A helper function to create a directory if it doesn't exist.
        """
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def reload(self):
        """
        Reload the configuration from the file. This is in its own function
        so that it can be called at any time by another class.
        """
        self._conf = configparser.SafeConfigParser()
        # Preserve the case of sections and keys.
        self._conf.optionxform = str
        self._conf.read(self.configPath)
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
