import logging
import base64
import json
import functools

import arcimoto.db
from arcimoto.exceptions import (
    ArcimotoException,
    ArcimotoPermissionError
)
import arcimoto.user


_current = None
_AUTHENTICATION_ROLE = "global.authentication"

USER_POOL_ID = "us-west-2_3x5jXoVFD"


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def authenticated_cursor_request(cursor=None, mock=False):
    '''
        returns a tuple containing an authenticated cursor
        and whether you need to close it at the end of the function

        if mock=True arcimoto.db.get_cursor will return the connection
        string instead of an active connection cursor
    '''
    if cursor is None:
        cursor_close = True
        cursor = arcimoto.db.get_cursor(_AUTHENTICATION_ROLE, mock)
    else:
        cursor_close = False

    return (cursor, cursor_close)


def current(**kwargs):
    '''
        Reads the Authorization token from the event and sets CurrentUser

        NOTE: This implicitly trusts that the Authorization token presented
        is valid. Calls that pass through API Gateway will ensure that this is
        true, but this won't be true for any other invocation method.

        returns the current user object so you can chain
    '''

    global _current

    # mock is used during tests
    mock = kwargs.get('mock', False)

    if _current is None:
        _current = User()

    username = None

    # unpack the email address from the JWT token in event
    event = arcimoto.runtime.event()
    token = event.get('params', {}).get('header', {}).get('Authorization', '')
    if token != '':
        try:
            (headers, claims, sig) = token.split('.')
            token_string = base64.urlsafe_b64decode(claims + '==')
            token_data = json.loads(token_string)
            username = token_data.get('sub', None)
        except Exception as e:
            # any failures leaves the username as None (aka, anonymous) and are allowed
            logger.warning(f'Failed to unpack JWT token: {e}')

    _current.respawn(username, mock)

    return _current


def require(permission):

    def _wrap(function):

        @functools.wraps(function)
        def _impl(*args, **kwargs):
            # kwargs:mute, mock are used during tests
            current(
                mock=kwargs.get('mock', False)
            ).assert_permission(
                permission,
                mute=kwargs.get('mute', False)
            )
            return function(*args, **kwargs)

        return _impl

    return _wrap


