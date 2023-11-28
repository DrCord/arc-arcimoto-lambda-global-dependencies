import psycopg2
from psycopg2 import extras
from psycopg2 import sql
import functools

from arcimoto.exceptions import ArcimotoException
import arcimoto.runtime

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# _connections in global scope will persist the connections for the life of the lambda
# container
_connections = {}


def check_record_exists(table, column_values, column_to_check=None, mock=False):
    (query_string, sql_identifiers, args) = _check_record_exists_query_prepare(
        table,
        column_values,
        column_to_check
    )
    if mock:
        return (query_string, sql_identifiers, args)

    return _check_record_exists_query_execute(query_string, sql_identifiers, args)


def _check_record_exists_query_prepare(table, column_values, column_to_check=None):
    sql_identifiers = []
    query_string = (
        'SELECT * '
        'FROM {} '
        'WHERE '
    )
    counter = 1
    sql_identifiers.append(table)
    args = []
    for column, value in column_values.items():
        query_string += '{} = %s'
        sql_identifiers.append(column)
        args.append(value)
        if len(column_values) != counter:
            query_string += ' AND '
            counter += 1
    if column_to_check is not None:
        query_string += ' AND {} IS NOT NULL'
        sql_identifiers.append(column_to_check)

    return (query_string, sql_identifiers, args)


def _check_record_exists_query_execute(query_string, sql_identifiers, args):
    cursor = arcimoto.db.get_cursor()
    # safe query composition -
    # https://www.psycopg.org/docs/sql.html
    # https://stackoverflow.com/a/46770525/1291935
    query = sql.SQL(query_string).format(*map(sql.Identifier, sql_identifiers))
    cursor.execute(query, args)

    return (cursor.rowcount == 1)


def close(role=None):
    global _connections

    if role is None:
        role = arcimoto.runtime.get_role()

    secret_name = _secret_name_assemble(role)

    conn = _connections.get(secret_name, None)
    if conn is not None:
        conn.close()
        del _connections[secret_name]


def datetime_record_output(datetime_record):
    return str(datetime_record) if datetime_record is not None else None


def _db_connect(conn_string, mock=False):
    if mock:
        return conn_string

    try:
        return psycopg2.connect(conn_string, cursor_factory=extras.DictCursor)
    except Exception as e:
        raise ArcimotoException('Unable to open DB connection: {}'.format(e)) from e


def _db_connection_string_assemble(secret):
    return 'dbname={} user={} host={} password={}'.format(
        secret['dbname'],
        secret['username'],
        secret['host'],
        secret['password']
    )


def _get_conn(secret_name=None, mock=False):

    if secret_name is None:
        raise ArcimotoException('No secret_name specified')

    try:
        secret = arcimoto.runtime.get_secret(secret_name)
        conn_string = _db_connection_string_assemble(secret)
        return _db_connect(conn_string, mock)

    except Exception as e:
        raise ArcimotoException('Unable to open DB connection: {}'.format(e)) from e


def get_cursor(role=None, mock=False):
    ''' if mock=True will return the connection string instead of an active connection cursor '''
    global _connections

    if role is None:
        role = arcimoto.runtime.get_role()

    secret_name = _secret_name_assemble(role)

    conn = _connections.get(secret_name, None)
    if conn is None:
        conn = _get_conn(secret_name, mock)
        if mock:
            return conn
        _connections[secret_name] = conn

    return conn.cursor()


