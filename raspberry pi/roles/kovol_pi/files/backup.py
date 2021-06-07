#!/usr/bin/python3

# Run as root (necessary due to working with Docker)
# Stops docker containers, backs up volumes with duplicity, capturing output in log, then restarts containers

# Restoration can be achieved with a command similar to below (after docker volume create <volume name>)
# sudo duplicity --no-encryption --file-to-restore nextcloud_data/ --force file:///mnt/disk2/docker-backup/ /mnt/disk1/docker-data/volumes/nextcloud_data

import subprocess
import logging
import logging.handlers
import datetime


def initiate_logging(log_file: str):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler(log_file)
    f = logging.Formatter("%(message)s")
    fh.setFormatter(f)
    logger.addHandler(fh)
    logger.addHandler(logging.StreamHandler())
    return logger


def stop_containers(compose_files: list):
    for f in compose_files:
        subprocess.run(["/usr/local/bin/docker-compose", "-f", f["file"], "--env", f["env"], "down"])


def start_containers(compose_files: list):
    for f in compose_files:
        subprocess.run(
            ["/usr/local/bin/docker-compose", "-f", f["file"], "--env", f["env"], "up", "-d"]
        )


def backup(source: str, destination: str):
    global errors
    # Cleanup old backups
    subprocess.run(["duplicity", "remove-older-than", "3M", destination])

    # Run backup
    backup = subprocess.run(
        [
            "duplicity",
            "--no-encryption",
            "--allow-source-mismatch",
            "--full-if-older-than",
            "2M",
            source,
            destination,
        ],
        capture_output=True,
    )

    # Logging
    if backup.returncode != 0:
        logger.error(
            "Backup to {b} is reporting errors:\n{errors}".format(
                b=destination, errors=backup.stderr
            )
        )
        errors = True
    else:
        if backup.stdout:
            logger.info("Backup to {b}:".format(b=destination))
            details = backup.stdout.decode("utf-8").strip().split("\n")
            for l in details:
                logger.info(l)


if __name__ == "__main__":
    logger = initiate_logging(log_file="/code/logs/backup.log")
    errors = False

    compose_files = [
        {
            "file": "/etc/docker/kovol_server_docker-compose.yml",
            "env": "/etc/docker/nextcloud.env",
        }
    ]
    logger.info("<span style=\"white-space: pre;\">")
    logger.info("\nBackup started: {t}".format(t=datetime.datetime.now().strftime("%a %d %b, %H:%M")))
    start = datetime.datetime.now()
    print("Starting local backup")

    stop_containers(compose_files)
    backup(
        source="/mnt/disk1/docker-data/volumes/",
        destination="file:///mnt/disk2/docker-backup/",
    )
    start_containers(compose_files)
    # print('Starting remote backup')
    # backup('{{ remote_backup_location }}')

    finish = datetime.datetime.now()
    # Log any errors
    if errors:
        logger.error("Backup script finished with errors")
    else:
        logger.info(
            "Backup script finished sucessfully: {d}".format(
                d=datetime.date.today().strftime("%a %d %b")
            )
        )
        logger.info("Backup took {t}".format(t=str(finish - start)))
    logger.info("</span>")