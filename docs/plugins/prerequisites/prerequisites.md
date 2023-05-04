## Prerequisites
path: **ixdiagnose/plugins/prerequisites**

: Prerequisites refer to the methods in **iXdiagnose** used to validate certain conditions that must be met before the
execution of a metric. Motivation for this hook is to provide a way to validate certain conditions before the execution
of a metric to avoid redundant calls and to improve the performance of the plugin/metric e.g if Active Directory is
not enabled, there is no point in running metrics which are going to query information from the AD environment. This
is where these Prerequisites can be used to validate if certain conditions are met before the execution of a metric.

#### Prerequisites Base Class
path: **ixdiagnose/plugins/prerequisites/base.py**

: There are two classes available in base.py file:

- CacheMeta
- Prerequisite

### CacheMeta
This class is a metaclass that initializes a `CACHE_RESULTS` dictionary for each new class created with this
metaclass. The `CACHE_RESULTS` dictionary is an empty dictionary that can be used to store cached results.

Following are methods and attributes of **CacheMeta**:

Methods
- new(cls, *args, **kwargs):
: This is a built-in method that is called when a new instance of a class is created. In this implementation, the
new method creates a new class using the `super().new` method and then initializes the `CACHE_RESULTS` dictionary for
the new class. The new class is then returned.

Attributes
- CACHE_RESULTS:
: This is a class-level attribute that is initialized to an empty dictionary for each new class created with this
metaclass. It can be used to store cached results for methods of the class.


### Prerequisite
**Prerequisite** is base class for all other prerequisites. It uses **CacheMeta** as a metaclass. 

#### Attributes

- CACHE_RESULTS
: This is a class-level attribute that is initialized to an empty dictionary for each new class created with this
metaclass. It can be used to store cached results for methods of the class.

- cache
: This is an instance-level attribute that is set to `False` by default but can be set to `True` if caching is desired
for this particular instance.

- cache_key
: This is an instance-level attribute that is set to `None` by default but can be set to a string value if caching
is desired and a specific cache key is needed for this particular instance. **cache_key** is used to get the cached
data from **CACHE_RESULTS**

#### Methods

- init(self, cache: bool = False)
: This method is called when a new instance of the class is created. It takes an optional boolean argument `cache`
which is set to `False` by default. If the `cache` argument is `True`, then the instance-level attribute `cache` is
set to `True`. It also initializes the instance-level attribute `cache_key` to `None`.

- evaluate(self) -> bool
: This method checks if the result for the prerequisite has already been cached using the `is_cached` method. If it
has, then the cached result is returned. Otherwise, the method calls the `evaluate_impl` method to obtain the result
and caches the result if the `cache` attribute is True and a `cache_key` has been specified.

- str(self)
: This method raises a **NotImplementedError**. It is intended to be overridden by subclasses to provide a string
representation of the prerequisite.

- evaluate_impl(self) -> bool
: This method is intended to be overridden by subclasses. It should implement the actual evaluation of the prerequisite
and return a boolean value representing whether the prerequisite is met or not.

- is_cached(self) -> bool
: This method checks if caching is enabled for this instance by checking if the `cache` attribute is True. If it is,
it checks if a `cache_key` has been specified for this instance and if it is present in the `CACHE_RESULTS` dictionary.
If both conditions are true, it returns True, indicating that the result has been cached.


There are total of three prerequisites available:
- **Active Directory Prerequisite**
- **Service Prerequisite**
- **LDAP Prerequisite**

### Active Directory Prerequisite
path: **ixdiagnose/plugins/prerequisites/active_directory.py**

**ActiveDirectoryStatePrerequisite** inherits from **Prerequisite** class.
It is used to define a prerequisite that checks the state of the Active Directory service. It inherits the
`CACHE_RESULTS`, `evaluate`, `is_cached`, and `init` methods from the **Prerequisite** class.

Methods
- evaluate_impl(self) -> bool
: This method overrides the `evaluate_impl` method of the Prerequisite class to implement the actual evaluation of the
prerequisite. It calls the `execute` method of the **MiddlewareCommand** class, passing the
`directoryservices.get_state` command to get the current state of the Active Directory service. It then returns
`True` if the state is not `DISABLED`, `False` otherwise.

- str(self)
: This method overrides the str method of the Prerequisite class to provide a string representation of the
**ActiveDirectoryStatePrerequisite** object. It returns a formatted string that includes the cache key (if present)
and a description of the prerequisite check.


### Service Prerequisite
path: **ixdiagnose/plugins/prerequisites/service.py**

This class is a subclass of the **Prerequisite** class and is used to define a prerequisite that checks whether a
specific system service is running. It inherits the `CACHE_RESULTS`, `evaluate`, `is_cached`, and `init` methods
from the **Prerequisite** class.

It will be used for example to see if a service is running and only then get it's relevant information i.e if `scst` is
not running, then we should not be querying it's state directly because it's stopped.

Methods
- init(self, service_name: str)
: This method overrides the `init` method of the **Prerequisite** class to initialize the `service_name` attribute,
which is the name of the system service to check, and to set caching to `True`. It also sets the `cache_key` to
the `service_name`.

- evaluate_impl(self) -> bool
: This method overrides the `evaluate_impl` method of the **Prerequisite** class to implement the actual evaluation
of the prerequisite. It calls the `run` function imported from **ixdiagnose/utils/run.py**. `run` function gets
`shell` command and executes it. Passing the `systemctl is-active --quiet [service_name]` command to check whether
the service is active. It then returns `True` if the return code from `run` command return values is `0`
(indicating that the service is active), `False` otherwise.

- str(self)
: This method overrides the `str` method of the **Prerequisite** class to provide a string representation of the
**ServiceRunningPrerequisite** object. It returns a formatted string that includes the service name and a description
of the prerequisite check.

### LDAP Prerequisites
path: **ixdiagnose/plugins/prerequisites/active_directory.py**

**LDAPStatePrerequisite** inherits from **Prerequisite** class
This class defines a prerequisite check that verifies whether the LDAP service is enabled or not.

Methods
- evaluate_impl(self) -> bool
: This method executes a **MiddlewareCommand** to retrieve the state of the `directoryservices`. It returns a boolean
value indicating whether the **LDAP** service is enabled or not.

- str(self)
: This method returns a string representation of the **LDAPStatePrerequisite** object. It includes the cache key and
the description of the **LDAP** service state check.
