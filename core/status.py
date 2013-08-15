import sys
from core import loader
from core import config
import time
import json
import os


class Status():
    """
    Handles the running of the status utility and acts as the glue for the
    application.
    """
    def __init__(self, configFilePath):
        VERSION = 1
        self.outputToBar(json.dumps({'version': VERSION}), False)
        self._configFilePath = configFilePath
        self._configModTime = os.path.getmtime(configFilePath)
        self.config = config.Config(self._configFilePath)
        self._pluginModTime = os.path.getmtime(self.config.generalSettings['plugins'])
        self.outputToBar('[', False)
        self.loader = loader.PluginLoader(
            self.config.generalSettings['plugins'], self.config.pluginSettings)

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
        self._pluginModTime != os.path.getmtime(self.config.generalSettings['plugins']):
            self.config.pluginSettings, self.config.generalSettings = self.config.reload()
            self.loader = loader.PluginLoader(
                self.config.generalSettings['plugins'], self.config.pluginSettings)

        time.sleep(self.config.generalSettings['interval'])
        data = []
        for obj in self.loader.objects:
            data.append(obj.main())
        self.outputToBar(json.dumps(data))
