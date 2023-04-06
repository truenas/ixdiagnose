import inspect
import os


def get_asset(filename):
    caller_module = inspect.getmodule(inspect.stack()[1][0])
    caller_module_dir = os.path.dirname(os.path.abspath(caller_module.__file__))
    with open(os.path.join(caller_module_dir, 'assets', filename), 'r') as f:
        return f.read()
