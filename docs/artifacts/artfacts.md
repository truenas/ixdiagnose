# Artifacts
path: **ixdiagnose/artifacts**

### Overview
The artifacts help to copy system logs and files in to the debug that are generated automatically by the system
and can be used to gain insight into the system's performance, problems, etc.

Currently, there are two types of artifacts available in **iXdiagnose**:
- Logs
- System Info

The design of artifacts is based on each artifact generating a directory in the debug directory. The directory name is
the name of the artifact. The directory contains the files and directories that the artifact copies over.

Artifacts consume `items` which hold the logic for copying files and directories. Please refer to `items` documentation
for more details.

Both of the above artifacts inherits from base artifact under **ixdiagnose/artifacts/base.py** .

### The Base Artifact Class

path: **ixdiagnose/artifacts/base.py**

The above file contains the base class **Artifact**,
which is inherited by other artifacts. It is an abstract base class that provides the structure for creating artifacts.

Attributes
- base_dir
: A string that represents the base directory which will be current working directory when
copying over files/directories via items.

- name
: A string that represents the name of the artifact which will be used to create the directory
in the artifacts debug directory.

- individual_item_max_size_limit
: An optional integer that represents the maximum size limit for each individual item specified in the `items` list.

- items
: A list of **Item** instances that represents the items that the artifact is composed of.

Methods
- __init__(self)
: Initializes an instance of the **Artifact** class.
It sets the `debug_report` attribute to an empty dictionary, and checks that the `base_dir`, `name`, and `items`
attributes are of the correct type and not empty. If `individual_item_max_size_limit` is not `None`, it sets the
maximum size limit for each item in the `items` list using `item.max_size`.

- output_dir(self)
: A property that returns the full path of the output directory for the artifact.

- write_debug_report(self)
: Writes the debug_report dictionary to a file named report.json in the output directory.

- gather(self)
: This method creates the output directory, calls the `gather_impl` method, and writes the `debug_report` to a file.
It returns a dictionary that contains information about the `execution_time`,
`execution_error` and `execution_traceback`.

- gather_impl(self)
: Collects data for each item in the `items` list. This method sets the `debug_report` for each item, which contains
information about the `execution_time`, item_execution_error, `item_execution_traceback`, and `item_report`.

### Adding a new artifact

When adding a new artifact to **iXdiagnose**, you must create a new Python file in the **ixdiagnose/artifacts**
directory. Following are some common attributes which are used when writing a new artifact:

Structure:
: `base_dir` defines the source folder from where the files or folders will be copied
: `name` defines the folder name of the artifact where all its files will be stored.
: `items` consists of **Item** instances list. It consists of items with the files or folder names to copy.
: `individual_item_max_size_limit` it sets the maximum size limit for each item in the `items` list.

Following are some basic steps on how to add a new artifact:
1. First, create a new Python file in the **ixdiagnose/artifacts** directory. This file will contain the code for your
new artifact. Name this file after your artifact name, for example, my_artifact.py.
2. Define the artifact class like following:
    ```
    from .base import Artifact
    from .items import File
    
    
    class MyArtifact(Artifact):
        base_dir = 'path/to/base/dir' # dir from where you want to copy files or directory
        name = 'your_artifact_folder_name' # folder in ixdiagnose debug specified items will be copied
        items = [
            File('file_name'), # file you want to copy from base_dir
        ]
    ```
   In the above code, 
   - `path/to/base/dir` is directory from where you want to copy files or folders
   - `your_artifact_folder_name` is folder in **iXdiagnose** debug where the artifact files will be copied
   - In `File('file_name')` **File** is a class inherits from **Item** class. It uses `file_name` you provide and copy
     the specified `file_name` file under `base_dir` in to the `your_artifact_folder_name`.
3. Add your artifact to `ArtifactFactory` in **ixdiagnose/artifacts/factory.py** file. Here is an example code:
    ```
    from ixdiagnose.utils.factory import Factory

    from .logs import Logs
    from .sys_info import SystemInfo
    from .my_artifact import MyArtifact # import your artifact
    
    
    artifact_factory = Factory()
    for artifact in [
        Logs,
        SystemInfo,
        MyArtifact # place your artifact in this list
    ]:
        artifact_factory.register(artifact())
    ```

That's it! You have successfully added a new artifact to the **iXdiagnose** package. 

Once the artifact has been added, it will be automatically discovered by **iXdiagnose** and added to the list of
available artifacts.
