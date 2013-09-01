i3situation
=============

A replacement for i3status written in Python 3 with support for huge
customisability through plugins.

Installation
=============

At the moment, the way to install i3situation is in a manual manner. It is
assumed that this repository has been
cloned and that you're in the folder that it was cloned into.

    sudo python setup.py install
    mkdir ~/.i3situation
    cp -r plugins/ ~/.i3situation/
    
Next, use your editor of choice to create a configuration file.

    vim ~/.i3situation/config
    
The minimum that you need to enter in order to run the application is as
follows:

    [general]
    interval = 1
    loggingLevel = DEBUG
    logFile = ~/.i3situation/log.txt
  
You then need to change the status_command value in the bar section of your i3
configuration to:

    status_command i3situation
    
Creating a Plugin
=============

Creating a plugin is a simple process, made easier by the Plugin base class.
The first step is to create a python
file in your plugin directory. Note: Files with a leading underscore will not
be loaded as a plugin but can be
used for library files.

    vim coolFeature.py

The Plugin base class needs to be imported from the plugins folder.

```python
from plugins._plugin import Plugin
```    

You should then create a class that inherits the newly imported Plugin class.

```python
from plugins._plugin import Plugin


class CoolFeaturePlugin(Plugin):
```    

The \_\_all\_\_ variable needs to be set to the name of your plugin class.

```python
from plugins._plugin import Plugin

__all__ = 'CoolFeaturePlugin'


class CoolFeaturePlugin(Plugin):
```

The \_\_init\_\_ function needs to accept two arguments- self and config. The
options that can be
configured by the user need to be placed in a dictionary called self.options
with the format:

```python
{'option': 'defaultValue'}
```

Options that can be configured by the user should be declared before calling
the super class'
\_\_init\_\_ function.

The super class' \_\_init\_\_ function must be passed two arguments- config and
the user configurable
options. There is only one compulsary option- interval. This refers to how
often (in seconds) the
main function of the plugin should be called.

```python
from plugins._plugin import Plugin

__all__ = 'CoolFeaturePlugin'


class CoolFeaturePlugin(Plugin):

    def __init__(self, config):
        self.options = {'coolOption': 'coolValue', 'interval': 1}
        super().__init__(config, self.options)
```

All plugins must have a main() function that is called by the plugin loader.
Within this function,
program logic should be executed and it should return a dictionary to the main
application. The 
Plugin base class provides a helper function called output that serves this
purpose. Output should
be passed a string as the first argument that represents a detailed output of
the plugin and a shorter
string as the second argument. It is perfectly acceptable to pass the same
value to each argument.

```python
from plugins._plugin import Plugin

__all__ = 'CoolFeaturePlugin'


class CoolFeaturePlugin(Plugin):

    def __init__(self, config):
        self.options = {'coolOption': 'coolValue', 'interval': 1}
        super().__init__(config, self.options)
    
    def main(self):
        return self.output('This is an amazing and fabulous plugin', 'This is a
great plugin')
```

This is all the code required to create a plugin. There are lots of good
examples of how to write
plugins in this [project's plugin
directory](https://github.com/HarveyHunt/i3situation/tree/master/i3situation/plugins)

Advanced Plugin Options
=============

It is also possible to manipulate many aspects of a plugin's output. The Plugin
class provides
a way to set the value of output options (blocks). Changing values in the
following dictionary
will affect the output options:

```python
self._outputOptions['color'] = '#FF00FF'
```

The following is the internal representation of output options used in the
Plugin class.

```python
self._outputOptions = {
    'color': None,
    'min_width': None,
    'align': None,
    'name': None,
    'urgent': None,
    'seperator': None,
    'seperator_block_width': None}
```

For a full explanation of each output option, please refer to section 2.2 of
the excellent 
i3bar documentation:
[i3Bar Protocol](http://i3wm.org/docs/i3bar-protocol.html)
TODO
=============

The following need to be implemented in newer versions, the order in which they
are displayed is not significant.

~~Multithreading support.~~

~~Support for lists in the config parser.~~
- Investigate the slow updating: The i3bar updates slowly, despite i3situation
  passing it information at the
correct speed.
- Create more documentation: More documentation needs to be created in regards
  to plugin development and installation.

