import datetime
import platform

path = "artifact.txt"
current_date_time = datetime.datetime.now()
os_info = platform.platform()

with open(path, 'w') as artifact:
    artifact.write(f"Current date & time: {current_date_time}\n")
    artifact.write(f"OS name & version: {os_info}\n")