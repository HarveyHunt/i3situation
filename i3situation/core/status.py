import sys
import logging
import time
import json
import os
from i3situation.core import pluginManager
from i3situation.core import config


class Status():
    """
    Handles the running of the status utility and acts as the glue for the
    application.
    """
    def __init__(self):
        self.config = config.Config()
        self.outputDict = {}
        self._configFilePath = self.config.configPath
        self._pluginPath = self.config.pluginPath
        self._configModTime = os.path.getmtime(self._configFilePath)
        self._pluginModTime = os.path.getmtime(self._pluginPath)
        logger = logging.getLogger()
        # If a stream handler has been attached, remove it.
        if logger.handlers:
            logger.removeHandler(logger.handlers[0])
        handler = logging.FileHandler(self.config.generalSettings['logFile'])
        logger.addHandler(handler)
        formatter = logging.Formatter(('[%(asctime)s] - %(levelname)s'
           ' - %(filename)s - %(funcName)s - %(message)s'),
           '%d/%m/%Y %I:%M:%S %p')
        handler.setFormatter(formatter)
        logger.setLevel(self.config.generalSettings['loggingLevel'])
        handler.setLevel(self.config.generalSettings['loggingLevel'])
        logging.debug('Config loaded from {0}'.format(self._configFilePath))
        logging.debug('Plugin path is located at {0}'.format(self._pluginPath))
        logging.debug('Last config modification time is: {0}'.format(self._configModTime))
        logging.debug('Last plugin directory modification time is: {0}'.format(self._pluginModTime))
        self.outputToBar('{\"version\":1}', False)
        self.outputToBar('[', False)
        logging.debug('Sent initial JSON data to i3bar.')
        logging.debug('Beginning plugin loading process')
        self.loader = pluginManager.PluginLoader(
            self._pluginPath, self.config.pluginSettings)
        self.threadManager = pluginManager.ThreadManager(self.outputDict)

    def outputToBar(self, message, comma=True):
        """
        Outputs data to stdout, without buffering.
        """
        if comma:
            message += ','
        sys.stdout.write(message + '\n')

    def reload(self):
        logging.debug('Reloading config file as files have been modified.')
        self.config.pluginSettings, self.config.generalSettings = self.config.reload()
        logging.debug('Reloading plugins as files have been modified.')
        self.loader = pluginManager.PluginLoader(
            self._pluginPath, self.config.pluginSettings)
        self._pluginModTime = os.path.getmtime(self._pluginPath)
        self._configModTime = os.path.getmtime(self._configFilePath)

    def runPlugins(self):
        for obj in self.loader.objects:
            self.threadManager.addThread(obj.main, obj.options['interval'])

    def run(self):
        """
        Calls a plugin's main method after each interval.
        """
        self.runPlugins()
        while True:
            # Reload plugins and config if either the config file or plugin
            # directory are modified.
            if self._configModTime != os.path.getmtime(self._configFilePath) or \
            self._pluginModTime != os.path.getmtime(self._pluginPath):
                self.threadManager.killAllThreads()
                self.reload()
                self.runPlugins()
            self.outputToBar(json.dumps(list(self.outputDict.values())))
            logging.debug('Output to bar')
            time.sleep(self.config.generalSettings['interval'])
