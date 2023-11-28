import boto3
import json

# get env resources
with open('env_resources.json') as f:
    env_resources = json.load(f)


def get_secret(secret_id):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId=secret_id
    )
    return json.loads(response['SecretString'])


def get_env_from_arn(arn):
    # default to dev
    env = 'dev'
    if arn.endswith(':staging'):
        env = 'staging'
    elif arn.endswith(':prod'):
        env = 'prod'
    return env


def get_env_from_vin(vin):
    # default to prod
    env = 'prod'
    if vin.startswith('DEV-'):
        env = 'dev'
    elif vin.startswith('STAGE-'):
        env = 'staging'
    return env


def get_conn_string(env, user_type):
    secret_id = env_resources[env][user_type]
    secret = get_secret(secret_id)
    conn_string = 'dbname=' + secret['dbname'] + ' user=' + secret['username'] + ' host=' + secret['host'] + ' password=' + secret['password']
    return conn_string
