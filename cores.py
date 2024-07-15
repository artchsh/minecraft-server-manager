import os, build_tools, spigot

def create_spigot_core(server_name: str, version: str):
    os.system('cls' if os.name == 'nt' else 'clear')
    build_tools.check_build_tools_version()
    spigot.build_spigot(version, server_name)
    spigot.run_spigot_first_time(server_name)

CORES = {
    'spigot': create_spigot_core
}
