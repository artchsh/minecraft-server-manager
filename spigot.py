import os
from utils import get_java, get_java_memory

def build_spigot(minecraft_version: str, server_name: str):
    java = get_java()
    os.system("mkdir servers")
    os.system(f"cd servers && mkdir {server_name}")
    cmd = f"cd build_tools && {java} -jar BuildTools.jar --rev {minecraft_version} -o ../servers/{server_name} --final-name server.jar"
    os.system(cmd)

def run_spigot_first_time(server_name: str):
    java = get_java()
    os.system(f"cd servers/{server_name} && {java} -jar server.jar nogui")
    with open(f"servers/{server_name}/eula.txt", "w") as f:
        f.write("eula=true")
        f.close()

def run_spigot(server_name: str):
    java = get_java()
    mem = get_java_memory()
    os.system(f"cd servers/{server_name} && {java} -Xmx{mem}M -Xms512M -jar server.jar nogui")