import os, build_tools, spigot, db

def create_spigot_core(server_name: str, version: str):
    os.system('cls' if os.name == 'nt' else 'clear')
    db.create_new_server_record(server_name, 'spigot', '0', version)
    build_tools.check_build_tools_version()
    spigot.build_spigot(version, server_name)
    spigot.run_spigot_first_time(server_name)

CORES = {
    'spigot': {
        'create': create_spigot_core,
        'run': spigot.run_spigot
    }
}
