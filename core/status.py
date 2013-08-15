import sys
from core import loader
from core import config
import time
import json


class Status():
    """
    Handles the running of the status utility and acts as the glue for the
    application.
    """
    def __init__(self, configFilePath):
        VERSION = 1
        self.outputToBar(json.dumps({'version': VERSION}), False)
        self.outputToBar('[', False)
        self.config = config.Config(configFilePath)
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
        time.sleep(0.5)
        data = []
        for obj in self.loader.objects:
            data.append(obj.main())
        self.outputToBar(json.dumps(data))
