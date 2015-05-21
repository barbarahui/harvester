'''Configuration for the harvester and associated code.
UCLDC specfic information comes from environment variables and the
values are filled in directly in returned namedtuple.

DPLA values are contained in a ConfigParser object that is returned in the
namedtuple.
'''
import os
from collections import namedtuple
import ConfigParser

REDIS_HOST = '10.0.0.68'
REDIS_PORT = '6379'
DPLA_CONFIG_FILE = 'akara.ini'

def config(config_file=None, redis_required=False, ec2_required=False):
    '''Return the HarvestConfig namedtuple for the harvester'''
    if not config_file:
        config_file = os.environ.get('DPLA_CONFIG_FILE', DPLA_CONFIG_FILE)
    DPLA = ConfigParser.ConfigParser()
    DPLA.readfp(open(config_file))
    env = parse_env(DPLA, redis_required=redis_required,
                    ec2_required=ec2_required)
    env['DPLA'] = DPLA
    return env


def parse_env(DPLA, redis_required=False, ec2_required=False):
    '''Get any overrides from the runtime environment for the server variables
    If redis_required, raise KeyError if REDIS_PASSWORD not found
    if ec2_required, raise KeyError if ec2 id env vars not found
    '''
    env = {}
    env['redis_host'] = os.environ.get('REDIS_HOST', REDIS_HOST)
    env['redis_port'] = os.environ.get('REDIS_PORT', REDIS_PORT)
    env['redis_connect_timeout'] = os.environ.get('REDIS_CONNECT_TIMEOUT', 10)
    env['redis_password'] = env['id_ec2_ingest'] = env['id_ec2_solr_build'] = None
    try:
        env['redis_password'] = os.environ['REDIS_PASSWORD']
    except KeyError, e:
        if redis_required:
            raise KeyError(''.join(('Please set environment variable ',
                                    'REDIS_PASSWORD to redis password!')))
    try:
        env['id_ec2_ingest'] = os.environ['ID_EC2_INGEST']
    except KeyError, e:
        if ec2_required:
            raise KeyError(''.join(('Please set environment variable ',
                                    'ID_EC2_INGEST to main ingest ',
                                    'ec2 instance id.')))
    try:
        env['id_ec2_solr_build'] = os.environ['ID_EC2_SOLR_BUILD']
    except KeyError, e:
        if ec2_required:
            raise KeyError(''.join(('Please set environment variable ',
                                    'ID_EC2_SOLR_BUILD to ingest ',
                                    'solr instance id.')))

    env['couchdb_url'] = os.environ.get('COUCHDB_URL', None)
    env['couchdb_username'] = os.environ.get('COUCHDB_USER', None)
    env['couchdb_password'] = os.environ.get('COUCHDB_PASSWORD', None)
    env['couchdb_dbname'] = os.environ.get('COUCHDB_DB', None)
    env['couchdb_dashboard'] = os.environ.get('COUCHDB_DASHBOARD', None)
    if not env['couchdb_url']:
        env['couchdb_url'] = DPLA.get("CouchDb", "URL")
    if not env['couchdb_username']:
        env['couchdb_username'] = DPLA.get("CouchDb", "Username")
    if not env['couchdb_password']:
        env['couchdb_password'] = DPLA.get("CouchDb", "Password")
    if not env['couchdb_dbname']:
        env['couchdb_dbname'] = DPLA.get("CouchDb", "ItemDatabase")
    if not env['couchdb_dashboard']:
        env['couchdb_dashboard'] = DPLA.get("CouchDb", "DashboardDatabase")
    if not env['couchdb_url']:
        env['couchdb_url'] = 'http://127.0.0.1:5984'
    if not env['couchdb_dbname']:
        env['couchdb_dbname'] = 'ucldc'
    if not env['couchdb_dashboard']:
        env['couchdb_dashboard'] = 'dashboard'
    return env