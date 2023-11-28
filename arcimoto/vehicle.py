import logging
import random

from arcimoto.exceptions import (
    ArcimotoArgumentError,
    ArcimotoException,
    ArcimotoNotFoundError
)
import arcimoto.db


ARCIMOTO_GROUP_ID = 1

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Vehicle(object):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    vin = None
    role = None
    conn = None
    mock = False
    mute = False
    _MODEL_RELEASE_ID = None

    reserved_meta_sections = ['vin', 'groups', 'telemetry']
    reserved_group_ids = [ARCIMOTO_GROUP_ID]

    def __init__(self, vin, **kwargs):

        self.vin = vin

        # mock/mute are used during tests
        self.mock = kwargs.get('mock', False)
        self.mute = kwargs.get('mute', False)

    @arcimoto.db.transaction
    def add_to_group(self, group_id, **kwargs):
        """
        Adds the vehicle to the specified group
        kwargs:mute is used via the @transaction decorator for tests
        """

        query = self._query_vehicle_group_id_add_vin
        if self.mock:
            return query

        if not self.exists:
            raise ArcimotoNotFoundError(f'Vehicle {self.vin} does not exist')

        self._vehicle_group_exists(group_id)

        cursor = arcimoto.db.get_cursor()
        cursor.execute(query, [self.vin, group_id])
        cursor.close()

    @property
    def allows_governor(self):
        '''
        Checks for the vehicle firmware for the Comm module being up to date enough to allow governor
        '''

        query = self._query_firmware_version_for_vin_allows_governor

        if self.mock:
            return query

        cursor = arcimoto.db.get_cursor()
        cursor.execute(query, [self.vin])
        result = cursor.fetchone()
        cursor.close()

        return (result is not None)

    @arcimoto.db.transaction
    def create(self, model_release_id, **kwargs):
        """
        Creates a basic vehicle in the telemetry system
        kwargs:mute is used in the @transaction decorator if available
        """

        self._MODEL_RELEASE_ID = model_release_id
        query = self._query_vehicle_create

        if self.mock:
            return query

        cursor = arcimoto.db.get_cursor()
        cursor.execute(query, [self.vin, self.MODEL_RELEASE_ID])
        cursor.close()

    @arcimoto.db.transaction
    def delete(self, **kwargs):
        """
        Deletes the vehicle from the telemetry system
        kwargs:mute is used in the @transaction decorator if available
        """

        if self.mock:
            return

        if not self.exists:
            raise ArcimotoNotFoundError(f'Vehicle {self.vin} does not exist')

        cursor = arcimoto.db.get_cursor()
        # This manually deletes relevant but non-referenced table data.
        # Make sure to set any actual references as `ON CASCADE DELETE` in their creation schema
        cursor.execute("DELETE FROM vehicle_join_vehicle_group WHERE vin=%s", [self.vin])
        cursor.execute("DELETE FROM telemetry_points WHERE vin=%s", [self.vin])
        cursor.execute("DELETE FROM vehicle_meta WHERE vin=%s", [self.vin])
        cursor.execute("DELETE FROM vehicle WHERE vin=%s", [self.vin])
        cursor.close()

    @property
    def exists(self):
        """
        Checks for the existance of the vehicle
        """

        query = self._query_vehicle_exists
        if self.mock:
            return query

        cursor = arcimoto.db.get_cursor()
        cursor.execute(query, [self.vin])
        result = cursor.fetchone()
        cursor.close()

        return (result is not None)

    def get(self):
        """
        Collects all vehicle properties and meta values into a dictionary
        """

        if self.mock:
            return

        if not self.exists:
            raise ArcimotoNotFoundError(f"Vehicle {self.vin} does not exist")

        cursor = arcimoto.db.get_cursor()

        vehicle = {
            'vin': self.vin,
            'allows_governor': self.allows_governor,
            'model_release_id': self.MODEL_RELEASE_ID,
            'groups': list(self.groups),
            'telemetry': self.telemetry_points,
            'managed_session': {
                'enabled': self.managed_session_mode
            }
        }

        if self.managed_session_mode:
            vehicle['managed_session']['active_session'] = self.managed_session_current

        # old data from vehicle_meta, exclusing firmware_versions section
        cursor.execute(self._query_vehicle_meta, [self.vin])
        for row in cursor:
            if row['section'] != 'firmware_versions':
                if vehicle.get(row['section'], None) is None:
                    vehicle[row['section']] = {}
                vehicle[row['section']][row['key']] = row['value']

        # new data from vehicle_release schema
        # firmware
        firmware = []
        cursor.execute(self._query_vehicle_firmware_installed, [self.vin])
        for record in cursor.fetchall():
            item = {
                'part_type': record['part_type'],
                'firmware_component': record['firmware_component'],
                'firmware_release_id': record['firmware_release_id'],
                'installed': arcimoto.db.datetime_record_output(record['installed']),
                'hash': record['hash']
            }
            firmware.append(item)

        vehicle['firmware_versions'] = {}
        for firmware_item in firmware:
            vehicle['firmware_versions'][firmware_item['firmware_component']] = firmware_item['hash']
        # parts
        parts = []
        cursor.execute(self._query_vehicle_parts_installed, [self.vin])
        for record in cursor.fetchall():
            item = {
                'part_type': record['part_type'],
                'part_number': record['part_number'],
                'installed': arcimoto.db.datetime_record_output(record['installed'])
            }
            parts.append(item)

        vehicle['parts'] = []
        for part in parts:
            vehicle['parts'].append(part)

        # model info
        cursor.execute(self._query_vehicle_model_name, [self.vin])
        result = cursor.fetchone()
        if result is not None:
            vehicle['model'] = result.get('model_name', None)

        cursor.close()

        return vehicle

    def get_meta(self, section, key):
        """
        Fetches an entry from the vehicle_meta table
        """

        if self.mock:
            return

        cursor = arcimoto.db.get_cursor()

        cursor.execute(self._query_vehicle_meta_entry, [self.vin, section, key])
        meta = cursor.fetchone()
        value = None
        if meta is not None:
            value = meta['value']

        cursor.close()
        return value

    # set up method that allows kwargs for `groups` property
    @arcimoto.db.transaction
    def _groups(self, **kwargs):
        """
        Returns a set of groups to which this vehicle belongs
        kwargs:mute is used in the @transaction decorator if available
        """

        groups = set()
        if self.mock:
            return groups

        cursor = arcimoto.db.get_cursor()
        cursor.execute(self._query_vehicle_groups, [self.vin])
        for row in cursor:
            groups.add(row['group_id'])

        cursor.close()
        return groups

    # declare `groups` property manually to allow input param kwargs for mute to pass to transaction decorator
    groups = property(_groups)

    @property
    def managed_session_current(self):
        """
        Gets active managed session or False if not in active managed session
        """

        if self.mock:
            return False

        managed_session_type = 'arcimoto'
        cursor = arcimoto.db.get_cursor()
        # first check in arcimoto managed sessions
        cursor.execute(self._query_vehicle_managed_session_current, [self.vin])
        result = cursor.fetchone()
        # check in reef managed sessions if not in arcimoto
        if result is None:
            managed_session_type = 'reef'
            cursor.execute(self._query_vehicle_managed_session_reef_current, [self.vin])
            result = cursor.fetchone()

        cursor.close()

        if result is None:
            return False

        return {
            'id': result['id'],
            'pin': result['pin'],
            'initialization': arcimoto.db.datetime_record_output(result['initialization']),
            'completion': arcimoto.db.datetime_record_output(result['completion']) if result['completion'] is not None else None,
            'creator': result.get('creator', None),
            'verification_id': result['verification_id'],
            'type': managed_session_type
        }

    # set up method that allows kwargs for `managed_session_end` property
    @arcimoto.db.transaction
    def managed_session_end(self, **kwargs):
        """
        kwargs:mute is used in the @transaction decorator if available
        """
        if self.mock:
            return {}

        if not self.managed_session_mode:
            raise ArcimotoException(f'Unable to end managed session: {self.vin} is not configured in "Managed Session" mode')

        managed_session_current = self.managed_session_current
        if managed_session_current is False:
            return {}

        managed_session_current_id = managed_session_current.get('id', None)
        if managed_session_current_id is None:
            raise ArcimotoException('Invalid current managed session id')

        cursor = arcimoto.db.get_cursor()
        # end any existing active managed session
        cursor.execute(self._query_vehicle_managed_session_end, [self.vin])
        # get data from current managed session, now that it is ended
        cursor.execute(self._query_vehicle_managed_session_get, [managed_session_current_id])
        result = cursor.fetchone()
        cursor.close()

        if result is None:
            return {}

        initialization = result.get('initialization', None)
        completion = result.get('completion', None)

        return {
            'id': managed_session_current_id,
            'vin': result.get('vin', None),
            'initialization': arcimoto.db.datetime_record_output(initialization) if initialization is not None else None,
            'completion': arcimoto.db.datetime_record_output(completion) if completion is not None else None,
            'creator': result.get('creator', None)
        }

    @property
    def managed_session_mode(self):
        """
        Checks if the vehicle is in managed session mode
        """

        if self.mock:
            return False

        cursor = arcimoto.db.get_cursor()
        cursor.execute(self._query_vehicle_managed_session_mode, [self.vin])
        result = cursor.fetchone()
        cursor.close()

        return (result is not None)

    @arcimoto.db.transaction
    def managed_session_start(self, username, verification_id, pin, **kwargs):
        """
        kwargs:mute is used in the @transaction decorator if available
        """
        if self.mock:
            return

        if not self.managed_session_mode:
            raise ArcimotoException(f"Unable to start managed session: {self.vin} is not configured in 'Managed Session' mode")

        # assure only a single active managed session by closing any before opening
        self.managed_session_end()

        # generate pin if not supplied in input
        if pin is None:
            pin = self.pin_generate()

        # start new active managed session
        try:
            cursor = arcimoto.db.get_cursor()
            cursor.execute(self._query_vehicle_managed_session_start, [self.vin, pin, username, verification_id])
            result = cursor.fetchone()
            cursor.close()

            no_results_error_msg = 'Unable to continue: SQL Result Error: No data returned from managed session start query'

            if result is None:
                raise ArcimotoException(no_results_error_msg)

            id = result.get('id', None)
            if id is None:
                raise ArcimotoException(no_results_error_msg)

            initialization = result.get('initialization', None)
        except Exception as e:
            raise ArcimotoException(e) from e

        return {
            'id': id,
            'pin': pin,
            'initialization': arcimoto.db.datetime_record_output(initialization) if initialization is not None else None
        }

    @property
    def MODEL_RELEASE_ID(self):
        if self.mock:
            return

        if self._MODEL_RELEASE_ID is None:
            self.vehicle_model_release_get()

        return self._MODEL_RELEASE_ID

    def pin_generate(self):
        '''
        Generates a 6 digit pin, using recursive algorythm to reject bad/easy pins
        '''

        # generate 6 digit PIN
        pin = str(random.randint(1, 1000000)).zfill(6)
        # 'bad pins' to reject
        disallowed_pins = [
            '000000',
            '111111',
            '222222',
            '333333',
            '444444',
            '555555',
            '666666',
            '777777',
            '888888',
            '999999',
            '012345',
            '123456',
            '234567',
            '345678',
            '456789',
            '567890',
            '098765',
            '987654',
            '876543',
            '765432',
            '654321',
            '543210'
        ]
        # recursive to generate a pin until you get one that is allowed
        if pin in disallowed_pins:
            self.pin_generate()

        return pin

    # set up method that allows kwargs for `record_gps` property
    @arcimoto.db.transaction
    def _record_gps_get(self, **kwargs):
        """
        Returns the current value of the GPS privacy setting
        kwargs:mute is used in the @transaction decorator if available
        """

        if self.mock:
            return

        if not self.exists:
            raise ArcimotoNotFoundError(f'Attempted to get record_gps property but vin {self.vin} does not exist')

        return (self.get_meta('privacy', 'record_gps') == 'true')

    # set up method that allows kwargs for `record_gps` setter
    @arcimoto.db.transaction
    def _record_gps_set(self, gps_privacy, **kwargs):
        """
        Sets the GPS privacy setting
        kwargs:mute is used in the @transaction decorator if available
        """

        if self.mock:
            return

        if not self.exists:
            raise ArcimotoNotFoundError(f'Vehicle {self.vin} does not exist')

        self.update_meta('privacy', 'record_gps', gps_privacy)

    # declare `record_gps` property manually to allow input param kwargs for mute to pass to transaction decorator
    record_gps = property(_record_gps_get, _record_gps_set)

    @arcimoto.db.transaction
    def reef_managed_session_end(self, **kwargs):
        """
        kwargs:mute is used in the @transaction decorator if available
        """

        if self.mock:
            return {}

        if not self.managed_session_mode:
            raise ArcimotoException(f'Invalid VIN: {self.vin} is not configured in "Managed Session" mode')

        managed_session_current = self.managed_session_current
        if managed_session_current is False:
            return {}

        managed_session_current_id = managed_session_current.get('id', None)
        if managed_session_current_id is None:
            raise ArcimotoException('Invalid managed session id')

        cursor = arcimoto.db.get_cursor()
        # end any existing active managed session(s)
        cursor.execute(self._query_vehicle_managed_session_end_reef, [self.vin])
        # get data from current managed session, now that it is ended
        cursor.execute(self._query_vehicle_managed_session_get_reef, [managed_session_current_id])
        result = cursor.fetchone()
        cursor.close()

        initialization = result.get('initialization', None)
        completion = result.get('completion', None)

        return {
            'id': managed_session_current_id,
            'vin': result.get('vin', None),
            'initialization': arcimoto.db.datetime_record_output(initialization) if initialization is not None else None,
            'completion': arcimoto.db.datetime_record_output(completion) if completion is not None else None,
            'verification_id': result.get('verification_id', None)
        }

    @arcimoto.db.transaction
    def reef_managed_session_start(self, verification_id, **kwargs):
        """
        kwargs:mute is used in the @transaction decorator if available
        """

        if self.mock:
            return

        if not self.managed_session_mode:
            raise ArcimotoException(f'Invalid VIN: {self.vin} is not configured in "Managed Session" mode')
        # assure only a single active managed session by closing any before opening
        self.reef_managed_session_end()

        pin = self.pin_generate()

        try:
            cursor = arcimoto.db.get_cursor()
            # start new active managed session
            cursor.execute(self._query_vehicle_managed_session_start_reef, [self.vin, pin, verification_id])
            result = cursor.fetchone()
            cursor.close()

            id = result.get('id', None)
            initialization = result.get('initialization', None)
            if id is None or initialization is None:
                raise ArcimotoException('Unable to continue - SQL Result Error: No data returned from managed session start query')
        except Exception as e:
            raise ArcimotoException(e)

        return {
            'id': id,
            'pin': pin,
            'initialization': arcimoto.db.datetime_record_output(initialization) if initialization is not None else None
        }

    @arcimoto.db.transaction
    def remove_from_group(self, group_id, **kwargs):
        """
        Removes the vehicle from the specified group
        kwargs:mute is used in the @transaction decorator if available
        """

        if self.mock:
            return

        if not self.exists:
            raise ArcimotoNotFoundError(f'Vehicle {self.vin} does not exist')

        if group_id in self.reserved_group_ids:
            raise ArcimotoArgumentError('Vehicles cannot be removed from reserved groups')

        cursor = arcimoto.db.get_cursor()
        cursor.execute(self._query_vehicle_remove_from_group, [self.vin, group_id])
        cursor.close()

    @arcimoto.db.transaction
    def remove_from_arcimoto_group(self, **kwargs):
        """
        Removes the vehicle from the arcimoto group
        super admin use only, designed for rollback of provisioning
        kwargs:mute is used in the @transaction decorator if available
        """

        if self.mock:
            return

        if not self.exists:
            raise ArcimotoNotFoundError(f'Vehicle {self.vin} does not exist')

        cursor = arcimoto.db.get_cursor()
        cursor.execute(self._query_vehicle_remove_from_group, [self.vin, ARCIMOTO_GROUP_ID])
        cursor.close()

    # set up method that allows kwargs for `telemetry_points` getter
    @arcimoto.db.transaction
    def _telemetry_points_get(self, **kwargs):
        """
        Returns all configured telemetry points for the vehicle
        kwargs:mute is used in the @transaction decorator if available
        """

        if self.mock:
            return {}

        if not self.exists:
            raise ArcimotoNotFoundError(f'Vehicle {self.vin} does not exist')

        cursor = arcimoto.db.get_cursor()

        telemetry_points = {}
        cursor.execute(self._query_vehicle_telemetry_points, [self.vin])
        for row in cursor.fetchall():
            telemetry_points[row['prop']] = {}

        cursor.close()
        return telemetry_points

    # set up method that allows kwargs for `telemetry_points` setter
    @arcimoto.db.transaction
    def _telemetry_points_set(self, telemetry_points, **kwargs):
        """
        Replaces all configured telemetry points for a vehicle with the specified list
        kwargs:mute is used in the @transaction decorator if available
        """

        if self.mock:
            return

        if not self.exists:
            raise ArcimotoNotFoundError(f'Vehicle {self.vin} does not exist')

        cursor = arcimoto.db.get_cursor()
        cursor.execute("DELETE FROM telemetry_points WHERE vin=%s", [self.vin])

        query = (
            'INSERT INTO telemetry_points '
            '(vin, prop, freq) '
            'VALUES (%s, %s, %s)'
        )
        for key, value in telemetry_points.items():
            freq = value.get("frequency", None)
            cursor.execute(query, [self.vin, key, freq])

        cursor.close()
    # declare `telemetry_points` property manually to allow input param kwargs for mute to pass to transaction decorator
    telemetry_points = property(_telemetry_points_get, _telemetry_points_set)

    @arcimoto.db.transaction
    def _telemetry_version_get(self, **kwargs):
        """
        Returns the registered telemetry definition version for the vehicle
        kwargs:mute is used in the @transaction decorator if available
        """

        if self.mock:
            return

        if not self.exists:
            raise ArcimotoNotFoundError(f'Vehicle {self.vin} does not exist')

        return self.get_meta('telemetry_settings', 'version')

    @arcimoto.db.transaction
    def _telemetry_version_set(self, telemetry_version, **kwargs):
        """
        Sets the telemetry definition version for the vehicle
        kwargs:mute is used in the @transaction decorator if available
        """

        if self.mock:
            return

        if not self.exists:
            raise ArcimotoNotFoundError(f'Vehicle {self.vin} does not exist')

        self.update_meta('telemetry_settings', 'version', telemetry_version)
    # declare `telemetry_version` property manually to allow input param kwargs for mute to pass to transaction decorator
    telemetry_version = property(_telemetry_version_get, _telemetry_version_set)

    @arcimoto.db.transaction
    def update_meta(self, section, key, value, **kwargs):
        """
        Upserts an entry in vehicle_meta table, uses (vin, section, key) as primary id
        kwargs:mute is used in the @transaction decorator if available
        """

        # disallow setting any meta data within reserved sections
        if section in self.reserved_meta_sections:
            raise ArcimotoArgumentError(f'Attempt to set meta in reserved section: {section}')

        if self.mock:
            return

        if not self.exists:
            raise ArcimotoNotFoundError(f'Vehicle {self.vin} does not exist')

        cursor = arcimoto.db.get_cursor()
        cursor.execute(self._query_vehicle_update_meta, [self.vin, section, key, value, value])
        cursor.close()

    def validate_access_reef(self):
        if self.mock:
            return

        allowed_vins = []
        cursor = arcimoto.db.get_cursor()

        try:
            cursor.execute(self._query_vehicles_validate_access_reef)
            for record in cursor.fetchall():
                allowed_vins.append(record['vin'])
        except Exception as e:
            logger.error(f'DB error validating VIN: {e}')
        finally:
            cursor.close()

        if self.vin not in allowed_vins:
            return False
        return True

    def validate_user_access(self, username):
        global logger

        if self.mock:
            return

        allowed_vins = []
        cursor = arcimoto.db.get_cursor()

        try:
            cursor.execute(self._query_vehicles_validate_user_access, [username])
            for record in cursor.fetchall():
                allowed_vins.append(record['vin'])
        except Exception as e:
            logger.warning('DB error validating VIN: {}'.format(e))
        finally:
            cursor.close()

        if self.vin not in allowed_vins:
            return False
        return True

    def vehicle_model_release_get(self):
        if self.mock:
            return

        cursor = arcimoto.db.get_cursor()
        cursor.execute(self._query_vehicle_model_release_get, [self.vin])
        result = cursor.fetchone()
        cursor.close()

        self._MODEL_RELEASE_ID = result.get('model_release_id')

        return self._MODEL_RELEASE_ID

    @arcimoto.db.transaction
    def vehicle_model_release_set(self, model_release_id, **kwargs):
        """
        kwargs:mute is used in the @transaction decorator if available
        """

        if self.mock:
            return

        if not self.exists:
            raise ArcimotoNotFoundError(f'Invalid {self.vin}: Vehicle does not exist')

        cursor = arcimoto.db.get_cursor()
        cursor.execute(self._query_vehicle_model_release_set, [model_release_id, self.vin])
        cursor.close()

        self._MODEL_RELEASE_ID = model_release_id

        try:
            msg = f'Model Release set to {model_release_id}'
            arcimoto.note.VehicleNote(
                vin=self.vin,
                message=msg,
                tags=['parts']
            )
        except Exception as e:
            raise ArcimotoException(f'Failure to create vehicle note for {self.vin} - {e}')

    @property
    def _query_firmware_version_for_vin_allows_governor(self):
        '''
        Checks for the vehicle firmware for the Comm module being up to date enough to allow governor
        '2021-01-23 08:31:00' is the timestamp for the commit that allowed the functionality
        c045a84edc60b96989f5bdd36c30d3406b7f4d3f
        '''

        return (
            'SELECT hash FROM firmware_versions '
            "WHERE created >= '2021-01-23 08:31:00' "
            'AND hash = ('
            'SELECT fr.hash '
            'FROM vehicle_firmware_installed AS vfi '
            'JOIN firmware_release as fr ON vfi.firmware_release_id=fr.firmware_release_id '
            'WHERE vfi.vin = %s '
            "AND vfi.firmware_component = 'Comm Firmware'"
            ')'
        )

    @property
    def _query_vehicle_create(self):
        return (
            'INSERT INTO vehicle (vin, model_release_id) '
            'VALUES (%s, %s) '
            'ON CONFLICT (vin) DO UPDATE '
            'SET model_release_id=excluded.model_release_id'
        )

    @property
    def _query_vehicle_exists(self):
        return (
            'SELECT vin '
            'FROM vehicle '
            'WHERE vin=%s'
        )

    @property
    def _query_vehicle_firmware_installed(self):
        return (
            'SELECT vfi.part_type, vfi.firmware_component, vfi.firmware_release_id, vfi.installed, fr.hash '
            'FROM vehicle_firmware_installed AS vfi '
            'JOIN firmware_release as fr ON vfi.firmware_release_id=fr.firmware_release_id '
            'WHERE vfi.vin = %s '
            'ORDER BY vfi.part_type, vfi.firmware_component ASC'
        )

    @property
    def _query_vehicle_group_id_add_vin(self):
        return (
            'INSERT INTO vehicle_join_vehicle_group '
            '(vin, group_id) VALUES (%s, %s) '
            'ON CONFLICT (vin, group_id) DO NOTHING'
        )

    @property
    def _query_vehicle_group_id_exists(self):
        return (
            'SELECT name '
            'FROM vehicle_group '
            'WHERE id=%s'
        )

    @property
    def _query_vehicle_groups(self):
        return (
            'SELECT group_id '
            'FROM vehicle_join_vehicle_group '
            'WHERE vin=%s'
        )

    @property
    def _query_vehicle_managed_session_current(self):
        return (
            'SELECT id, pin, initialization, completion, creator, verification_id '
            'FROM managed_sessions '
            'WHERE vin=%s '
            'AND completion IS NULL'
        )

    @property
    def _query_vehicle_managed_session_end(self):
        return (
            'UPDATE managed_sessions '
            'SET completion = NOW() '
            'WHERE vin=%s '
            'AND completion IS NULL'
        )

    @property
    def _query_vehicle_managed_session_end_reef(self):
        return (
            'UPDATE managed_sessions_reef '
            'SET completion = NOW() '
            'WHERE vin=%s '
            'AND completion IS NULL'
        )

    @property
    def _query_vehicle_managed_session_get(self):
        return (
            'SELECT vin, initialization, completion, creator '
            'FROM managed_sessions '
            'WHERE id=%s '
            'ORDER BY id DESC LIMIT 1'
        )

    @property
    def _query_vehicle_managed_session_get_reef(self):
        return (
            'SELECT vin, initialization, completion, verification_id '
            'FROM managed_sessions_reef '
            'WHERE id=%s '
            'ORDER BY id DESC LIMIT 1'
        )

    @property
    def _query_vehicle_managed_session_mode(self):
        return (
            'SELECT vin '
            'FROM managed_sessions_vehicles '
            'WHERE vin=%s'
        )

    @property
    def _query_vehicle_managed_session_start(self):
        return (
            'INSERT INTO managed_sessions (vin, pin, creator, verification_id) '
            'VALUES (%s, %s, %s, %s) '
            'RETURNING id, initialization'
        )

    @property
    def _query_vehicle_managed_session_start_reef(self):
        return (
            'INSERT INTO managed_sessions_reef (vin, pin, verification_id) '
            'VALUES (%s, %s, %s) '
            'RETURNING id, initialization'
        )

    @property
    def _query_vehicle_managed_session_reef_current(self):
        return (
            'SELECT id, pin, initialization, completion, verification_id '
            'FROM managed_sessions_reef '
            'WHERE vin=%s '
            'AND completion IS NULL'
        )

    @property
    def _query_vehicle_meta(self):
        return (
            'SELECT section, key, value '
            'FROM vehicle_meta '
            'WHERE vin=%s'
        )

    @property
    def _query_vehicle_meta_entry(self):
        return (
            'SELECT value '
            'FROM vehicle_meta '
            'WHERE vin=%s AND section=%s AND key=%s'
        )

    @property
    def _query_vehicle_model_name(self):
        return (
            'SELECT vm.model_name '
            'FROM vehicle_model AS vm '
            'JOIN vehicle_model_release AS vmr ON vmr.model_id = vm.id '
            'JOIN vehicle AS v ON v.model_release_id = vmr.model_release_id '
            'WHERE v.vin = %s'
        )

    @property
    def _query_vehicle_model_release_get(self):
        return (
            'SELECT model_release_id FROM vehicle '
            'WHERE vin = %s'
        )

    @property
    def _query_vehicle_model_release_set(self):
        return (
            'UPDATE vehicle '
            'SET model_release_id = %s '
            'WHERE vin = %s'
        )

    @property
    def _query_vehicle_parts_installed(self):
        return (
            'SELECT part_type, part_number, installed '
            'FROM vehicle_parts_installed '
            'WHERE vin = %s '
            'ORDER BY part_type, part_number ASC'
        )

    @property
    def _query_vehicle_remove_from_group(self):
        return (
            'DELETE FROM vehicle_join_vehicle_group '
            'WHERE vin=%s AND group_id=%s'
        )

    @property
    def _query_vehicle_telemetry_points(self):
        return (
            'SELECT prop, freq '
            'FROM telemetry_points '
            'WHERE vin=%s'
        )

    @property
    def _query_vehicle_update_meta(self):
        return (
            'INSERT INTO vehicle_meta '
            '(vin, section, key, value) '
            'VALUES (%s, %s, %s, %s) '
            'ON CONFLICT (vin, section, key) DO UPDATE '
            'SET value=%s '
            'RETURNING vin, section, key, value'
        )

    @property
    def _query_vehicles_validate_access_reef(self):
        return (
            'SELECT DISTINCT(vjvg.vin) '
            'FROM vehicle_join_vehicle_group AS vjvg '
            'LEFT JOIN vehicle_group vg '
            'ON vg.id=vjvg.group_id '
            "WHERE vg.name = 'REEF'"
        )

    @property
    def _query_vehicles_validate_user_access(self):
        return (
            'SELECT DISTINCT(v.vin) FROM '
            'users_join_vehicle_group AS u '
            'LEFT JOIN vehicle_group vg '
            'ON u.vehicle_group=vg.id '
            'LEFT JOIN vehicle_join_vehicle_group AS v '
            'ON vg.id=v.group_id '
            'WHERE u.username=%s'
        )

    def _vehicle_group_exists(self, group_id):
        cursor = arcimoto.db.get_cursor()
        cursor.execute(self._query_vehicle_group_id_exists, [group_id])
        if cursor.fetchone() == 0:
            raise ArcimotoNotFoundError(f'Group {group_id} does not exist')
        return True
