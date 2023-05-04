## Overview

The **iXdiagnose** repository features a plugin folder that houses the plugin architecture and various diagnostic
check implementations for TrueNAS systems. These plugins are separate Python classes which are responsible for
gathering different subsystem's information.

Each plugin is responsible for gathering information from a specific subsystem. For example, the `hardware.py` plugin
will be gathering information about the hardware of the system, such as CPU, memory, and disks.

The design of the plugin architecture is such that a plugin targets a subsystem and gathers information from it. The
actual retrieval of that specific information is handled by `Metric` objects. Each plugin has a list of `Metric`
objects which are executed when the plugin is executed. The `Metric` objects are responsible for gathering different
type of information as required and writing their own separate files in the plugin directory in the debug directory.

### Plugin (The base class)
path: **ixdiagnose/plugins/base.py**

: The Plugin class is a base class for all plugins in the **iXdiagnose** repository. It defines the common
functionalities required for a plugin to execute and retrieve diagnostic information in TrueNAS systems.

: Motivation is that the base class of plugin should be able to execute the metrics and generate the debug report
whereas developers can focus on writing metrics in child classes which just dictate which data to retrieve.

Attributes
- metrics
: A list of **Metric** objects to be executed. These can be serializable / non-serializable metrics.

- raw_metrics
: A list of **Metric** objects which are not able to retrieve serialized data.

- serializable_metrics
: A list of **Metric** objects which are able to retrieve serialized data.

- name
: a string that represents the name of the plugin

Methods:
- __init__
: Initializes the class instance and validates that the class attributes are of the correct type.

- output_dir
: Returns the output directory path for the plugin.

- metrics_to_execute
: Returns a list of Metric objects to be executed based on the `conf.structured_data` configuration.

- execute_metrics
: Creates the output directory if it does not exist, executes the metrics, and generates the debug report.

- execute_impl
: Executes the metrics and captures the `execution_time`, `metric_report`, `metric_output`, `metric_execution_error`
and `metric_execution_traceback`.

- write_debug_report
: write the debug report to a JSON file. Writes error to a `report.json` file.

- execute
: Executes the `execute_metrics` and `write_debug_report` methods and returns an execution summary, including the
`execution_time`, `execution_error`, and `execution_traceback`.


Each plugin uses **Plugin** base class. The implementation structure for every plugin is same.

### Structure for Plugins

Inheritance

: Every plugin inherits from **Plugin** base class. Every new plugin generally overrides `name`, `metrics`,
`raw_metrics` and `serializable_metrics` attributes of **Plugin** class.
: `name` defines the folder name of the plugin where all its debug files will be stored. All the above metrics
inherit from **Metric** class.

: Moving on about retrieving data with metrics for a plugin, we wanted to be able to have ability to retrieve
serialized data and raw data. How-ever for some data points that is not possible and they only get us either raw or
serializable data but not both. For example, `middleware` commands can only return raw data but not serializable data.
Based on this we have 3 types which we can specify in the plugin's class:

- `metrics` attribute
- `raw_metrics` attribute
- `serializable_metrics` attribute

`metrics` attribute is a list of **Metric** objects which can return either raw or serializable data. It is aimed
for those metrics which cannot return both raw/serializable data.

`raw_metrics` and `serializable_metrics` are used when we have datapoints which we can get in both raw/serializable
forms. For example, getting ZFS pool's data - we can get in both raw form and serializable form. So, we can specify
necessary ZFS pool metric in both `raw_metrics` and `serializable_metrics` attributes which means that based on user
specification/preference he can switch to serializable or raw data.
 
## Adding a new Plugin in iXdiagnose

### When it is appropriate to add a new plugin?

Plugins should be added only for those services that are frequently targeted for diagnosing issues or for those
`middleware` commands that are frequently used in finding errors or issues in `middleware`.

Note: 
: Adding a new plugin(s) greatly effects performance of **iXdiagnose**. We should be mindful when adding new
plugin(s) in **iXdiagnose**.

To add a new plugin to **iXdiagnose**, you will need to follow these steps:

1. Create a new Python file for your plugin under the plugins directory of the **iXdiagnose** package. For example,
if you want to create a plugin named my_plugin, create a file named `my_plugin.py` under the plugins directory.
2. Define your plugin class by inheriting from the **Plugin** base class. You can use the following code as a template:

    ```
    from ixdiagnose.plugins.base import Plugin
    
    class MyPlugin(Plugin):
        name = 'myplugin'
        metrics = [
            # Add your metrics here after importing them
        ]
        serializable_metrics = [
            # Add metrics here
        ]
        raw_metrics = [
            # Add metrics here
    ```
    In this code, replace `MyPlugin` with the name of your plugin, and add your metrics to the `metrics` list.
   Some metrics can provide output in both serializable and raw text form.
   With `serilizable_metrics` and `raw_metrics` present you can decide weather
   you want their output in json form or not. **iXdiagnose** provide following metrics:
   - Command Metric
   - Directory Tree Metric
   - File Metric
   - Middleware Metric
   - Python Metric

   Note:
   : If you want to create your own metric, see metrics docs.

3. Import your plugin in the **ixdiagnose/plugins/factory.py**. Here is an example on how to add it:
    ```commandline
    from ixdiagnose.utils.factory import Factory
    
    from .active_directory import ActiveDirectory
    from .my_plugin import MyPlugin
    
    plugin_factory = Factory()
    for plugin in [
        ActiveDirectory,
        ... # other plugins
        MyPlugin,
    ]:
        plugin_factory.register(plugin())
    ```

    In the above code, replace MyPlugin with the name of your plugin.

This will execute your plugin and generate output in a directory named my_plugin under the debug directory.

That's it! You have successfully added a new plugin to the **iXdiagnose** package. 

Once your plugin is added, it should be automatically discovered by the **iXdiagnose** and added to the list of
available plugins. Furthermore, you can see already added plugins under **ixdiagnose/plugins** folder.
