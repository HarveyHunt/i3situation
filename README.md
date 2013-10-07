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
    loggingLevel = ERROR
    logFile = ~/.i3situation/log.txt
  
You then need to change the status_command value in the bar section of your i3
configuration to:

    status_command i3situation
    
Configuring Plugins
=============
Plugins are the way to get this application to output to i3bar and allow for large
amounts of expandability. The configuration file is automatically reloaded when
any changes occur to it. Changing the content of a plugin file will also cause
a reload of all plugins and settings.

Plugins are configured in the config file. You must first denote a new plugin
config section by using a unique name for that instance of a plugin. For example:

    [myNewsPlugin]

Inside this section you need to say which plugin you wish to use (Note: the plugin
field refers to the filename of the plugin less the .py extension).

    [myNewsPlugin]
    plugin = news
    
Each plugin needs to have an interval set. This interval refers to how often the
plugin's displayed text is updated.

    [myNewsPlugin]
    plugin = news
    interval = 30
    
You can then change the options for a plugin by defining them next. The available
options can be seen in the plugin file in a dictionary- with the defaults next to it.

A list of values should be comma separated and a boolean value can be written as:

- on
- True
- true
- off
- False
- false

The example below illustrates using a comma separated list:

    [myNewsPlugin]
    plugin = news
    interval = 30
    topics = uk,technology
    
You can also edit options that affect how the output is displayed (Note: the
same options are available for all plugins). The following example illustrates
changing the colour of the output:

    [myNewsPlugin]
    plugin = news
    interval = 30
    topics = uk,technology
    color = #808080

The rest of the output options that can be edited are discussed in the Advanced Plugin 
Options section of this document.

Below is an example of my i3situation config that I have been using since the start
of this project:

    [general]
    interval = 1
    loggingLevel = ERROR
    logFile = ~/.i3situation/log.txt
    colors = true
     
    [news]
    plugin = news
    interval = 30
    color = #808080
     
    [cmus]
    plugin = cmus
    interval = 1
    color = #808080
    format = ❴artist - title - position/duration❵
     
    [time]
    plugin= dateTime
    interval = 1
    color = #808080
    
Plugins
============

* [News](#news)
* [Cmus](#cmus)
* [Date and Time](#date and time)
* [Reddit](#reddit)
* [Run](#run)
* [Text](#text)

## News
The news plugin displays news from the BBC website.

Options:
* **Topics**: A comma seperated list of topics that shall be displayed.
(A full list of topics can be found [here](http://api.bbcnews.appengine.co.uk/topics))

```
topics=uk,technology
```

* **Format**: A string showing the format in which the output should be displayed.
 Keywords in the string will be replace with data. Possible keywords are time and news.

```
format=news @ time
```

## Cmus
A plugin to display information provided by Cmus (current song etc).

Options:
* **Format**: A string showing the format in which the output should be displayed.
 Keywords in the string will be replaced with data. Possible keywords can be found [here](i3situation/plugins/cmus.py).

```
format=artist -> title
```

## Date and Time
A plugin to display the current date and time. Has support for multiple time zones.

Options:
* **Time Zone**: The time zone that should be used when finding the time.

```
timeZone=GMT
```

* **Long Format**: The text to display when there is a large amount of space. A full list of 
format options can be found [here](http://docs.python.org/3/library/time.html#time.strftime)

```
longFormat=%d-%m-%Y %H:%M:%S
```

* **Short Format**: The text to be displayed when there is a smaller amount of bar space available.

```
shortFormat=%H:%M:%S
```

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
