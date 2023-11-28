import cerberus

from arcimoto.exceptions import ArcimotoArgumentError


_validator = None


def _create_validator(schema):
    global _validator

    if schema is None:
        schema = {}

    _validator = cerberus.Validator(schema)
    _validator.purge_unknown = True


def register(schema):
    '''Register lambda input arguments schema to be evaluated by cerberus'''

    try:
        _create_validator(schema)
    except cerberus.schema.SchemaError as e:
        raise ArcimotoArgumentError(f'Invalid argument definition: {e}', data=e) from e


def validate(args):
    global _validator

    try:
        # If no schema has been registered, we don't validate
        if _validator is None:
            _create_validator({})

        if not _validator.validate(args):
            raise ArcimotoArgumentError('Input validation failed', data=_validator.errors)

        return _validator.normalized(args)
    except cerberus.validator.DocumentError as e:
        raise ArcimotoArgumentError('Invalid arguments') from e


def arg_string_empty_string_to_null(v):
    value = v.lower()
    if value in ('', 'none'):
        return None
    return v


def arg_integer_empty_string_to_null(v):
    value = v.lower()
    if value in ('', 'none'):
        return None
    return int(v)


def arg_boolean_empty_string_to_null(v):
    value = v.lower()
    if value in ('', 'none'):
        return None
    if value == 'false':
        return False
    else:
        return True
