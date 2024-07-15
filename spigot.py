import os, requests, db
from utils import get_java
from config import read_config
from main import main

def build_spigot(minecraft_version: str, server_name: str):
    java = get_java()
    os.system("mkdir servers")
    os.system(f"cd servers && mkdir {server_name}")
    is_latest, _ = is_last_version_installed(server_name)
    if is_latest:
        print("Latest spigot version is already installed. Skipping...")
        return
    cmd = f"cd build_tools && {java} -jar BuildTools.jar --rev {minecraft_version} -o ../servers/{server_name} --final-name server.jar"
    os.system(cmd)
    

def run_spigot_first_time(server_name: str):
    java = get_java()
    os.system(f"cd servers/{server_name} && {java} -jar server.jar nogui")
    with open(f"servers/{server_name}/eula.txt", "w") as f:
        f.write("eula=true")
        f.close()
    run_spigot(server_name, skip_build_step=True)

def run_spigot(server_name: str, skip_build_step: bool = False):
    java = get_java()
    mem = db.get_server_by_name(server_name)['memory']
    if not skip_build_step:
        build_spigot(db.get_server_by_name(server_name)['version'], server_name)
    os.system(f"cd servers/{server_name} && {java} -Xmx{mem}M -Xms512M -jar server.jar nogui")
    main()
    
def is_last_version_installed(server_name: str):
    config = read_config()
    installed_BN = 0
    try:
        installed_BN = db.get_server_by_name(server_name)['core_build_number']
    except:
        pass
    response = requests.get(config['Cores']['spigot_info_url'])
    if response.status_code == 200:
        latest_BN = response.json()['number']
        print(f"Installed spigot build number: {installed_BN}")
        print(f"Latest spigot build number: {latest_BN}")
        if int(installed_BN) < int(latest_BN):
            db.update_server_core_build_number(server_name, latest_BN)
            return False, latest_BN
        else:
            return True, latest_BN