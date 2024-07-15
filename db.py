import json, os

FILE = 'db/msm.json'

def write_data(data: list[dict]):
    f = open(FILE, 'w')
    f.write(json.dumps(data, indent=2))
    f.close()

def read_data() -> list[dict]:
    os.system('mkdir db')
    if not os.path.exists(FILE):
        f = open(FILE, 'w')
        f.write(json.dumps([], indent=2))
        f.close()
    f = open(FILE, 'r')
    data = json.loads(f.read())
    f.close()
    return data

def create_new_server_record(server_name: str, core: str, core_build_number: str, version: str):
    server = {
        'name': server_name,
        'core': core,
        'core_build_number': core_build_number,
        'version': version,
        'local_ip': '',
        'memory': '2048'
    }
    data = read_data()
    data.append(server)
    write_data(data)
    
def get_server_by_name(server_name: str) -> dict:
    data = read_data()
    for server in data:
        if server['name'] == server_name:
            return server

def get_all_servers() -> list[dict]:
    return read_data()


def update_server_local_ip(server_name: str, local_ip: str):
    data = read_data()
    for server in data:
        if server['name'] == server_name:
            server['local_ip'] = local_ip
    write_data(data)
    
def delete_server(server_name: str):
    data = read_data()
    for server in data:
        if server['name'] == server_name:
            data.remove(server)
    write_data(data)
    
def delete_all_servers():
    write_data([])

def update_server_core_build_number(server_name: str, core_build_number: str):
    data = read_data()
    for server in data:
        if server['name'] == server_name:
            server['core_build_number'] = core_build_number
    write_data(data)
    
def server_name_exists(server_name: str):
    data = read_data()
    for server in data:
        if server['name'] == server_name:
            return True
    return False