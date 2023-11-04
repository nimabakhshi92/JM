from celery import Celery
from celery.schedules import crontab
import datetime
import subprocess
from Gdrive import upload_basic

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        #        crontab(hour=7, minute=30),
        crontab(minute='*/1'),
        backup_db.s(),
    )


@app.task
def backup_db():
    date_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    command = ['mysqldump', '-u', 'root', '-pnewpassword', 'JM']
    with open(f'sqlbackup/backup{date_time}.sql', 'w') as output_file:
        subprocess.run(command, stdout=output_file, text=True)

    file_metadata = {'name': f'backup{date_time}.sql'}
    filename = f'sqlbackup/backup{date_time}.sql'
    mimetype = 'sql/sql'
    upload_basic(file_metadata, filename, mimetype
                 )
    command_restore = ['mysql', '-u', 'root', '-pnewpassword', 'JMStaging']
    with open(filename, 'r') as input_file:
        subprocess.run(command_restore, stdin=input_file)