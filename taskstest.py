from celery import Celery
from celery.schedules import crontab
import datetime
import subprocess
from .Gdrive import upload_basic

date_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
command = ['mysqldump', '-u', 'root', '-pnewpassword', 'JM']
with open(f'sqlbackup/backup{date_time}.sql') as output_file:
    subprocess.run(command, stdout=output_file, text=True)

file_metadata = {'name': f'sqlbackup/backup{date_time}.sql'}
filename = f'sqlbackup/backup{date_time}.sql'
mimetype = 'sql/sql'
upload_basic(file_metadata, filename, mimetype)
