import subprocess
import os

import ntplib
from datetime import datetime, timezone
c = ntplib.NTPClient()
# Provide the respective ntp server ip in below function
response = c.request('time1.google.com', version=3)
response.offset
print (datetime.fromtimestamp(response.tx_time, timezone.utc))

def decrypt(data):
    return data

def encrypt(data):
    return data

def get_id():
    if 'nt' in os.name:
        completed_process = subprocess.run('tools\\dmidecode.exe -s system-uuid'.split(), capture_output=True)
    else:
        completed_process = subprocess.run('hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid'.split(), capture_output=True)

    return  completed_process.stdout.decode(errors="ignore").strip()
