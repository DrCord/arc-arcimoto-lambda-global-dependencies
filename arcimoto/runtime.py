import functools
import json
import logging


from arcimoto.exceptions import (
    ArcimotoAlertException,
    ArcimotoArgumentError,
    ArcimotoException,
    ArcimotoFirmwareAlertException,
    ArcimotoHighAlertException,
    ArcimotoManufacturingAlertException,
    ArcimotoNetworkAlertException,
    ArcimotoNoStepUnrollException,
    ArcimotoNotFoundError,
    ArcimotoOrdersAlertException,
    ArcimotoPermissionError,
    ArcimotoREEFAlertException,
    ArcimotoReplicateAlertException,
    ArcimotoServiceAlertException,
    ArcimotoTelemetryAlertException,
    ArcimotoYRiskAlertException
)
import arcimoto.note
import arcimoto.args
import arcimoto.user

from arcimoto_aws_services.lambda_service import LambdaService
from arcimoto_aws_services.secretsmanager import SecretsManagerService

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


ENV_DEV = 'dev'
ENV_STAGING = 'staging'
ENV_PROD = 'prod'
AWS_ACCOUNT_ID = '511596272857'


'''
These global variables will persist across lambda container invocations,
but are expected to be set per-invocation by _set_context()
'''
_arn = None
_function_name = __name__
_env = ENV_DEV
_event = None
_role = None


def arn_sections_join(service, resource, region='us-west-2'):
    global AWS_ACCOUNT_ID
    return '{}:{}:{}:{}:{}'.format('arn:aws', service, region, AWS_ACCOUNT_ID, resource)


def boto_lambda_exception_handle(payload):
    exception_type = payload.get('errorType', None)
    error_message = payload.get('errorMessage', None)
    if exception_type == 'ArcimotoAlertException':
        raise ArcimotoAlertException(error_message)
    elif exception_type == 'ArcimotoArgumentError':
        raise ArcimotoArgumentError(error_message)
    elif exception_type == 'ArcimotoHighAlertException':
        raise ArcimotoHighAlertException(error_message)
    elif exception_type == 'ArcimotoNoStepUnrollException':
        raise ArcimotoNoStepUnrollException(error_message)
    elif exception_type == 'ArcimotoNotFoundError':
        raise ArcimotoNotFoundError(error_message)
    elif exception_type == 'ArcimotoPermissionError':
        raise ArcimotoPermissionError(error_message)
    raise ArcimotoException(error_message)


def handler(function):
    '''
    Decorator that will auto-configure the package for lambda execution.
    '''

    @functools.wraps(function)
    def _impl(event, context):
        global _event

        try:
            _set_context(context)
            _event = event

            # the AWS default pass-through API mapping template puts params into 'body-json',
            # add those to the top level of the event itself so everything gets validated
            body_json = event.get('body-json', {})
            for prop in body_json:
                _event[prop] = body_json[prop]

            args = arcimoto.args.validate(_event)
            result = function(**args)

            _event = None
            return result if result is not None else {}

        except ArcimotoFirmwareAlertException as e:
            arcimoto.note.FirmwareNotification(
                message=str(e.message),
                source=get_function_name(),
                data=e.data,
                severity=arcimoto.note.SEVERITY_ERROR
            )
            raise e

        except ArcimotoManufacturingAlertException as e:
            arcimoto.note.ManufacturingNotification(
                message=str(e.message),
                source=get_function_name(),
                data=e.data,
                severity=arcimoto.note.SEVERITY_ERROR
            )
            raise e

        except ArcimotoNetworkAlertException as e:
            arcimoto.note.NetworkNotification(
                message=str(e.message),
                source=get_function_name(),
                data=e.data,
                severity=arcimoto.note.SEVERITY_ERROR
            )
            raise e

        except ArcimotoOrdersAlertException as e:
            arcimoto.note.OrdersNotification(
                message=str(e.message),
                source=get_function_name(),
                data=e.data,
                severity=arcimoto.note.SEVERITY_ERROR
            )
            raise e

        except ArcimotoREEFAlertException as e:
            arcimoto.note.REEFNotification(
                message=str(e.message),
                source=get_function_name(),
                data=e.data,
                severity=arcimoto.note.SEVERITY_ERROR
            )
            raise e

        except ArcimotoReplicateAlertException as e:
            arcimoto.note.ReplicateNotification(
                message=str(e.message),
                source=get_function_name(),
                data=e.data,
                severity=arcimoto.note.SEVERITY_ERROR
            )
            raise e

        except ArcimotoServiceAlertException as e:
            arcimoto.note.ServiceNotification(
                message=str(e.message),
                source=get_function_name(),
                data=e.data,
                severity=arcimoto.note.SEVERITY_ERROR
            )
            raise e

        except ArcimotoTelemetryAlertException as e:
            arcimoto.note.TelemetryNotification(
                message=str(e.message),
                source=get_function_name(),
                data=e.data,
                severity=arcimoto.note.SEVERITY_ERROR
            )
            raise e

        except ArcimotoYRiskAlertException as e:
            arcimoto.note.YRiskNotification(
                message=str(e.message),
                source=get_function_name(),
                data=e.data,
                severity=arcimoto.note.SEVERITY_ERROR
            )
            raise e

        except ArcimotoAlertException as e:
            arcimoto.note.Notification(
                message=str(e.message),
                source=get_function_name(),
                data=e.data,
                severity=arcimoto.note.SEVERITY_ERROR
            )
            raise e

        except ArcimotoHighAlertException as e:
            arcimoto.note.Notification(
                message=e.message,
                source=get_function_name(),
                data=e.data,
                severity=arcimoto.note.SEVERITY_CRITICAL
            )
            raise e

        except ArcimotoArgumentError as e:
            # flatten rich data (message and data) to a string and re-raise
            message = '{} {}'.format(e.message, e.data)
            raise ArcimotoArgumentError(message) from e

    return _impl


