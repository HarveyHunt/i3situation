import sys
import logging
import time
import json
import os
from core import loader
from core import config


class Status():
    """
    Handles the running of the status utility and acts as the glue for the
    application.
    """
    def __init__(self):
        VERSION = 1
        self.outputToBar(json.dumps({'version': VERSION}), False)
        self.outputToBar('[', False)
        self.config = config.Config()
        self._configFilePath = self.config.configPath
        self._pluginPath = self.config.pluginPath
        self._configModTime = os.path.getmtime(self._configFilePath)
        logger = logging.getLogger()
        handler = logging.FileHandler(self.config.generalSettings['logFile'])
        # Remove standard stream handler as it will interfere with the JSON
        # output.
        logger.removeHandler(logger.handlers[0])
        logger.addHandler(handler)
        formatter = logging.Formatter(('[%(asctime)s] - %(levelname)s'
           ' - %(filename)s - %(funcName)s - %(message)s'),
           '%d/%m/%Y %I:%M:%S %p')
        handler.setFormatter(formatter)
        logger.setLevel(self.config.generalSettings['loggingLevel'])
        handler.setLevel(self.config.generalSettings['loggingLevel'])
        self._pluginModTime = os.path.getmtime(self._configFilePath)
        self.loader = loader.PluginLoader(
            self._pluginPath, self.config.pluginSettings)

    def outputToBar(self, message, comma=True):
        """
        Outputs data to stdout, without buffering.
        """
        if comma:
            message += ','
        sys.stdout.write(message + '\n')

    def run(self):
        """
        Calls a plugin's main method after each interval.
        """
        # Reload plugins and config if either the config file or plugin
        # directory are modified.
        if self._configModTime != os.path.getmtime(self._configFilePath) or \
        self._pluginModTime != os.path.getmtime(self._pluginPath):
            self.config.pluginSettings, self.config.generalSettings = self.config.reload()
            self.loader = loader.PluginLoader(
                self._pluginPath, self.config.pluginSettings)

        time.sleep(self.config.generalSettings['interval'])
        data = []
        for obj in self.loader.objects:
            data.append(obj.main())
        self.outputToBar(json.dumps(data))
