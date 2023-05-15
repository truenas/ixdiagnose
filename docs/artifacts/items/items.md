# Items

path: **ixdiagnose/artifacts/items**

Items define logic that is used to copy files or directories from system to **iXdiagnose** debug folder.
There are three items available currently:
- Directory
- File
- Pattern

### Item Base Class

path: **ixdiagnose/artifacts/items/base.py**

It defines a class **Item** that provides methods to copy an item from a source directory to a destination directory.
It also includes methods to check whether the item exists, whether it should be copied, and to perform some
initialization and post-copy actions.

Methods
- __init__(self, name: str, max_size: Optional[int] = None)

: Initializes an Item object with a name and an optional maximum size for the item.

- exists(self, item_path: str) -> Tuple[bool, str]

: Checks whether the item at the specified path exists.

- size(self, item_path: str) -> int

: Gets the size of the item at the specified path.

- size_check(self, item_path) -> Tuple[bool, Optional[str]]

: Checks whether the item at the specified path is within the maximum size limit. If the maximum size is not set,
this method returns `True`. If the item is larger than the maximum size, this method returns `False` and an error message.

- to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[Union[str, Dict[str, str]]]]

: Performs any additional checks to determine whether the item should be copied.

- is_to_be_copied(self, item_path) -> Tuple[bool, Optional[Union[str, Dict[str, str]]]]

: Checks whether the item should be copied based on whether it exists and whether it passes any additional checks. If
the item should be copied, this method returns `True`. If not, it returns `False` and an error message.

- source_item_path(self, item_dir: str) -> str

: Gets the full path to the source item based on the specified directory and the item name.

- destination_item_path(self, destination_dir: str) -> str

: Gets the full path to the destination item based on the specified directory and the item name.

- initialize_context(self, item_path: str) -> None

: Initializes the context for the copy operation.

- post_copy_hook(self, destination_path: str)

: Performs any post-copy actions.

- copy(self, item_dir: str, destination_dir: str) -> dict

: Copies the item from the source directory to the destination directory and returns a dictionary with a report of
the copy operation. The report includes an `error`,`traceback`, and a list of the `copied_items`
(which is always the item being copied or an empty list if an error occurred).

- copy_impl(self, item_path: str, destination_path: str) -> list

: Performs the actual copy operation and returns a list of the copied items.

### Directory Item
path: **ixdiagnose/artifacts/items/directory.py**
The **Directory** class implements methods to copy a directory recursively, validate if the directory exists and
check its size.

Functions
get_directory_size(directory: str) -> int
: Calculates the size of a given directory by summing the size of each file and subdirectory within it using the
`Path.rglob()` method. The result is the sum of all file sizes and the size of the root directory itself.

copy2(copied_files: list, src: str, dst: str) -> str
: A function that is used as the `copy_function` parameter in the `shutil.copytree()` method. This function copies a
file from source to destination using `shutil.copy2()` and appends the src path to a list of `copied_files`.

#### Class
Directory(Item)
to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[str]]
: A method that checks if the directory exists and can be copied. If it can be copied, it calls the `size_check()`
method to check if the directory size exceeds the maximum size. If the directory does not exist or cannot be
copied, it returns a tuple containing `False` and an error message. If the directory can be copied, it returns a
tuple containing `True` and `None`.

size(self, item_path: str) -> int
: A method that returns the size of the given directory using the `get_directory_size()` function.

copy_impl(self, item_path: str, destination_path: str) -> list
: A method that copies the directory from the source path `item_path` to the destination path `destination_path`
using `shutil.copytree()`. It also uses the `copy2()` function as the `copy_function` parameter to append the paths
of the copied files to a list and returns this list of copied items.

### Pattern
The purpose of this class is to represent a pattern that matches a set of items in a directory. The items that match
the pattern are represented by **Item** objects (either **Directory** or **File** objects), and are stored in a list
called `items`.

Attributes
- name
: A string representing the name of the pattern

- max_size
: An optional integer representing the maximum size of the pattern (in bytes) that can be copied

- truncate_files
: An optional boolean indicating whether files that exceed the `max_size` limit should be truncated

Methods
- __init__(self, name: str, max_size: Optional[int] = None, truncate_files: Optional[bool] = True)
: The constructor method for the class. It initializes the `name`, `max_size`, and `truncate_files` attributes.

- initialize_context(self, item_path: str) -> None
: This method initializes the `items` list by creating **Item** objects for each item that matches the pattern in the
directory specified by `item_path`. The `max_size` and `truncate_files` attributes of each **Item** object are set
to the values specified in the **Pattern** object's constructor.

- exists(self, item_path: str) -> Tuple[bool, str]
: This method checks whether there are any items that match the pattern in the directory specified by `item_path`.
It returns a tuple where the first element is a boolean indicating whether there are any matching items, and the
second element is an error message if there are no matching items.

- source_item_path(self, item_dir: str) -> str
: This method returns the source path for an item that matches the pattern in the directory specified by `item_dir`.

- destination_item_path(self, destination_dir: str) -> str
: This method returns the destination path for an item that matches the pattern in the directory
specified by `destination_dir`.

- to_copy_items(self, items_path: str) -> list
: This method returns a list of items in the directory specified by `items_path` that match the pattern.

- size(self, item_path: str) -> int
: This method calculates the total size of all the items that match the pattern in the directory
specified by `item_path`.

- to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[dict]]
: This method checks whether all the items that match the pattern in the directory specified by `item_path`
can be copied. It returns a tuple where the first element is a boolean indicating whether all the items can be
copied, and the second element is a dictionary of error messages for any items that cannot be copied.

- copy_impl(self, item_path: str, destination_path: str) -> list
: This method copies all the items that match the pattern in the directory specified by `item_path` to the
directory specified by `destination_path`. It returns a list of the items that were copied.

### Adding new items
To add a new item in path **ixdiagnose/artifacts/items**, follow these steps:
1. Create a new Python file with a unique name for your item, e.g. my_item.py.
2. Define a new class for your item by inheriting from the **Item** class in **base.py**. For example, if your item
is a file, you can name the class **MyFile**.
3. Implement the required methods for your item. At a minimum, you must implement the `copy_impl` method, which
performs the actual copying of the item. You may also want to implement other methods such as `size`,
`to_be_copied_checks`, `initialize_context`, and `post_copy_hook`, depending on the needs of your item.
4. Here is the example template:
    ```
    import os
    import shutil
    
    from .base import Item
    
    
    class MyItem(Item):
    
        def __init__(self, name: str, max_size: Optional[int] = None):
            super().__init__(name=name, max_size=max_size)
    
            # TODO: Add any additional initialization code here
    
        def size(self, item_path: str) -> int:
            # TODO: Implement method to calculate the size of the item
            pass
    
        def to_be_copied_checks(self, item_path: str) -> Tuple[bool, Optional[str]]:
            # TODO: Implement method to check if the item should be copied
            pass
    
        def initialize_context(self, item_path: str) -> None:
            # TODO: Implement method to initialize any necessary context before copying
            pass
    
        def post_copy_hook(self, destination_path: str) -> None:
            # TODO: Implement method to perform any necessary actions after copying
            pass
    
        def copy_impl(self, item_path: str, destination_path: str) -> list:
            # TODO: Implement method to perform the actual copying of the item
            pass

    ```
You can also see already added items under path **ixdiagnose/artifacts/items**.
