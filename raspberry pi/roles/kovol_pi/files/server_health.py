#!/usr/bin/python3

import datetime
import os
import shutil
import subprocess
import logging
import logging.handlers
from subprocess import PIPE

errors = []
in_kovol = False


def ok(msg):
    green = "\033[92m"
    white = "\033[0m"
    ok = green + "Pass	" + white
    print(ok + msg)


def fail(msg):
    global errors
    white = "\033[0m"
    red = "\033[91m"
    errors.append(msg)
    fail = red + "Fail	" + white
    print(fail + msg)


try:
    print("{date} Testing server...\n".format(date=datetime.date.today()))

    print("--- Server ---")
    # check disk usage
    disk_usage = shutil.disk_usage("/mnt/disk1")
    percent = disk_usage.used / disk_usage.total * 100

    if percent > 75:
        fail("Team share disk usage above 75%")
    else:
        ok("Team share disk usage {x:.0f}%".format(x=percent))

    disk2_usage = shutil.disk_usage("/mnt/disk2")
    percent2 = disk2_usage.used / disk2_usage.total * 100

    if percent2 > 75:
        fail("Backup disk usage above 75%")
    else:
        ok("Backup disk usage {x:.0f}%".format(x=percent2))

    sd_usage = shutil.disk_usage("/")
    sd_percent = sd_usage.used / sd_usage.total * 100

    if sd_percent > 85:
        fail("SD card disk usage above 85%")
    else:
        ok("SD card usage at {x:.0f}%".format(x=sd_percent))

    # check sticks are mounted
    if not os.path.exists("/mnt/disk1/docker-data") or not os.path.exists(
        "/mnt/disk2/docker-backup"
    ):
        fail("External storage not mounted")
    try:
        rtn1 = subprocess.run(["ls", "/mnt/disk1"], stdout=PIPE)
        rtn1.check_returncode()
        rtn2 = subprocess.run(["ls", "/mnt/disk2"], stdout=PIPE)
        rtn2.check_returncode()
    except subprocess.CalledProcessError:
        fail("External storage not mounted properly")

    else:
        ok("External storage mounted")

    # check memory usage
    memory_data = subprocess.run(["free"], stdout=PIPE).stdout.decode()
    m = memory_data.split(" ")
    m = [t for t in m if t]
    total = int(m[6])
    used = int(m[7])
    percent = used / total * 100

    if percent > 75:
        fail("Memory usage is too high: {p:.0f}%".format(p=percent))
    else:
        ok("Memory usage at {p:.0f}%".format(p=percent))

    # check CPU usage
    cpu = subprocess.run(["uptime"], stdout=PIPE).stdout.decode()
    cpu = float(cpu.split(" ")[-1])
    if cpu > 50:
        fail("CPU usage too high, averaging {p:.0f}%".format(p=cpu))

    else:
        ok("CPU usage averaging {p:.2f}%".format(p=cpu))

    print("\n--- Applications ---")

    # check Lexicon log for content
    try:
        with open("/code/logs/lexicon_error.html", "r") as lexicon_log:
            content = lexicon_log.read()
            if content:
                fail("Lexicon log has errors, application is failing")
            else:
                ok("Lexicon program not reporting errors")
    except FileNotFoundError:
        print('No lexicon log found')

    print("\n--- Backups ---")
    try:
        with open("/code/logs/backup.html") as backup_log:
            content = backup_log.read()
            if datetime.date.today().strftime("%a %d %b") not in content:
                fail("Backup didn't run")
            elif (
                "Backup script finished sucessfully: {d}".format(
                    d=datetime.date.today().strftime("%a %d %b")
                )
                not in content
            ):
                fail("Backup didn't sucessfully complete")
            else:
                ok("Backups completed sucessfully")
    except FileNotFoundError:
        print('No backup log found')

    if in_kovol:
        print("\n--- Backup_pi ---")
            # check interface status
        itf = subprocess.run(["/sbin/ifconfig", "-s"], stdout=PIPE).stdout.decode()
        if "wlan0" in itf:
            fail("Wireless interface is on")
        elif "eth0" not in itf:
            fail("Wired interface is off")
        else:
            ok("Network interfaces functioning")

        # check connecition to backup_pi
        host = "192.168.0.11"
        response = os.system("ping -qc 1 " + host + " 2>&1 >/dev/null")
        if response == 0:
            ok("Connected to backup_pi")
            backup_pi_connection = True
        else:
            fail("Not connected to backup_pi")
            backup_pi_connection = False

        # check ssh to backup pi
        if backup_pi_connection:
            response = os.system("ssh -q kovol@{h} 'exit 0'".format(h=host))
            if response == 0:
                ok("Valid SSH connection to backup_pi")
            else:
                fail("Cannot SSH into backup_pi")

            # check backup_pi diskspace
            response = subprocess.run(
                ["ssh", "kovol@{h}".format(h=host), "df", "|", "grep", "root"],
                stdout=PIPE,
            )
            output = response.stdout.decode()
            percent = output.find("%")
            usage = int(output[int(percent) - 2 : percent])

            if usage > 75:
                fail("Backup_pi disk usage above 75%")
            else:
                ok("Backup_pi disk usage at {p}%".format(p=usage))

    print("\n--- Web services ---")

    # Check websites online
    http = "http://localhost"
    websites = [
        ("Main page", http),
        ("CLAHub", http + ":8000"),
        ("Lexicon", http + "/lexicon/main_dict.html"),
        ("Songs", http + "/songs/KovolSongbook.html"),
        ("Texts", http + "/texts/index.html"),
        ("Nextcloud", http + ":8080/login"),
    ]
    for site in websites:
        rsp = subprocess.run(["curl", "-Is", site[1]], stdout=PIPE).stdout.decode()
        if "200 OK" in rsp:
            ok("{site} is online".format(site=site[0]))
        else:
            fail("{site} is offline".format(site=site[0]))

    # collate errors and report them
    print("\n\n--- Summary ---")
    if errors:
        print("There are server erors:")
        for error in errors:
            print('	--{e}'.format(e=error))
    else:
        print("No problems")

finally:
    # add to a system log
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler("/code/logs/server_health.html")
    f = logging.Formatter("%(message)s")
    fh.setFormatter(f)
    logger.addHandler(fh)
    time = datetime.datetime.now()
    logger.info("<span style=\"white-space: pre;\">{d}".format(d=time))
    if errors:
        logger.error("Errors were found: {e}".format(e=errors))
    else:
        logger.info("No problems")
    logger.info("</span>")