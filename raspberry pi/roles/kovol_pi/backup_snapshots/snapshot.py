import os
import shutil
import datetime
import time
import hashlib
import filecmp
import logging
import logging.handlers

essential_files = '/home/pi/Documents/backup_snapshots/essential_files.txt' # file path to a text file containing filepaths to back up
snapshot_folder = '/home/pi/Documents/backup_snapshots' # folder to do the backups to
# essential_files = '/home/steve/Documents/Computing/Python_projects/snapshot_script/essential_files.txt'
# snapshot_folder = '/home/steve/Documents/Computing/Python_projects/snapshot_script/snapshots'
months_to_backup = 6

log = logging.getLogger('log')
fh = logging.handlers.RotatingFileHandler('backup_error_log.txt')
form = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh = logging.StreamHandler()
fh.setFormatter(form)
log.addHandler(fh)
log.addHandler(sh)
run_log = logging.getLogger('run_log')
f = logging.FileHandler('run_log.txt')
run_log.setLevel('INFO')
run_log.addHandler(f)
run_log.info('\nRan at %s' % str(datetime.datetime.now()))


try:
    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder)
    os.chdir(snapshot_folder)
    # get backup targets
    with open(essential_files) as f:
        file_list = f.readlines()
    file_list = [i.strip() for i in file_list]
    files = []
    # check files exist and is not a directory
    for file in file_list:
        if not os.path.exists(file):
            log.error('%s does not exist' % file)
        if os.path.isdir(file):
            log.error('%s is a directory' % file)
            raise IsADirectoryError
        else:
            files.append(file)
    filenames = [os.path.splitext(os.path.basename(i))[0] for i in files]

    # do the backup
    folders_backed_up = []
    for name, item in zip(filenames, files):
        folder = os.path.join(snapshot_folder, name)
        folders_backed_up.append(folder)
        if not os.path.isdir(folder):
            os.mkdir(folder)
        os.chdir(folder)
        old_files = os.listdir()
        run_log.info('Folder = %s'% folder)
        if len(old_files) > 0:
            run_log.info('More than one file')
            newest_file = max(old_files, key=os.path.getctime)
            run_log.info('Newest file = %s, current file = %s' % (newest_file, item))
            if filecmp.cmp(newest_file, item):
                run_log.info('same file, no copy')
                continue
            else:
                run_log.info('Files seem to be different, should copy')
        date = str(datetime.datetime.now().strftime('%d_%m_%y_'))
        new_name = date + os.path.basename(item)
        shutil.copyfile(item, os.path.join(folder, new_name))
        run_log.info('%s copied to %s' % (item, new_name))

    # clean up old versions
    for folder in folders_backed_up:
        os.chdir(folder)
        files = os.listdir(folder)
        # always leave at least 1 version
        if len(files) < 2:
            continue
        for file in files:
            file = os.path.abspath(file)
            mod = datetime.datetime.fromtimestamp(os.path.getmtime(file))
            since = datetime.datetime.now() - mod
            if since.days > months_to_backup *30:
                run_log.info('Removing %s' % file)
                os.remove(file)
                
except:
    date = str(datetime.date.today())
    log.exception('\n###Fatal error %s ###' % date)