class User:

    def __init__(self, username=None, **kwargs):
        self.reset()

        # mock is used during tests
        mock = kwargs.get('mock', False)

        if username is not None:
            self.respawn(username, mock)

    @property
    def authenticated(self):
        return self.username is not None

    def assert_permission(self, permission, message='Unauthorized', **kwargs):
        # kwargs:mute=True is used during unit tests
        mute = kwargs.get('mute', False)

        if not self.has_permission(permission):
            if not mute:
                logger.warning(f'assert_permission failure - permission: {permission} for username {self.username}')
            raise ArcimotoPermissionError(message)
        return True

    @property
    def exists(self):
        return self.has_profile

    def is_user_profile(self):
        return self.has_profile

    def get_abilities(self, **kwargs):
        # mock is used during tests
        mock = kwargs.get('mock', False)

        if not len(self.abilities):
            self.set_abilities(mock=mock)
        return self.abilities

    def get_groups(self, **kwargs):
        # mock is used during tests
        mock = kwargs.get('mock', False)

        if not len(self.groups):
            self.set_permission_groups(mock=mock)
        return self.groups

    def get_preferences(self, **kwargs):
        # mock is used during tests
        mock = kwargs.get('mock', False)

        if not len(self.preferences):
            self.set_preferences(mock=mock)
        return self.preferences

    def get_profile(self):
        return self.profile

    def get_roles(self):
        return self.roles

    def get_username(self):
        return self.username

    def has_permission(self, permission):
        return self.has_permissions([permission])

    def has_permissions(self, permissions):
        '''
            Determines if a user has all requested roles
        '''
        for permission in permissions:
            if self.roles.get(permission, None) is None:
                return False
        return True

    def reset(self):
        self.username = None
        self.has_profile = False
        self.profile = {
            'email': None,
            'phone': None,
            'display_name': None,
            'avatar': None,
            'avatar_file_type': None
        }
        self.groups = []
        self.roles = {}
        self.preferences = []
        self.abilities = []

    def respawn(self, username, mock=False):
        '''
            resets user and gets minimum data for user object to work
            for has_profile and permission checks
        '''
        cursor = None

        if not mock:
            self.reset()
        self.set_username(username)

        # don't fetch any user data if we're anonymous or mock=True
        if self.username is None or mock:
            return

        try:
            cursor = arcimoto.db.get_cursor(_AUTHENTICATION_ROLE)

            logger.debug(f'Caching configuration for {self.username}')

            self.set_profile(cursor)
            self.set_permissions(cursor)

        except Exception as e:
            raise ArcimotoException(str(e)) from e

        finally:
            # explicitly close the auth connection
            arcimoto.db.close(_AUTHENTICATION_ROLE)

    def set_abilities(self, **kwargs):
        '''
           Compares all system abilities to user permissions to assign user abilities
        '''

        # mock is used during tests
        mock = kwargs.get('mock', False)

        # don't fetch any user data if we're anonymous
        if self.username is None:
            return
        # no abilities if no roles
        if not len(self.roles):
            return

        # get all abilities in system with associated permissions
        user_abilities_object = arcimoto.user.Abilities(mock=mock)
        system_abilities = user_abilities_object.abilities

        # compare with user permissions and assign abilities to self.abilities
        # check which abilities user has based on self.roles
        # naively loop through all system abilities and check for the permissions associated
        for system_ability in system_abilities:
            user_permissions_applicable_for_ability = []
            # check for all permissions ability requires
            for system_ability_permission in system_ability['permissions']:
                # loop over user permissions
                for user_permission, user_permission_resources in self.roles.items():
                    # check if user has permission
                    if user_permission == system_ability_permission['permission']:
                        # check resource match
                        if '*' in user_permission_resources or system_ability_permission['resource'] in user_permission_resources:
                            user_permissions_applicable_for_ability.append(user_permission)
                            break

            if len(user_permissions_applicable_for_ability) == len(system_ability['permissions']):
                self._user_add_ability(system_ability)

    def set_permission_groups(self, cursor=None, **kwargs):
        global logger

        # mock is used during tests
        mock = kwargs.get('mock', False)

        # permission groups
        query = self._query_permission_groups_for_username()
        if mock:
            return query

        try:
            (cursor, cursor_close) = authenticated_cursor_request(cursor)

            cursor.execute(query, [self.username])
            self.groups = []
            for record in cursor.fetchall():
                self.groups.append(record['name'])

        except Exception as e:
            raise ArcimotoException(str(e)) from e

        finally:
            # explicitly close the auth connection if it was created for this function
            if cursor_close:
                arcimoto.db.close(_AUTHENTICATION_ROLE)

    def set_permissions(self, cursor=None, **kwargs):
        global logger

        # mock is used during tests
        mock = kwargs.get('mock', False)

        query = self._query_permissions_for_username()
        if mock:
            return query

        try:
            (cursor, cursor_close) = authenticated_cursor_request(cursor)

            # permissions
            cursor.execute(query, [self.username])
            for record in cursor.fetchall():
                resources = self.roles.get(record['permission'], [])
                resources.append(record['resource'])
                self.roles[record['permission']] = resources

        except Exception as e:
            raise ArcimotoException(str(e)) from e

        finally:
            # explicitly close the auth connection if it was created for this function
            if cursor_close:
                arcimoto.db.close(_AUTHENTICATION_ROLE)

    def set_preferences(self, cursor=None, **kwargs):
        # mock is used during tests
        mock = kwargs.get('mock', False)

        query = self._query_preferences_for_username()
        if mock:
            return query

        if self.authenticated:
            if cursor is None:
                cursor = arcimoto.db.get_cursor(_AUTHENTICATION_ROLE)

            try:
                cursor.execute(query, [self.username])
                self.preferences = []
                for row in cursor:
                    prefs_record = {
                        'preference': row['preference'],
                        'value': row['value'],
                        'description': row['description']
                    }
                    self.preferences.append(prefs_record)

            except Exception as e:
                raise ArcimotoException(str(e)) from e

            finally:
                # explicitly close the auth connection
                arcimoto.db.close(_AUTHENTICATION_ROLE)
        else:
            self.preferences = []

    def set_profile(self, cursor=None, **kwargs):
        global logger

        # mock is used during tests
        mock = kwargs.get('mock', False)

        query = self._query_profile_for_username()
        if mock:
            return query

        try:
            (cursor, cursor_close) = authenticated_cursor_request(cursor)

            cursor.execute(query, [self.username])
            user_profile = cursor.fetchone()
            if user_profile is not None:
                self.has_profile = True
                self.profile['email'] = user_profile.get('email', None)
                self.profile['phone'] = user_profile.get('phone', None)
                self.profile['display_name'] = user_profile.get('display_name', None)

                avatar_bytes = user_profile.get('avatar', None)
                if avatar_bytes is not None:
                    self.profile['avatar'] = base64.b64encode(avatar_bytes).decode('utf-8')
                    self.profile['avatar_file_type'] = user_profile.get('avatar_file_type', None)
                else:
                    self.profile['avatar'] = None
                    self.profile['avatar_file_type'] = None

        except Exception as e:
            raise ArcimotoException(str(e)) from e

        finally:
            # explicitly close the auth connection if it was created for this function
            if cursor_close:
                arcimoto.db.close(_AUTHENTICATION_ROLE)

    def set_username(self, username):
        self.username = username

    def _query_permission_groups_for_username(self):
        query = (
            'SELECT '
            'name '
            'FROM user_group '
            'INNER JOIN user_group_join '
            'ON user_group.id=user_group_join.group_id '
            'WHERE user_group_join.username=%s'
        )
        return query

    def _query_permissions_for_username(self):
        query = (
            'SELECT '
            'p.permission as permission, '
            'p.resource as resource '
            'FROM user_permission as p '
            'LEFT JOIN user_permission_group_join as pg ON '
            'p.permission = pg.permission '
            'LEFT JOIN user_group as g ON '
            'pg.group_id = g.id '
            'LEFT JOIN user_group_join as ug ON '
            'g.id = ug.group_id '
            'WHERE ug.username = %s'
        )
        return query

    def _query_preferences_for_username(self):
        query = (
            'SELECT pj.preference as preference, '
            'pj.value as value, '
            'p.description as description FROM '
            'user_profile_join_user_preferences as pj '
            'LEFT JOIN user_preferences as p ON pj.preference=p.preference '
            'WHERE pj.username=%s'
        )
        return query

    def _query_profile_for_username(self):
        query = (
            'SELECT username, email, phone, display_name, avatar, avatar_file_type '
            'FROM user_profile '
            'WHERE username=%s'
        )
        return query

    def _user_add_ability(self, system_ability):
        self.abilities.append(
            {
                'id': system_ability['id'],
                'ability': system_ability['ability'],
                'constant': system_ability['constant']
            }
        )


