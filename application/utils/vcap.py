import os
import json


SERVICES = json.loads(os.getenv('VCAP_SERVICES', '{}'))


def creds(service_name, tag=None):
    """
    Return credentials field for any vcap service.
    """
    if service_name not in SERVICES:
        raise EnvironmentError("Service does not exist in environment")
    service_instance = SERVICES.get(service_name)
    for item in service_instance:
        if tag:
            creds = {
                k: v for (k,v) in item.items()
                if k == 'credentials' and tag in d['tags']
            }
        else:
            creds = {k: v for (k,v) in item.items() if k == 'credentials'}
            break
    return creds['credentials']


def strip_redis_creds(creds):
    """
    Filter out extra values in HSDP vcap redis creds not needed for this demo
    """
    return {
        k: v for k, v in creds.iteritems() if k in ['host', 'password', 'port']
    }