def prepare_update_query_and_params(table_name, where_predicates, columns_data, allow_none=False):
    columns = []
    column_values = []
    value_placeholders = []
    sql_identifiers = []
    allowed_ops = {
        '=': '=',
        '!=': '!=',
        '<>': '<>',
        '>': '>',
        '<': '<',
    }

    query_template = (
        'UPDATE {} '
        'SET '
    )
    sql_identifiers.append(table_name)

    for column_data in columns_data:
        for column_name in column_data:
            if allow_none or column_data[column_name] is not None:
                columns.append(column_name)
                column_values.append(column_data[column_name])
                value_placeholders.append('%s')

    # query has to be formatted differently for a single column vs multiple
    if len(columns) == 1:
        sql_identifiers.append(columns[0])
        query_template += '{} = '
        query_template += (
            f'{value_placeholders[0]} '
            'WHERE '
        )
    else:
        columns_len = len(columns)
        query_template += '('
        for i in range(0, columns_len):
            query_template += '{}'
            sql_identifiers.append(columns[i])
            if i != columns_len - 1:
                query_template += ', '
        query_template += (
            ') = '
            f'({", ".join(value_placeholders)}) '
            'WHERE '
        )

    where_values = []
    for where_predicate in where_predicates:
        query_template += (
            '{} ' + f'{allowed_ops[where_predicate["operator"]]}' + ' %s '
        )
        sql_identifiers.append(where_predicate['column'])
        where_values.append(where_predicate['value'])
        if len(where_predicates) != len(where_values):
            query_template += 'AND '
    query_template += (
        'RETURNING {}.*'
    )
    sql_identifiers.append(table_name)

    # safe query composition - https://www.psycopg.org/docs/sql.html and https://stackoverflow.com/a/46770525/1291935
    query = sql.SQL(query_template).format(*map(sql.Identifier, sql_identifiers))

    params = [*column_values, *where_values]
    return (query, params)


def _secret_name_assemble(role_name=None):
    try:
        if role_name is None:
            role_name = arcimoto.runtime.get_role()

        env = arcimoto.runtime.get_env()

        secret_name = '.'.join([role_name, 'db', env])
        return secret_name

    except Exception as e:
        raise ArcimotoException(f'Unable to assemble secret name: {e}') from e


def transaction_for_role(role_name):
    '''
    Decorator that will automatically commit or catch an Exception
    and rollback any DB transaction if the connection has been established.
    Will re-raise any exceptions without wrapping in an ArcimotoException

    Takes an explicit role_name to use for DB connection management.
    '''
    if role_name is None:
        raise ArcimotoException('Unable to open transaction: transaction_for_role decorator requires role_name')

    def _wrap(function):

        @functools.wraps(function)
        def _impl(*args, **kwargs):
            global _connections

            # mute is used during tests
            mute = kwargs.get('mute', False)

            secret_name = _secret_name_assemble(role_name)

            try:
                response = function(*args, **kwargs)
                # you must wait until after the function call to fetch the connection
                # because connections are opened from within the call on demand
                conn = _connections.get(secret_name, None)

                if conn is not None:
                    conn.commit()
                else:
                    if not mute:
                        print(f'UNABLE TO COMMIT WITHOUT CONNECTION for {role_name}')
                return response

            except Exception as e:
                conn = _connections.get(secret_name, None)

                if conn is not None:
                    conn.rollback()
                else:
                    if not mute:
                        print(f'UNABLE TO ROLLBACK WITHOUT CONNECTION for {role_name}')
                raise e

        return _impl

    return _wrap


def transaction(function):
    '''
    Decorator that will automatically commit or catch an Exception
    and rollback any DB transaction if the connection has been established.
    Will re-raise any exceptions without wrapping in an ArcimotoException

    Uses the default execution role for DB connection management.
    '''

    @functools.wraps(function)
    def _impl(*args, **kwargs):
        global _connections

        role = arcimoto.runtime.get_role()
        secret_name = _secret_name_assemble(role)

        # mute is used during tests
        mute = kwargs.get('mute', False)

        try:
            response = function(*args, **kwargs)
            # you must wait until after the function call to fetch the connection
            # because connections are opened from within the call on demand
            conn = _connections.get(secret_name, None)

            if conn is not None:
                conn.commit()
            else:
                if not mute:
                    print(f'UNABLE TO COMMIT WITHOUT CONNECTION for role {role}')
            return response

        except Exception as e:
            conn = _connections.get(secret_name, None)

            if conn is not None:
                conn.rollback()
            else:
                if not mute:
                    print(f'UNABLE TO ROLLBACK WITHOUT CONNECTION for role {role}')
            raise e

    return _impl
