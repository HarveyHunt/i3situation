import glob
import shutil
import imp
import logging
import time
import os.path
import threading
import compileall


class MissingPlugin(Exception):
    """
    The plugin that has been mentioned in the configuration file doesn't appear
    in the application's plugin directory.
    """
    pass


class Thread(threading.Thread):
    """
    A thread that runs a plugin's main function and mutates that outputdict
    in order to return the value of the plugin's main function. This is where
    a plugin's interval is taken into account.
    """

    def __init__(self, func, interval, output_dict):
        """
        func: The function that will be executed by the thread. It is always the
        main() function of a plugin.

        interval: How often the func is run. (Time in seconds).

        output_dict: A dictionary containing dictionaries. Is in the format:
        {plugin_name: {information about plugin}, ...}
        The information about plugin contains data such as the full_text and
        formatting options.
        """
        super().__init__(group=None, daemon=True)
        self.func = func
        self.output_dict = output_dict
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
            self.output_dict[ret['name']] = ret
            time.sleep(self.interval)
        return

    def stop(self):
        """
        Stop the thread from running.
        The thread doesn't stop immediately, it stops once the running
        variable is checked, after the thread's interval.
        """
        self.running = False


class ThreadManager():
    """
    Keeps track of threads and enables the creation and destruction of
    threads.

    The output_dict variable is a dictionary passed into the class that is then
    mutated by the threads in order to update the output of the application.
    This means that the main thread need only display the output and not poll
    for changes in the output data. It also means that queues are not needed.
    """

    def __init__(self, output_dict):
        """
        output_dict: Same as that used in the Thread class ^^^.
        """
        self._thread_pool = []
        self.output_dict = output_dict

    def add_thread(self, func, interval):
        """
        Creates a thread, starts it and then adds it to the thread pool.

        Func: Same as in the Thread class.
        Interval: Same as in the Thread class.
        """
        t = Thread(func, interval, self.output_dict)
        t.start()
        self._thread_pool.append(t)

    def kill_all_threads(self):
        """
        Provides an easy way to graciously end all threads.
        """
        for t in self._thread_pool:
            t.stop()
        self._thread_pool = []


class PluginLoader():
    """
    Loads classes from plugin files placed in the plugin directory.
    The plugin's class name must be the only part of the __all__
    variable. Any files that should not be loaded as plugins require
    an underscore at the start of their filename, such as:
    _plugin.py
    """
    def __init__(self, dir_path, config):
        self.dir_path = dir_path
        source_path = '/'.join(os.path.dirname(__file__).split('/')[0:-1])
        source_path = os.path.join(source_path, 'plugins')
        if len(glob.glob(self.dir_path + '/*')) < len(glob.glob(source_path + '/*')) \
                or os.path.getmtime(source_path) > os.path.getmtime(self.dir_path):
            shutil.rmtree(self.dir_path)
            shutil.copytree(source_path, self.dir_path)
        self._compile_files()
        self._config = config
        self.plugins = self.refresh_files()
        self.objects = self.load_objects()

    def _compile_files(self):
        """
        Compiles python plugin files in order to be processed by the loader.
        It compiles the plugins if they have been updated or haven't yet been
        compiled.
        """
        for f in glob.glob(os.path.join(self.dir_path, '*.py')):
            # Check for compiled Python files that aren't in the __pycache__.
            if not os.path.isfile(os.path.join(self.dir_path, f + 'c')):
                compileall.compile_dir(self.dir_path, quiet=True)
                logging.debug('Compiled plugins as a new plugin has been added.')
                return
            # Recompile if there are newer plugins.
            elif os.path.getmtime(os.path.join(self.dir_path, f)) > os.path.getmtime(
                os.path.join(self.dir_path, f + 'c')):
                compileall.compile_dir(self.dir_path, quiet=True)
                logging.debug('Compiled plugins as a plugin has been changed.')
                return

    def _load_compiled(self, file_path):
        """
        Accepts a path to a compiled plugin and returns a module object.

        file_path: A string that represents a complete file path to a compiled
        plugin.
        """
        name = os.path.splitext(os.path.split(file_path)[-1])[0]
        plugin_directory = os.sep.join(os.path.split(file_path)[0:-1])
        compiled_directory = os.path.join(plugin_directory, '__pycache__')
        # Use glob to autocomplete the filename.
        compiled_file = glob.glob(os.path.join(compiled_directory, (name + '.*')))[0]
        plugin = imp.load_compiled(name, compiled_file)
        return plugin

    def load_objects(self):
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
                plugin_class = getattr(module, module.__all__)
                objects.append(plugin_class(settings))
                logging.debug('Loaded a plugin object based upon {0}'.format(
                    settings['plugin']))
            else:
                logging.critical('Missing plugin {0} was not found in {1}'.format(
                    settings['plugin'], self.dir_path))
                raise MissingPlugin('The plugin {0} was not found in {1}'.format(
                    settings['plugin'], self.dir_path))
        return objects

    def refresh_files(self):
        """
        Discovers the available plugins and turns each into a module object.
        This is a seperate function to allow plugins to be updated
        dynamically by other parts of the application.
        """
        plugins = {}
        _plugin_files = glob.glob(os.path.join(self.dir_path, '[!_]*.pyc'))
        for f in glob.glob(os.path.join(self.dir_path, '[!_]*.py')):
            if not any(os.path.splitext(f)[0] == os.path.splitext(x)[0]
                    for x in _plugin_files):
                logging.debug('Adding plugin {0}'.format(f))
                _plugin_files.append(f)
        for f in _plugin_files:
            plugin = self._load_compiled(f)
            plugins[plugin.__name__] = plugin
            logging.debug('Loaded module object for plugin: {0}'.format(f))
        return plugins
