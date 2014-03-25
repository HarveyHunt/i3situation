i3situation
=============

A replacement for i3status written in Python 3 with support for huge
customisability through plugins.

Please feel free to send a pull request or request features by opening an issue.

Contents
============

* [Installation](#installation)
* [Configuring Plugins](#configuring-plugins)
* [Plugins](#plugins)
* [Creating A Plugin](#creating-a-plugin)
    * [Events](#events)
* [Advanced Plugin Options](#advanced-plugin-options)

Installation
=============

If you're lucky enough to be using Arch Linux, i3situation is available from the [AUR](https://aur.archlinux.org/packages/i3situation-git/).

i3situation is also available over at [PyPi](https://pypi.python.org/pypi/i3situation/1.0.1).

If you want to install straight from this git repository, first clone it and then change
into the cloned directory.

    git clone https://github.com/HarveyHunt/i3situation
    cd i3situation

You then need to install i3situation using the setup.py file that is provided.

    sudo python setup.py install
    
Next, use your editor of choice to create a configuration file.

    vim ~/.config/i3situation/config
    
The minimum that you need to enter in order to run the application is as
follows:

    [general]
    interval = 1
    logging_level = ERROR
    log_file = ~/.config/i3situation/log.txt
  
You then need to change the status_command value in the bar section of your i3
configuration to:

    status_command i3situation
    
It is a good idea to run i3situation at this point, as it will handle copying over the
plugins into your configuration directory.
    
Configuring Plugins
=============
Plugins are the way to get this application to output to i3bar and allow for large
amounts of expandability. The configuration file is automatically reloaded when
any changes occur to it. Changing the content of a plugin file will also cause
a reload of all plugins and settings.

Plugins are configured in the config file. You must first denote a new plugin
config section by using a unique name for that instance of a plugin. For example:

    [my_time_plugin]

Inside this section you need to say which plugin you wish to use (Note: the plugin
field refers to the filename of the plugin less the .py extension).

    [my_time_plugin]
    plugin = date_time
    
Each plugin needs to have an interval set. This interval refers to how often the
plugin's displayed text is updated.

    [my_time_plugin]
    plugin = date_time
    interval = 1

Each plugin has an on_click function already defined. This function allows the user to
specify a shell command that should be executed each time a plugin's text area is clicked
with a mouse button (of which there are three, defined [here](#events)). For example:

    [my_time_plugin]
    plugin = date_time
    interval = 1
    button1 = urxvt
    button2 = xterm
    
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

    [my_reddit_plugin]
    plugin = reddit
    interval = 30
    mode = subreddit
    subreddits = programming,linux
    
You can also edit options that affect how the output is displayed (Note: the
same options are available for all plugins). The following example illustrates
changing the colour of the output:

    [my_reddit_plugin]
    plugin = reddit
    interval = 30
    mode = subreddit
    subreddits = programming,linux
    color = #808080

The rest of the output options that can be edited are discussed in the Advanced Plugin 
Options section of this document.

My personal i3situation configuration file can be found with my [dotfiles](https://github.com/harvey_hunt/dotfiles).
    
Plugins
============

* [Cmus](#cmus)
* [Date and Time](#date and time)
* [Reddit](#reddit)
* [Run](#run)
* [Text](#text)
* [Conky](#conky)
* [Battery](#battery)

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
time_zone=GMT
```

* **Long Format**: The text to display when there is a large amount of space. A full list of 
format options can be found [here](http://docs.python.org/3/library/time.html#time.strftime)

```
long_format=%d-%m-%Y %H:%M:%S
```

* **Short Format**: The text to be displayed when there is a smaller amount of bar space available.

```
short_format=%H:%M:%S
```

##Reddit
A plugin that can display information from Reddit, such as post titles and upvotes.

Options:
* **Mode**: The mode that the plugin shall operate in. Front page will display threads from the 
front page of Reddit or your personal front page (provided you have logged in).

```
mode=front
```

* **Subreddits**: The subreddits that should be displayed when the plugin is in subreddit mode. 
Should be in the form of a comma seperated list.

```
subreddits=vim,python
```

* **Username**: Your Reddit username.

```
username=segfaultless
```

* **Password**: Your Reddit password.

```
password=lamepassword
```

* **Limit**: The amount of threads that should be requested from Reddit in one go.

```
limit=25
```

* **Format**: The format that the plugin's output should be presented in. Keywords will 
be replaced with actual data. For a full list of keywords, look [here](i3situation/plugins/reddit.py)

```
format=subreddit title ups
```

* **Sort**: The method with which the Reddit threads are sorted.

```
sort=hot
```

## Run
A plugin to run shell commands and send the output to i3bar.

* **Command**: The command that is to be executed.

```
command=echo Hello
```

## Text
A simple plugin to output text.

* **Text**: The text that will be displayed.

```
text=Hello World
```

## Conky
A plugin to allow conky's output to be displayed. It is required that you have a valid .conkyrc

* **Command**: The conky command to be executed.

```
command=$uptime
```

* **Config**: The path to the conkyrc file that shall be used.

```
config=~/.conkyrc
```

## Battery
A plugin that displays information about the battery, such as charge level and status.

* **format**: The format of the output. <status> will be replaced by the battery's current status
and <charge> will be replaced by the current charge level.

```
format=<charge>%
```

* **percentage**: Whether or not the charge should be calculated as a percentage.

```
percentage=True
```

* **low_threshold**: The value of charge below which the low_color will be displayed. Note: this value
should be from 0 to 1 when percentage isn't set and 0 to 100 when it is set.

```
low_threshold=20
```

* **low_color**: The colour to be displayed when the battery charge level is classed as low.

```
low_color=#FF0000
```

* **discharging_color**: The colour to be displayed when the battery is discharging.

```
discharging_color=#FF6103
```

* **charging_color**: The colour to be displayed when the battery is charging.

```
charging_color=#00F000
```

* **full_color**: The colour to be displayed when the battery is full.

```
full_color=#FFFFFF
```

* **battery_path**: The path to the battery file- generally in the form /sys/class/power_supply/BATX.

```
battery_path=/sys/class/power_supply/BAT0
```

Creating a Plugin
=============

Creating a plugin is a simple process, made easier by the Plugin base class.
The first step is to create a python
file in your plugin directory. Note: Files with a leading underscore will not
be loaded as a plugin but can be
used for library files.

    vim cool_feature.py

The Plugin base class needs to be imported from the plugins folder.

```python
from plugins._plugin import Plugin
```    

You should then create a class that inherits the newly imported Plugin class.

```python
from plugins._plugin import Plugin


class cool_feature_plugin(Plugin):
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
{'option': 'default_value'}
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
        self.options = {'cool_option': 'cool_value', 'interval': 1}
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
        self.options = {'cool_option': 'cool_value', 'interval': 1}
        super().__init__(config, self.options)
    
    def main(self):
        return self.output('This is a fabulous plugin', 'Cool plugin')
```

Events
-----------

It is also possible to create a function that gets executed whenever the plugin's output
is clicked. The plugin must have an on_click() function that handles the event. The function
must accept an event dictionary as an argument- the layout of which is below:

```
{'button': 1, 'name': 'time', 'y': 1196, 'x': 1846}
```

The button corresponds to which mouse button was used to click the text. The mouse buttons are 
numbered as follows:

1. Left Mouse Button
2. Middle Mouse Button
3. Right Mouse Button

The x and y variables refer to the position that the text was clicked at.

The name refers to the name of the plugin object that was clicked.

It is possible to do many things once the text has been clicked, but please bear in mind that
the on_click() code will be run in the same thread as the event handler. Therefore, it is important
that any code in on_click() isn't too intensive.

Adding an on_click() function to the cool_feature_plugin looks as follows:

```python
from plugins._plugin import Plugin

__all__ = 'CoolFeaturePlugin'


class CoolFeaturePlugin(Plugin):

    def __init__(self, config):
        self.options = {'cool_option': 'cool_value', 'interval': 1}
        super().__init__(config, self.options)
    
    def main(self):
        return self.output('This is a fabulous plugin', 'Cool plugin')
    
    def on_click(self, event):
        if event['button'] == 1:
            self.output_options['color'] = '#FF0000'
        else:
            self.output_options['color'] = '#0000FF'
```

This is all the code required to create a plugin. There are lots of good
examples of how to write
plugins in this [project's plugin
directory](https://github.com/harvey_hunt/i3situation/tree/master/i3situation/plugins)

Advanced Plugin Options
=============

It is also possible to manipulate many aspects of a plugin's output. The Plugin
class provides
a way to set the value of output options (blocks). Changing values in the
following dictionary
will affect the output options:

```python
self.output_options['color'] = '#FF00FF'
```

The following is the internal representation of output options used in the
Plugin class.

```python
self.output_options = {
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
