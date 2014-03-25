import unittest
import os
import errno
import configparser

from i3situation.core import config


class TestDataTypeReplacement(unittest.TestCase):

    def test_replace_data_types(self):
        self.assertEqual(config.Config._replace_data_types({'': 'true'})[''],
                        True)
        self.assertEqual(config.Config._replace_data_types({'': 'True'})[''],
                        True)
        self.assertEqual(config.Config._replace_data_types({'': 'on'})[''],
                        True)

        self.assertEqual(config.Config._replace_data_types({'': 'false'})[''],
                        False)
        self.assertEqual(config.Config._replace_data_types({'': 'False'})[''],
                        False)
        self.assertEqual(config.Config._replace_data_types({'': 'off'})[''],
                        False)

        self.assertEqual(config.Config._replace_data_types(
                    {'log_file': '~'})['log_file'], os.path.expanduser('~'))

        self.assertEqual(config.Config._replace_data_types({'': '1'})[''],
                        1)

        self.assertEqual(config.Config._replace_data_types({'': '1, 2, 3'})[''],
                        ['1', '2', '3'])

        for level, value in {'NONE': 0, 'NULL': 0, 'DEBUG': 10, 'INFO': 20,
                'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}.items():
            self.assertEqual(config.Config._replace_data_types({'': level})[''],
                        value)


class TestConfigIncorrectFile(unittest.TestCase):
    def setUp(self):
        if os.environ.get('$XDG_CONFIG_HOME', None):
            self.folder_location = [os.path.join(os.environ.get('$XDG_CONFIG_HOME'),
                'i3situation', 'tests')]
        else:
            self.folder_location = [os.path.join(os.path.expanduser('~'), '.config',
                'i3situation', 'tests')]

    def test_no_config(self):
        with self.assertRaises(TypeError):
            c = config.Config()

    def test_empty_config(self):
        self._create_config('')
        with self.assertRaises(config.IncompleteConfigurationFile):
            c = config.Config(self.folder_location)

    def test_wrong_permissions(self):
        with self.assertRaises(PermissionError):
            c = config.Config('/root/')

    def test_wrong_path(self):
        with self.assertRaises(OSError):
            c = config.Config(os.path.join(os.path.expanduser('~'),
                                            'i3situation-test'))

    def test_missing_header(self):
        self._create_config('WRONGDATA')
        with self.assertRaises(configparser.MissingSectionHeaderError):
            c = config.Config(self.folder_location)

    def test_incomplete_header(self):
        self._create_config('[gener]')
        with self.assertRaises(config.IncompleteConfigurationFile):
            c = config.Config(self.folder_location)

    def test_default_general_config(self):
        default_general_config = config.Config._replace_data_types({'interval':
            '1', 'logging_level': 'ERROR', 'log_file':
            '~/.config/i3situation/log.txt', 'colors': 'True'})
        self._create_default_config()
        conf = config.Config(self.folder_location)
        self.assertEqual(conf.general, default_general_config)

    def _create_config(self, config_string):
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
        _touch_dir(self, self.folder_location[0])
        with open(os.path.join(self.folder_location[0], 'config'), 'w') as f:
            f.write(config_string)

    def _create_default_config(self):
        s = '[general]\ninterval = 1\nlogging_level = ERROR\n' \
            'log_file = ~/.config/i3situation/log.txt\ncolors = true'
        self._create_config(s)


if __name__ == '__main__':
    unittest.main()
