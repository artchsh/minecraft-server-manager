import requests
from tqdm import tqdm
from config import read_config
import time

def download_file(url, filename):
    # Send a GET request to the URL
    response = requests.get(url, stream=True)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Get the total file size
        total_size = int(response.headers.get('content-length', 0))
        
        # Open the file in write-binary mode
        with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            start_time = time.time()
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)
                
                # Calculate and display estimated time remaining
                elapsed_time = time.time() - start_time
                if progress_bar.n > 0:
                    estimated_total_time = elapsed_time * total_size / progress_bar.n
                    remaining_time = estimated_total_time - elapsed_time
                    progress_bar.set_postfix({"Remaining": f"{remaining_time:.1f}s"})

        print(f"\nFile downloaded successfully: {filename}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

def get_java():
    config = read_config()
    java_path = config['Java']['path']
    if java_path == 'java':
        return "java"
    return f'"{java_path}"'

def parse_config_versions(core: str):
    config = read_config()
    return config['Cores'][f'{core}_versions'].split(',')

if __name__ == "__main__":
    download_file("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "dummy.pdf")