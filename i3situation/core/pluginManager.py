import glob
import imp
import logging
import time
import os.path
import threading
import compileall


class MissingPlugin(Exception):
    pass


class Thread(threading.Thread):
    """
    A thread that runs a plugin's main function and mutates that outputdict
    in order to return the value of the plugin's main function. This is where
    a plugin's interval is taken into account.
    """

    def __init__(self, func, interval, outputDict):
        super().__init__(group=None, daemon=True)
        self.func = func
        self.outputDict = outputDict
        self.interval = interval

    def run(self):
        """
        Calls the main function of a plugin and mutates the output dict
        with its return value. Provides an easy way to change the output
        whilst not needing to constantly poll a queue in another thread and
        allowing plugin's to manage their own intervals.
        """
        self.running = True
        while self.running:
            ret = self.func()
            self.outputDict[ret['name']] = ret
            time.sleep(self.interval)
        return

    def stop(self):
        self.running = False


class ThreadManager():
    """
    Keeps track of threads and enables the creation and destruction of
    threads.

    The outputDict variable is a dictionary passed into the class that is then
    mutated by the threads in order to update the output of the application.
    This means that the main thread need only display the output and not poll
    for changes in the output data. It also means that queues are not needed.
    """

    def __init__(self, outputDict):
        self._threadPool = []
        self.outputDict = outputDict

    def addThread(self, func, interval):
        """
        Creates a thread, starts it and then adds it to the thread pool.
        """
        t = Thread(func, interval, self.outputDict)
        t.start()
        self._threadPool.append(t)

    def killAllThreads(self):
        """
        Provides an easy way to graciously end all threads.
        """
        for t in self._threadPool:
            t.stop()
        self._threadPool = []


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
        self._compileFiles()
        self._config = config
        self.plugins = self.refreshFiles()
        self.objects = self.loadObjects()

    def _compileFiles(self):
        """
        Compiles python plugin files in order to be processed by the loader.
        It compiles the plugins if they have been updated or haven't yet been
        compiled.
        """
        for f in glob.glob(os.path.join(self.dirPath, '*.py')):
            # Check for compiled Python files that aren't in the __pycache__.
            if not os.path.isfile(os.path.join(self.dirPath, f + 'c')):
                compileall.compile_dir(self.dirPath, quiet=True)
                logging.debug('Compiled plugins as a new plugin has been added.')
                return
            # Recompile if there are newer plugins.
            elif os.getmtime(os.path.join(self.dirPath, f)) > os.getmtime(
                os.path.join(self.dirPath, f + 'c')):
                compileall.compile_dir(self.dirPath, quiet=True)
                logging.debug('Compiled plugins as a plugin has been changed.')
                return

    def _loadCompiled(self, filePath):
        """
        Accepts a path to a compiled plugin and returns a module object.
        """
        name = os.path.splitext(os.path.split(filePath)[-1])[0]
        pluginDirectory = os.sep.join(os.path.split(filePath)[0:-1])
        compiledDirectory = os.path.join(pluginDirectory, '__pycache__')
        # Use glob to autocomplete the filename.
        compiledFile = glob.glob(os.path.join(compiledDirectory, (name + '.*')))[0]
        plugin = imp.load_compiled(name, compiledFile)
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
                logging.debug('Loaded a plugin object based upon {0}'.format(
                    settings['plugin']))
            else:
                logging.critical('Missing plugin {0} was not found in {1}'.format(
                    settings['plugin'], self.dirPath))
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
                logging.debug('Adding plugin {0}'.format(f))
                _pluginFiles.append(f)
        for f in _pluginFiles:
            plugin = self._loadCompiled(f)
            plugins[plugin.__name__] = plugin
            logging.debug('Loaded module object for plugin: {0}'.format(f))
        return plugins
