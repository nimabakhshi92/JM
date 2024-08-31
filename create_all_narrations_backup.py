import requests
import jdatetime
from pathlib import Path
import os

AUTOMATION_PATH = Path(os.path.abspath(__file__)).parent
os.chdir(AUTOMATION_PATH)

resp = requests.get('http://localhost:4000/api/download_narrations/?ids=')
if resp.status_code == 200:
    folder_path = os.path.join('zipBackup')
    filename = f'All- {jdatetime.datetime.now().strftime("%Y-%m-%d---%H-%M-%S")}.zip'
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'wb') as f:
        f.write(resp.content)
