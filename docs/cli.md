# CLI Documentation for iXdiagnose

`ixdiagnose` is a command-line tool designed to generate debug information on TrueNAS systems. This documentation provides an overview of the available commands, options, and their usage.

## Commands

### `run` - Generate Complete Debug

The `run` command generates a comprehensive debug report for your TrueNAS system. It allows you to customize the debug generation process with various options.

Options:

- **-s, --serialized:** Generate debug in structured form.
- **-c, --compress:** Get compressed debug. Provide a complete file path for the compressed output.
- **--debug-path:** Path where you want to save the debug.
- **-t, --timeout:** Timeout value for middleware client in seconds (default: 20).
- **-Xa, --exclude-artifacts:** Exclude specific artifacts from the debug report. Provide a comma-separated list.
- **-Xp, --exclude-plugins:** Exclude specific plugins from the debug report. Provide a comma-separated list.

Example:

```commandline
ixdiagnose run -s --debug-path /path/to/debug -t 30 -Xa logs,sys_info -Xp smb,vm,network
```


### `artifact` - Gather Artifacts
The `artifact` command gathers various system artifacts. It is useful for collecting specific information for diagnostic purposes.

Options:

- **--debug-path:** Path where you want to save the collected artifacts.
- **-t, --timeout:** Timeout value for the artifact collection process in seconds (default: 20).
- **-X, --exclude:** Exclude specific artifacts from the collection. Provide a comma-separated list.

Example:

```commandline
ixdiagnose artifact --debug-path /path/to/artifacts -t 30 -X logs,sys_info
```


### `plugin` - Generate Plugins' Debug
The `plugin` command generates debug information specifically related to TrueNAS plugins. It allows you to exclude specific plugins from the generated report.

Options:

- **--debug-path:** Path where you want to save the plugins' debug.
- **-t, --timeout:** Timeout value for the plugin debug generation process in seconds (default: 20).
- **-X, --exclude:** Exclude specific plugins from the debug report. Provide a comma-separated list.

Example:

```commandline
ixdiagnose plugin --debug-path /path/to/plugin-debug -t 30 -X smb,vm,network
```


### Common Options

- **--help:** Display the help message for the specific command.


### Notes
Paths provided for **--debug-path** or **--compress** must be absolute.

When using --compress, ensure that the specified compressed path does not already exist.
