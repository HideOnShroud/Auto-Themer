import subprocess
import time
import schedule
import sys
from suntime import Sun


# switch = 'auto' for sunrise/sunset. switch = 'custom' for custom
switch = 'auto'

# Input your location
latitude = 41.7151
longitude = 44.8271
sun = Sun(latitude, longitude)


def sunrise():

    if switch == 'auto':
        return sun.get_local_sunrise_time().hour
    else:
        return 9  # Desired timme ONLY HOUR


def sunset():

    if switch == 'auto':
        return sun.get_local_sunset_time().hour
    else:
        return 18  # Desired timme ONLY HOUR


def get_file_path():

    #\x5c == \
    return sys.path[0]+"\x5c"+"auto_themer.pyw"


def day_or_night():

    # Change sunset() and sunrise() into integers for static time.
    if time.localtime().tm_hour >= sunset() or time.localtime().tm_hour <= sunrise():
        return '0'
    else:
        return '1'


# Rainmeter option
def rainmeter_skin():

    if day_or_night() == '0':
        return 'Full'  # Layout name
    else:
        return 'LM1'  # Layout name


def job():

    command = ['reg.exe', 'add', 'HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize', '/v',
               'AppsUseLightTheme', '/t', 'REG_DWORD', '/d', day_or_night(), '/f']

    command2 = ['reg.exe', 'add', 'HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize', '/v',
                'SystemUsesLightTheme', '/t', 'REG_DWORD', '/d', day_or_night(), '/f']

    command3 = ["C:\Program Files\Rainmeter\Rainmeter.exe", "!LoadLayout", rainmeter_skin()]  # Rainmeter Option

    command4 = ['reg.exe', 'add', 'HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run', '/v', 'Auto_themer', '/t',
                'REG_SZ', '/d', get_file_path(), '/f']
    
    subprocess.run(command)
    subprocess.run(command2)
    subprocess.call(command3)  # Rainmeter option
    subprocess.call(command4)


def main():

    job()
    schedule.every().day.at(f"0{sunrise()}:00").do(job)
    schedule.every().day.at(f"{sunset()}:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