class Abilities:
    # Context: system user abilities, not abilities of a specific user

    _abilities = []

    def __init__(self, **kwargs):
        # kwargs:mock=True used in tests
        mock = kwargs.get('mock', False)

        self.reset()
        self.list(mock)

    @property
    def abilities(self):
        return self._abilities

    @abilities.setter
    def abilities(self, value):
        self._abilities = value

    def get_abilities(self):
        return self.abilities

    def list(self, mock=False):
        # get all abilities in system and related permissions/resources
        global logger

        abilities = []
        query = self._query_abilities_list()
        if mock:
            return query

        try:
            cursor = arcimoto.db.get_cursor(_AUTHENTICATION_ROLE)
            cursor.execute(query)
            for record in cursor:
                ability_id = record['id']
                ability_index = next((i for i, item in enumerate(abilities) if item['id'] == ability_id), None)
                if ability_index is not None:
                    abilities[ability_index]['permissions'].append(
                        {
                            'permission': record['permission'],
                            'resource': record['permission_resource']
                        }
                    )
                else:
                    abilities.append(
                        {
                            'id': ability_id,
                            'ability': record['ability'],
                            'constant': record['constant'],
                            'description': record['description'],
                            'permissions': [
                                {
                                    'permission': record['permission'],
                                    'resource': record['permission_resource']
                                }
                            ]
                        }
                    )

        except Exception as e:
            raise ArcimotoException(str(e)) from e

        finally:
            # explicitly close the auth connection
            arcimoto.db.close(_AUTHENTICATION_ROLE)
            self.abilities = abilities

    def reset(self):
        self.abilities = []

    def _query_abilities_list(self):
        query = (
            'SELECT ua.id, ua.ability, ua.constant, ua.description, '
            'pj.permission, pj.permission_resource '
            'FROM user_ability as ua '
            'LEFT JOIN user_ability_permission_join as pj ON '
            'ua.id = pj.ability_id '
            'ORDER BY ua.id ASC'
        )
        return query
