
import os, db
from utils import parse_config_versions
from cores import CORES

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Minecraft Server Manager")
    print("[0] - Configure a new Minecraft Server")
    print("[1] - Start an existing Minecraft Server")
    print("[2] - Exit")
    choice = input("Enter your choice -> ")
    if choice == '0':
        create_new_minecraft_server()
    elif choice == '1':
        exit()
    elif choice == '2':
        exit()
    else:
        main()

def create_new_minecraft_server():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Choose name for your server")
    print("--------------------------------")
    print("[9] - Back")
    minecraft_server_name = input("-> ")
    if minecraft_server_name == '9':
        main()
    else:
        choose_core(minecraft_server_name)

def choose_core(server_name: str):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Now choose your server's core")
    print("[0] - Spigot")
    print("--------------------------------")
    print("[9] - Back")
    choice = input("Enter your choice -> ")
    if choice == '0':
        choose_version(server_name, 'spigot')

    elif choice == '9':
        create_new_minecraft_server()
    else:
        choose_core()

def choose_version(server_name: str, core: str):
    os.system('cls' if os.name == 'nt' else 'clear')
    core_versions = parse_config_versions(core)
    print("Now choose your server's version")
    for i in range(len(core_versions)):
        print(f"[{i}] - {core_versions[i]}")
    print("--------------------------------")
    print("[99] - Back")
    choice = input("Enter your choice -> ")
    if choice != "99":
        version = core_versions[int(choice)]
        CORES[core](server_name, version)
        db.create_new_server_record(server_name, 'spigot', version)
    else:
        choose_core(server_name)

if __name__ == "__main__":
    main()