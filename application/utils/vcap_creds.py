import os
import json

SERVICES = json.loads(os.getenv('VCAP_SERVICES', '{}'))

def get_creds(service_name, tag=None):
    if service_name not in SERVICES:
        raise EnvironmentError("Service does not exist in environment")
    service_instance = SERVICES.get(service_name)
    for item in service_instance:
        if tag:
            creds = {
                k: v for (k,v) in item.items()
                if k == 'credentials' if tag in d['tags']
            }
        else:
            creds = {k: v for (k,v) in item.items() if k == 'credentials'}
            break
    return creds['credentials']