def event():
    global _event
    if _event is None:
        raise ArcimotoException('Event access outside of invocation')
    return _event


def get_env():
    global _env
    return _env


def get_function_name():
    global _function_name
    return _function_name


def get_role():
    global _role
    return _role


def get_secret(secret_name):
    SecretsManagerServiceObject = SecretsManagerService()
    return SecretsManagerServiceObject.get_secret(secret_name)


def invoke_lambda(lambda_name, args, **kwargs):
    global logger

    mute = kwargs.get('mute', False)

    if not mute:
        logger.info(f'Invoking lambda {lambda_name} with args: {args}')

    existing_token = args.get('params', {}).get('header', {}).get('Authorization', '')
    if not existing_token:
        incoming_event = event()
        user_token = incoming_event.get('params', {}).get('header', {}).get('Authorization', '')
        if user_token:
            args['params'] = {
                'header': {
                    'Authorization': user_token
                }
            }

    LambdaServiceObject = LambdaService()
    call_result = LambdaServiceObject.client.invoke(
        FunctionName=':'.join([lambda_name, get_env()]),
        InvocationType='RequestResponse',
        Payload=json.dumps(args).encode()
    )

    payload = json.loads(call_result['Payload'].read())

    if 'FunctionError' in call_result:
        exception_type = payload.get('errorType', None)
        error_message = str(payload['errorMessage'])
        if exception_type == 'ArcimotoAlertException':
            raise ArcimotoAlertException(error_message)
        elif exception_type == 'ArcimotoFirmwareAlertException':
            raise ArcimotoFirmwareAlertException(error_message)
        elif exception_type == 'ArcimotoManufacturingAlertException':
            raise ArcimotoManufacturingAlertException(error_message)
        elif exception_type == 'ArcimotoNetworkAlertException':
            raise ArcimotoNetworkAlertException(error_message)
        elif exception_type == 'ArcimotoOrdersAlertException':
            raise ArcimotoOrdersAlertException(error_message)
        elif exception_type == 'ArcimotoREEFAlertException':
            raise ArcimotoREEFAlertException(error_message)
        elif exception_type == 'ArcimotoReplicateAlertException':
            raise ArcimotoReplicateAlertException(error_message)
        elif exception_type == 'ArcimotoServiceAlertException':
            raise ArcimotoServiceAlertException(error_message)
        elif exception_type == 'ArcimotoTelemetryAlertException':
            raise ArcimotoTelemetryAlertException(error_message)
        elif exception_type == 'ArcimotoYRiskAlertException':
            raise ArcimotoYRiskAlertException(error_message)
        elif exception_type == 'ArcimotoArgumentError':
            raise ArcimotoArgumentError(error_message)
        elif exception_type == 'ArcimotoHighAlertException':
            raise ArcimotoHighAlertException(error_message)
        elif exception_type == 'ArcimotoNoStepUnrollException':
            raise ArcimotoNoStepUnrollException(error_message)
        elif exception_type == 'ArcimotoNotFoundError':
            raise ArcimotoNotFoundError(error_message)
        elif exception_type == 'ArcimotoPermissionError':
            raise ArcimotoPermissionError(error_message)
        raise ArcimotoException(error_message)

    return payload


def _role_lookup(arn):
    try:
        LambdaServiceObject = LambdaService()

        response = LambdaServiceObject.client.get_function_configuration(
            FunctionName=arn
        )
        role_arn = response.get('Role', None)

        if role_arn is None:
            raise ArcimotoException('No role specified')

        (preamble, role) = role_arn.split('/')
        return role

    except Exception as e:
        raise ArcimotoException('Failed to fetch execution role: {}'.format(e)) from e


def _set_context(context):
    global _arn, _function_name, _role, _env

    try:
        _arn = context.invoked_function_arn
        _function_name = context.function_name
        if _role is None:
            _set_role(_role_lookup(_arn))

        if _arn.endswith(':staging'):
            _env = ENV_STAGING
        elif _arn.endswith(':prod'):
            _env = ENV_PROD
        else:
            _env = ENV_DEV

    except Exception as e:
        raise ArcimotoException(f'Invalid context provided to Arcimoto runtime: {e}') from e


def _set_role(role):
    global _role

    _role = role


def test_invoke_lambda(lambda_name, args, test_runner_user_admin=True):
    unittest_user_tokens = arcimoto.runtime.get_secret('unittest.users.tokens')
    USER_TOKEN_ADMIN = unittest_user_tokens.get('USER_TOKEN_ADMIN', '')
    USER_TOKEN_NON_ADMIN = unittest_user_tokens.get('USER_TOKEN_NON_ADMIN', '')

    payload = args
    payload['params'] = payload.get('params', {})
    payload['params']['header'] = {
        'Authorization': USER_TOKEN_ADMIN
    }
    if not test_runner_user_admin:
        payload['params']['header']['Authorization'] = USER_TOKEN_NON_ADMIN

    return invoke_lambda(lambda_name, payload, mute=True)
