# File System Hierarchy of iXdiagnose


This document outlines the file system hierarchy of **iXdiagnose**. It is intended for developers who want to contribute to **iXdiagnose**.

Base file system hierarchy of **iXdiagnose**:

```commandline
ixdiagnose
├── Dockerfile
├── ixdiagnose (Directory)
├── LICENSE
├── README.md
├── requirements.txt
├── setup.cfg
└── setup.py
```

All the contributions involving **iXdiagnose** should be done in the **ixdiagnose** directory.


### Hierarchy of ixdiagnose directory:

```commandline
ixdiagnose/ixdiagnose
├── artifact.py
├── artifacts (Directory)
├── config.py
├── event.py
├── exceptions.py
├── __init__.py
├── cli.py
├── plugin.py
├── plugins (Directory)
├── run.py
├── test (Directory)
└── utils (Directory)
```

#### Files and Folders of interest

- `artifact.py` contains the logic which is used to gather the artifacts.
- `config.py` contains the logic which is used to parse the configuration file.
- `event.py` contains the logic which is used to manage the event management used to give real updates on debug generation.
- `cli.py` contains the logic which is used to parse the command line arguments and run the application.
- `plugin.py` contains the logic which is used to manage the plugins.
- `run.py` contains the logic which is used to run the plugins.
- `utils` contains the utility functions used by the application.
- `plugins` directory contains the plugins used by the application.
- `artifacts` directory contains the artifacts used by the application.
- `test` directory contains the tests for the application.
- `exceptions.py` contains the custom exceptions used by the application.

### Hierarchy of plugins

`plugins` directory contains plugins which will be executed when the application runs. The plugins are divided into
different categories based on the functionality they provide.

```commandline
ixdiagnose/plugins
├── active_directory.py
├── base.py
├── factory.py
├── hardware.py
├── __init__.py
├── iscsi.py
├── ldap.py
├── metrics
│   ├── base.py
│   ├── command.py
│   ├── directory_tree.py
│   ├── file.py
│   ├── __init__.py
│   ├── middleware.py
│   └── python.py
├── network.py
├── nfs.py
├── prerequisites
│   ├── active_directory.py
│   ├── base.py
│   ├── __init__.py
│   └── service.py
├── replication.py
├── services.py
├── smart.py
├── smb.py
├── ssl.py
├── sysctl.py
├── system.py
├── vm.py
└── zfs.py

```

### Hierarchy of artifacts


```commandline
ixdiagnose/artifacts
├── base.py
├── factory.py
├── __init__.py
├── items
│   ├── base.py
│   ├── directory.py
│   ├── file.py
│   ├── __init__.py
│   └── pattern.py
├── logs.py
└── sys_info.py
```
