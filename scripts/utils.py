import os



def _join_dir(dir1, dir2):
    joined = os.path.join(dir1, dir2)
    if not os.path.exists(joined):
        os.makedirs(joined)
    return joined

def _error(msg):
    raise Exception(f'Error: msg')

def _info(msg):
    print(msg)

def _must_exist(path):
    if not os.path.exists(path):
        raise Exception('Paht not found:{path}')