import logging
import uuid

import arcimoto.vehicle
import arcimoto.runtime

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def handle_test_result(result):
    global logger
    output = {
        'message': '1 test run' if result.testsRun == 1 else f'{result.testsRun} tests run',
        'status': None
    }

    if len(result.skipped) > 0:
        output['issues'] = process_result_type(result.skipped, 'skipped')

    if result.wasSuccessful():
        output['status'] = 'SUCCESS'

    else:
        output['status'] = 'TEST SUITE FAILURE'
        output['issues'] = {
            **process_result_type(result.errors, 'error'),
            **process_result_type(result.failures, 'failure')
        }

    return output


def process_result_type(result_type, result_type_name):
    output = {}
    for test, stack_trace in result_type:
        if test.id().startswith('setUp') or test.id().startswith('tearDown'):
            test_name = test.id().split('(')[0].strip()
        else:
            test_name = test.id().split('.')[-1]
        output[test_name] = {
            'status': 'failure',
            'message': stack_trace.splitlines()[-1],
            'type': result_type_name
        }

    return output


def test_vin_get():
    env = arcimoto.runtime.get_env()
    if env is not arcimoto.runtime.ENV_PROD:
        return env.upper() + '-TEST-VIN'
    return 'TEST-VIN'


def unit_test_user_get_username(admin=False):
    if not admin:
        return '87136858-81a4-4330-802d-b68568acef34'
    return '47a728a9-db7c-4294-9ad2-87d293135025'


def uuid_vin_get():
    vin = ''
    env = arcimoto.runtime.get_env()
    if env is not arcimoto.runtime.ENV_PROD:
        vin += env.upper() + '-'
    vin += 'TEST-VIN' + '-' + uuid.uuid4().hex
    return vin


def vehicle_create(vin, model_release_id=1, **kwargs):
    # mute is used during tests
    mute = kwargs.get('mute', False)

    vehicle = arcimoto.vehicle.Vehicle(vin, mute=mute)
    vehicle.create(model_release_id, mute=mute)
    return vin


def vehicle_delete(vin=None, **kwargs):
    # mute is used during tests
    mute = kwargs.get('mute', False)

    if vin is None:
        vin = test_vin_get()
    vehicle = arcimoto.vehicle.Vehicle(vin, mute=mute)
    vehicle.delete(mute=mute)
