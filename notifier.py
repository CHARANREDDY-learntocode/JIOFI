import time, requests, os
from bs4 import BeautifulSoup


def _get_battery_status(soup):
        return soup.find(id='batterystatus')['value']

def _get_battery_level(soup):
    return soup.find(id='batterylevel')['value']

def notify(title, text):
    os.system("""
            osascript -e 'display notification "{}" with title "{}"'
            """.format(text, title))

def connect():
    try:
        response = requests.get('http://192.168.225.1/', timeout=3)
        soup = BeautifulSoup(response.text, features="html.parser")
        status = _get_battery_status(soup=soup)
        level = _get_battery_level(soup=soup)
        return status, int(level.replace('%', ''))
    except:
        return None, None



def check():
    while True:
        status, level = connect()
        if status == "Charging" and level >= 90 or status == "Fully Charged":
            notify('JioFi', f'Your JioFi is charged to {level}%')
        elif status == 'Discharging' and level <= 25:
            notify('JioFi', f'Charge JioFi, current battery percentage: {level}%')
            
        time.sleep(600)