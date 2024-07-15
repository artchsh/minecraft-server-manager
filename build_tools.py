import requests, os
from config import read_config, write_config_key
from utils import download_file

def check_build_tools_version():
    print("Checking BuildTools version...")
    config = read_config()
    info_url = config['BuildTools']['info_url']
    response = requests.get(info_url)
    if response.status_code == 200:
        data = response.json()
        latest_build_number = data['id']
        current_build_number = config['BuildTools']['build_number_installed']
        print(f"Latest BuildTools version: {latest_build_number}\nCurrent BuildTools version: {current_build_number}")
        
        if int(latest_build_number) > int(current_build_number):
            print("A new version of BuildTools is available.")
            print("Downloading and updating BuildTools...")
            update_build_tools(latest_build_number)
    else:
        print(f"Failed to get BuildTools version. Status code: {response.status_code}")
        
def update_build_tools(build_number: str):
    config = read_config()
    download_url = config['BuildTools']['download_url']
    os.system("mkdir build_tools")
    download_file(download_url, "build_tools/BuildTools.jar")
    write_config_key('BuildTools', 'build_number_installed', f"{build_number}")
    os.system('cls' if os.name == 'nt' else 'clear')
    print("BuildTools updated successfully.")
    pass

if __name__ == "__main__":
    check_build_tools_version()