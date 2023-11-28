import boto3
import logging
import json

import arcimoto.runtime
from arcimoto.exceptions import ArcimotoException

from arcimoto_aws_services.aws_service import DEFAULT_AWS_REGION

SEVERITY_CRITICAL = 'CRITICAL'
SEVERITY_ERROR = 'ERROR'
SEVERITY_WARNING = 'WARNING'
SEVERITY_INFO = 'INFO'


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


_QUEUES = {
    'prod': 'arcimoto_notifications',
    'staging': 'arcimoto_notifications_staging',
    'dev': 'arcimoto_notifications_dev'
}

_DEFAULT_SEVERITY = SEVERITY_INFO
_DEFAULT_SOURCE_TYPE = 'lambda'
_NOTE_SOURCE_TYPE = 'note'
_DEFAULT_SOURCE = 'Arcimoto'


##############
#  Messages  #
##############


class Message:
    '''This is a base class and is not intended to be instantiated directly'''

    def __init__(self, message, source_type, severity, source, data, channel=None):
        self.message = message
        self.source_type = source_type
        self.source = source
        self.severity = severity
        self.data = data
        self.channel = channel

    def _post_message(self):
        try:
            sqs = boto3.resource('sqs', region_name=DEFAULT_AWS_REGION)
            queue_name = _QUEUES.get(arcimoto.runtime.get_env(), arcimoto.runtime.ENV_DEV)
            queue = sqs.get_queue_by_name(QueueName=queue_name)
            payload = {
                'severity': self.severity,
                'message': self.message,
                'source_type': self.source_type,
                'source': self.source,
                'data': self.data,
                'channel': self.channel
            }
            queue.send_message(MessageBody=json.dumps(payload))

        except Exception as e:
            raise ArcimotoException('Failed to post Message: {}'.format(e)) from e


#################
# Notifications #
#################
class Notification(Message):
    ''' NOTE: the init arguments are in a different order than the Message Class this inherits from '''
    def __init__(self, message, source_type=_DEFAULT_SOURCE_TYPE, source=None, severity=_DEFAULT_SEVERITY, data={}, channel='lambda'):
        super().__init__(message, source_type, severity, source, data, channel)
        self.send_notification()

    def send_notification(self):
        '''Send notifications on events'''
        if self.source is None:
            self.source = 'UNKNOWN'
        self._post_message()


class FirmwareNotification(Notification):
    def __init__(self, message, source_type=_DEFAULT_SOURCE_TYPE, source=None, severity=_DEFAULT_SEVERITY, data={}):
        super().__init__(message, source_type, source, severity, data, 'firmware')


class ManufacturingNotification(Notification):
    def __init__(self, message, source_type=_DEFAULT_SOURCE_TYPE, source=None, severity=_DEFAULT_SEVERITY, data={}):
        super().__init__(message, source_type, source, severity, data, 'manufacturing')


class NetworkNotification(Notification):
    def __init__(self, message, source_type=_DEFAULT_SOURCE_TYPE, source=None, severity=_DEFAULT_SEVERITY, data={}):
        super().__init__(message, source_type, source, severity, data, 'network')


class OrdersNotification(Notification):
    def __init__(self, message, source_type=_DEFAULT_SOURCE_TYPE, source=None, severity=_DEFAULT_SEVERITY, data={}):
        super().__init__(message, source_type, source, severity, data, 'orders')


class REEFNotification(Notification):
    def __init__(self, message, source_type=_DEFAULT_SOURCE_TYPE, source=None, severity=_DEFAULT_SEVERITY, data={}):
        super().__init__(message, source_type, source, severity, data, 'reef')


class ReplicateNotification(Notification):
    def __init__(self, message, source_type=_DEFAULT_SOURCE_TYPE, source=None, severity=_DEFAULT_SEVERITY, data={}):
        super().__init__(message, source_type, source, severity, data, 'replicate')


class ServiceNotification(Notification):
    def __init__(self, message, source_type=_DEFAULT_SOURCE_TYPE, source=None, severity=_DEFAULT_SEVERITY, data={}):
        super().__init__(message, source_type, source, severity, data, 'service')


class TelemetryNotification(Notification):
    def __init__(self, message, source_type=_DEFAULT_SOURCE_TYPE, source=None, severity=_DEFAULT_SEVERITY, data={}):
        super().__init__(message, source_type, source, severity, data, 'telemetry')


class YRiskNotification(Notification):
    def __init__(self, message, source_type=_DEFAULT_SOURCE_TYPE, source=None, severity=_DEFAULT_SEVERITY, data={}):
        super().__init__(message, source_type, source, severity, data, 'yrisk')


##############
#    Notes   #
##############
class Note(Message):
    def __init__(self, object_type, object_id, message, tags=[], source_type=_NOTE_SOURCE_TYPE, source=_DEFAULT_SOURCE, severity=_DEFAULT_SEVERITY, data={}):
        #  message, source_type, severity, source, data, env
        super().__init__(message, source_type, severity, source, data)
        self.object_type = object_type
        self.object_id = object_id
        self.tags = tags

    def post_note(self):
        self.data = {
            'note': {
                'object_type': self.object_type,
                'object_id': self.object_id,
                'author': self.source,
                'content': self.message,
                'tags': self.tags
            },
            'other_data': self.data
        }
        self._post_message()


class VehicleNote(Note):
    def __init__(self, vin, message, tags=[], source_type=_NOTE_SOURCE_TYPE, source=_DEFAULT_SOURCE, data={}):
        super().__init__('Vehicle', vin, message, tags, source_type, source, severity=_DEFAULT_SEVERITY, data={})
        self.post_note()


class AuthorityNote(Note):
    def __init__(self, authorityId, message, tags=[], source_type=_NOTE_SOURCE_TYPE, source=_DEFAULT_SOURCE, data={}):
        super().__init__('Authority', authorityId, message, tags, source_type, source, severity=_DEFAULT_SEVERITY, data={})
        self.post_note()


class UserNote(Note):
    def __init__(self, userId, message, tags=[], source_type=_NOTE_SOURCE_TYPE, source=_DEFAULT_SOURCE, data={}):
        super().__init__('User', userId, message, tags, source_type, source, severity=_DEFAULT_SEVERITY, data={})
        self.post_note()
