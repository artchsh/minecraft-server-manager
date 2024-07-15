import configparser, os
 
 
def create_config():
    config = configparser.ConfigParser()

    config['BuildTools'] = {
        'download_url': 'https://hub.spigotmc.org/jenkins/job/BuildTools/lastStableBuild/artifact/target/BuildTools.jar', 
        'info_url': 'https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/api/json',
        'build_number_installed': '0'
    }
    config['Cores'] = {
        'spigot_versions': '1.21,1.20.6,1.19.4,1.18.2,1.17.1,1.16.5,1.15.2,1.14.4,1.13.2,1.12.2,1.11.2,1.10.2,1.9.4,1.8.8,1.7.10',
        'spigot_info_url': 'https://hub.spigotmc.org/jenkins/job/Spigot-RSS/lastSuccessfulBuild/api/json',
    }
    config['Java'] = {
        'path': 'java', 
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def read_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    
    if not os.path.exists('config.ini'):
        print("Config file not found. Creating a new one...")
        create_config()
    
    config.read('config.ini')
    return config

def write_config_key(section: str, key: str, value: str):
    config = read_config()
    config[section][key] = value
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
 
if __name__ == "__main__":
    create_config()