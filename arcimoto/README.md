# Arcimoto Core Package

The `arcimoto` package provides common behaviors and functionality for Python lambda functions. Functionality is broken down into specific namespaces as follows.

## arcimoto.args

Argument parsing and input validation.

### register(schema)

The register function should be called in global context within your lambda to configure input validation. The `schema` argument is a dictionary defining how the event passed to the lambda handler will be validated.

If a validation schema is registered, validation will happen automatically along with other runtime automation by the `@arcimoto.runtime.handler` decorator. Calling `register(None)` will disable validation.

Validation is implemented by the [Cerberus package](https://docs.python-cerberus.org/en/latest/) and all [Cerberus rules](https://docs.python-cerberus.org/en/latest/validation-rules.html) are valid within the schema.

```python
arcimoto.args.register({
    'name': {'type': 'string'},
    'id': {'type': 'integer', 'min': 1, 'required': True}
})
```

During validation, all registered inputs are checked. If there are any failures then all errors are returned as the `data` element within an ArcimotoArgumentError.

**NOTE:** The Cerberus option `allow_unknown` is enabled for validation. This permits additional data to be included in the lambda event that is *not* validated, making the validation system effectively *opt in*.

## arcimoto.db

Shared database implementation.

### get_cursor(role=None)

Gets a DB cursor that can be used for arbitrary queries. Will automatically open a DB connection if it's not already open, and will return an already open connection for subsequent calls.

**NOTE:** A lambda gets the appropriate DB credentials by sniffing the environment name from `arcimoto.runtime.get_env()`, fetching the execution role of the lambda as assigned in the console from `arcimoto.runtime.get_role()` and building the secret name from those components and a fixed format of : `<role_name>.db.<env>`. The role name used can be overridden by explicitly passing it in.

```python
cursor = arcimoto.db.get_cursor()
cursor.execute("SELECT * FROM table")
```

### close(role=None)

Will close any open and cached DB connection.

**NOTE:** A lambda gets the appropriate DB credentials by sniffing the environment name from `arcimoto.runtime.get_env()`, fetching the execution role of the lambda as assigned in the console from `arcimoto.runtime.get_role()` and building the secret name from those components and a fixed format of : `<role_name>.db.<env>`. The role name used can be overridden by explicitly passing it in.

```python
arcimoto.db.close()
```

### @transaction

Using the `@transaction` decorator provides the wrapped function with automatic rollback functionality if any exceptions are thrown during execution. On exception, the shared DB connection is issued a rollback and the exception is re-raised to be handled in the normal flow.

This variant uses the default lambda execution role to determine which DB connection to manage.

```python
@arcimoto.db.transaction
def update_unique_thing(thing_data):
    cursor = arcimoto.db.get_cursor()
    cursor.execute("UPDATE table SET field=%s WHERE unique=%s", [thing_data, UNIQUE_THING])

    if cursor.rowcount != 1:
        raise ArcimotoException("That update didn't go as planned")
```

### @transaction_for_role(role_name)

Using the `@transaction_for_role` decorator provides the wrapped function with automatic rollback functionality if any exceptions are thrown during execution. On exception, the shared DB connection is issued a rollback and the exception is re-raised to be handled in the normal flow.

This variant requires you to specify an explicit role to use for connection management.

```python
@arcimoto.db.transaction_for_role('custom.role')
def update_unique_thing(thing_data):
    cursor = arcimoto.db.get_cursor(role='custom.role')
    cursor.execute("UPDATE table SET field=%s WHERE unique=%s", [thing_data, UNIQUE_THING])

    if cursor.rowcount != 1:
        raise ArcimotoException("That update didn't go as planned")
```

## arcimoto.exceptions

All Arcimoto exceptions are in the `arcimoto.exceptions` namespace. All exceptions are configured to be exported by default, however a general `import *` is not best practices, so import the exception types you need, like:

```python
from arcimoto.exceptions import ArcimotoArgumentError
```

All runtime exceptions should be descendents of the `ArcimotoException` class in order to trigger automatic lambda runtime handling specific to each type of exception.

### ArcimotoException

Base exception class for all Arcimoto lambda exceptions. In addition to the standard `message` argument, you can additionally pass keyword arguments for `data` and `source`. These arguments are primarily used by concrete subclasses to enhance Exception handling.

```python
try:
    raise ArcimotoException("Something went wrong")
except ArcimotoException as e:
    logger.debug("Error from module {}".format(e.source))
```

### ArcimotoAlertException

Indicates an exception that should generate a notification message through the standard message broker.

#### ArcimotoFirmwareAlertException

Indicates an exception that should generate a notification message through the standard message broker into the `#firmware-notifications{-ENV if not prod}` channel.

#### ArcimotoManufacturingAlertException

Indicates an exception that should generate a notification message through the standard message broker into the `#manufacturing-notifications{-ENV if not prod}` channel.

#### ArcimotoNetworkAlertException

Indicates an exception that should generate a notification message through the standard message broker into the `#network-notifications{-ENV if not prod}` channel.

#### ArcimotoOrdersAlertException

Indicates an exception that should generate a notification message through the standard message broker into the `#orders-notifications{-ENV if not prod}` channel.

#### ArcimotoREEFAlertException

Indicates an exception that should generate a notification message through the standard message broker into the `#REEF-notifications{-ENV if not prod}` channel.

#### ArcimotoReplicateAlertException

Indicates an exception that should generate a notification message through the standard message broker into the `#replicate-notifications{-ENV if not prod}` channel.

#### ArcimotoServiceAlertException

Indicates an exception that should generate a notification message through the standard message broker into the `#service-notifications{-ENV if not prod}` channel.

#### ArcimotoTelemetryAlertException

Indicates an exception that should generate a notification message through the standard message broker into the `#telemetry-notifications{-ENV if not prod}` channel.

#### ArcimotoYRiskAlertException

Indicates an exception that should generate a notification message through the standard message broker into the `#yrisk-notifications{-ENV if not prod}` channel.

### ArcimotoHighAlertException

Indicates an exception that should generate a notification message through the standard message broker. This exception is intended to be more severe than an `ArcimotoAlertException`.

### ArcimotoPermissionError

Raise a permission or access control related exception. Thrown automatically if required permissions are not assigned to the current user.

### ArcimotoArgumentError

Raise an exception related to invalid argument/input. Thrown automatically if input validation fails.

### ArcimotoNotFoundError

Raise an exception related to not finding a requested resource.

### ArcimotoNoStepUnrollException

Raise a specific exception type that step_wrapper will use to signal that it should not unroll any executed steps.

## arcimoto.note

The `note` namespace provides several message and notification objects you can use to deliver alerts and notifications through the standard Arcimoto message broker.

### Message

Base class for all "message" types within `arcimoto.note`. Not intended to be directly used.

### Notification

Class used to send notifications to registered communication channels in the message broker.

```python
arcimoto.note.Notification("My custom notification")
```

### Note

Notes are used to attach arbitrary comments to resources within the Arcimoto data model.
The base `Note` class provides common functionality and isn't intended to be used directly.

### VehicleNote

Attach a note to a vehicle.  

```python
arcimoto.note.VehicleNote("VIN12345", "My custom vehicle note")`
```

### AuthorityNote

Attach a note to an an authority.

```python
arcimoto.note.AuthorityNote("ArcimotoRentalService", "My custom authority note")`
```

### UserNote

Attach a note to a user.

```python
arcimoto.note.UserNote("username@arcimoto.com", "My custom User note")`
```

## arcimoto.runtime

The `runtime` package provides lambda runtime and function related conveniences.

### @handler

Using the `@handler` decorator indicates the primary entry point for the lambda runtime function. Many automated behaviors are implemented by this decorator:

1. The context, environment, function details and role are automatically collected and stored for access in a consistent manner. These details enable multiple autoconfiguration conveniences throughout the rest of the `arcimoto` package.

2. If a validation schema has been registered with `arcimoto.args.register()` then input validation of the `event` argument is performed. If validation fails, an `ArcimotoArgumentError` is raised and the ```data``` property of the exception will be set to a list of *all* argument failures and their reasons.

3. The function is executed and the result is captured for return.

4. Any `ArcimotoAlertException` or `ArcimotoHighAlertExceptions` are automatically caught and will trigger notifications through the message broker before being re-raised.

**NOTE:** You must declare the `lambda_handler` symbol manually in order for the AWS lambda environment to locate your entry point:

```python
@arcimoto.runtime.handler
def main_function(validated_arg_1, validated_arg_2):
    # insert custom lambda code here

lambda_handler = main_function
```

### get_env()

Will return the current execution environment (dev, staging or prod) of the invoked lambda.

```python
if arcimoto.runtime.get_env() == arcimoto.runtime.ENV_DEV:
    # we're in dev
elif arcimoto.runtime.get_env() == arcimoto.runtime.ENV_STAGING:
    # we're in staging
elif arcimoto.runtime.get_env() == arcimoto.runtime.ENV_PROD:
    # we're in prod
```

### get_function_name()

Returns the current lambda function name, without any variable or environment qualifiers. Useful for logging, notifications, etc.

### get_role()

Returns the execution role assigned to the lambda.

### invoke_lambda()

Invokes an AWS lambda by name with the arguments given.

## arcimoto.tests

### test_vin_get()

Gets the global variable test_vin from this package.

### vehicle_create()

Wrapper to create a vehicle with the vehicle object. VIN defaults to 'TEST-VIN' in prod and '$ENVIRONMENT$-TEST-VIN' in staging and dev.

### vehicle_delete()

Wrapper to delete a vehicle with the vehicle object.  VIN defaults to 'TEST-VIN' in prod and '$ENVIRONMENT$-TEST-VIN' in staging and dev.

## arcimoto.user

The `user` namespace provides user and permission controls common to all lambdas.

### @require(permission)

Using the `@require(permission)` decorator on a function will automatically assert that the current user has the specified permission before executing the function. This decorator can be stacked multiple times if more than one permission is required.

```python
@arcimoto.user.require('permission.to.check')
@arcimoto.user.require('other.required.permission')
def arbitrary_function():
    pass
```

**NOTE:** This decorator **must** be specified **after** the `@arcimoto.runtime.handler` in execution order to perform context discovery prior to the permission check. It may be used on the primary entry point designated by `@arcimoto.runtime.handler` or another function to permission restrict that specific function.

```python
@arcimoto.runtime.handler
@arcimoto.user.require('permission.to.check')
def main_entry_point(argument):
    pass
```

```python
@arcimoto.runtime.handler
def main_entry_point(argument):
    function_that_needs_higher_permission_level(argument)
    pass
@arcimoto.user.require('permission.to.check')
def function_that_needs_higher_permission_level(argument)
    pass
```

### current()

The global `current()` function will return the current user as best understood by the runtime context. A `User` object will always be returned, but if the runtime was unable to determine which trusted user is currently invoking the function, the user object returned will represent an anonymous user with no permissions.

```python
user = arcimoto.user.current()
logger.debug("Current user is: {}".format(user.username))
```

### User

On initialization, the User object will always represent an anonymous user. Calling `set_username(username)` will cause a DB read in order to load the specified user information, including profile details, groups and permissions. Any error during lookup will result in the user remaining anonymous.

#### username

The `username` property is either the current username if authenticated or `None` if anonymous.

#### authenticated

The `authenticated` property reflects whether the user is currently anonymous or was successfully fetched from the DB.

#### assert_permission(permission_name, message="Unauthorized")

The primary means of authorization and access control is to assert that the current user has the required permission through group membership and to raise an `ArcimotoPermissionError` if the permission isn't present. If provided in the optional `message` argument, the message property of the raised exception is set, otherwise the default exception messag of "Unathorized" is used.

```python
try:
    arcimoto.users.current().assert_permission("required.permission")
except ArcimotoPermissionError as e:
    logger.debug("User '{}' disallowed".format(arcimoto.users.current().username))
```

#### has_permission(permission_name)

If you need to check for a permission without raising an error if it's not present, you can use `has_permission()`.

```python
if not arcimoto.users.current().has_permission("required.permission"):
    logger.debug("That user isn't allowed to do that")
```

#### has_permissions(permission_list)

The `has_permissions()` method allows you to check for the presence of multiple permissions in a single call:

```python
required_list = ["required.permission.1", "required_permission.2"]
if not arcimoto.users.current().has_permissions(required_list):
    logger.debug("That user didn't meet all the requirements")
```
