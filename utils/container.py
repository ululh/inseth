import os
def storage_prefix():
    in_container = os.environ.get('IN_CONTAINER', False)
    if in_container:
        return('/data')
    else:
        return('/home/ulul/inseth')


