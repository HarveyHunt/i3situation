import glob
import imp
import os.path


class MissingPlugin(Exception):
    pass


class PluginLoader():
    """
    Loads classes from plugin files placed in the plugin directory.
    The plugin's class name must be the only part of the __all__
    variable. Any files that should not be loaded as plugins require
    an underscore at the start of their filename, such as:
    _plugin.py
    """
    def __init__(self, dirPath, config):
        self.dirPath = dirPath
        self._config = config
        self.plugins = self.refreshFiles()
        self.objects = self.loadObjects()

    def _loadFromFile(self, filePath):
        """
        Accepts a path to a plugin and returns a module object.
        Also works with compiled python files.
        """
        name, ext = os.path.splitext(os.path.split(filePath)[-1])
        ext = ext.lower()
        if ext == '.pyc':
            plugin = imp.load_compiled(name, filePath)
        elif ext == '.py':
            plugin = imp.load_source(name, filePath)
        return plugin

    def loadObjects(self):
        """
        Matches the plugins that have been specified in the config file
        with the available plugins. Returns instantiated objects based upon
        the classes defined in the plugins.
        """
        objects = []
        for settings in self._config:
            if settings['plugin'] in self.plugins:
                module = self.plugins[settings['plugin']]
                # Trusts that the only item in __all__ is the name of the
                # plugin class.
                pluginClass = getattr(module, module.__all__)
                objects.append(pluginClass(settings))
            else:
                raise MissingPlugin('The plugin {0} was not found in {1}'.format(
                    settings['plugin'], self.dirPath))
        return objects

    def refreshFiles(self):
        """
        Discovers the available plugins and turns each into a module object.
        This is a seperate function to allow plugins to be updated
        dynamically by other parts of the application.
        """
        plugins = {}
        _pluginFiles = glob.glob(os.path.join(self.dirPath, '[!_]*.pyc'))
        for f in glob.glob(os.path.join(self.dirPath, '[!_]*.py')):
            if not any(os.path.splitext(f)[0] == os.path.splitext(x)[0]
                    for x in _pluginFiles):
                _pluginFiles.append(f)
        for f in _pluginFiles:
            plugin = self._loadFromFile(f)
            plugins[plugin.__name__] = plugin
        return plugins
