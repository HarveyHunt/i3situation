import os
import errno
import configparser


class IncompleteConfigurationFile(ValueError):
    pass

class Config():
    """
    Provides a simplified interface to the configuration of the application.

    Accepts a list of folder_locations that are then checked for validity.
    """
    def __init__(self, folder_locations):
        for path in folder_locations:
            if os.path.isdir(path):
                self._folder_path = path
                break
        else:
            self._folder_path = folder_locations[0]
            self._touch_dir(self._folder_path)
        self.plugin_path = os.path.join(self._folder_path, 'plugins')
        if not os.path.exists(self.plugin_path):
            self._touch_dir(self.plugin_path)
        self.config_file_path = os.path.join(self._folder_path, 'config')
        if not os.path.exists(self.config_file_path):
            self.create_default_config()
        self.plugin, self.general = self.reload()

    def _touch_dir(self, path):
        """
        A helper function to create a directory if it doesn't exist.

        path: A string containing a full path to the directory to be created.
        """
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def create_default_config(self):
        s = '[general]\ninterval = 1\nlogging_level = ERROR\n' \
            'log_file = ~/.config/i3situation/log.txt\ncolors = true'
        with open(self.config_file_path, 'w') as f:
            f.write(s)

    def reload(self):
        """
        Reload the configuration from the file. This is in its own function
        so that it can be called at any time by another class.
        """
        self._conf = configparser.ConfigParser()
        # Preserve the case of sections and keys.
        self._conf.optionxform = str
        self._conf.read(self.config_file_path)
        if 'general' not in self._conf.keys():
            raise IncompleteConfigurationFile('Missing the general section')
        general = self._replace_data_types(dict(self._conf.items('general')))
        self._conf.remove_section('general')
        plugin = []
        for section in self._conf.sections():
            plugin.append(dict(self._conf.items(section)))
            plugin[-1].update({'name': section})
            plugin[-1] = self._replace_data_types(plugin[-1])
        return (plugin, general)

    @staticmethod
    def _replace_data_types(dictionary):
        """
        Replaces strings with appropriate data types (int, boolean).
        Also replaces the human readable logging levels with the integer form.

        dictionary: A dictionary returned from the config file.
        """
        logging_levels = {'NONE': 0, 'NULL': 0, 'DEBUG': 10, 'INFO': 20,
                'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}
        for k, v in dictionary.items():
            if v in ['true', 'True', 'on']:
                dictionary[k] = True
            elif v in ['false', 'False', 'off']:
                dictionary[k] = False
            elif k == 'log_file' and '~' in v:
                dictionary[k] = v.replace('~', os.path.expanduser('~'))
            elif v in logging_levels:
                dictionary[k] = logging_levels[v]
            elif isinstance(v, str) and v.isnumeric():
                dictionary[k] = int(v)
            elif ',' in v:
                dictionary[k] = [x.strip() for x in v.split(',')]
        return dictionary
