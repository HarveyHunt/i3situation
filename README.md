i3situation
=============

A replacement for i3status written in Python 3 with support for huge customisability through plugins.

Installation
=============

At the moment, the way to install i3situation is in a manual manner. It is assumed that this repository has been
cloned and that you're in the folder that was cloned.

    sudo python setup.py install
    mkdir ~/.i3situation
    cp -r plugins/ ~/.i3situation/
    
Next, use your editor of choice to create a configuration file.

    vim ~/.i3situation/config
    
The minimum that you need to enter in order to run the application is as follows:

    [general]
    interval = 1
    loggingLevel = DEBUG
    logFile = ~/.i3situation/log.txt
  
You then need to change the status_command value in the bar section of your i3 configuration to:

    status_command i3situation.py

TODO
=============

The following need to be implemented in newer versions, the order in which they are displayed is not significant.
- Multithreading support: This will allow plugins to have correct control over their update interval as well as 
preventing plugins that rely on network connections from holding up the main thread.
- Support for lists in the config parser: This needs to be implemented in order to allow users to specify a list
for a config option- such as topics for the news plugin. I think the best way to implement this is by allowing
the user to enter python syntax for lists and implementing a parser for this in Config._replaceDataTypes.
- Investigate the slow updating: The i3bar updates slowly, despite i3situation passing it information at the
correct speed.
- Consider whether sections require a unique name: Removing the use of a unique name would make config files look
cleaner and more intuitive, but is against the i3bar input protocol recommendations.
- Create more documentation: More documentation needs to be created in regards to plugin development and installation.
