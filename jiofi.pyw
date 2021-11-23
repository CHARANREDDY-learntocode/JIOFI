import os
import rumps
from threading import Thread
from notifier import check
import requests
from bs4 import BeautifulSoup

class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__("JioFi")
        self.menu = ["Show Status"]
        thread = Thread(target = check)
        thread.start()
        self.connect()


    @rumps.clicked("Show Status")
    def prefs(self, _):
        status, level, network_status = self.connect()
        print(status, level, network_status)
        if  status is not None:
            if status == "Charging": rumps.alert('JioFi - Connected 🟢', f'Battery Status: {status} 🔋🔋\nBattery percentage:  {level}%\nConnection Status: {network_status}')
            else: rumps.alert('JioFi - Connected 🟢', f'Battery Status: {status} ⛔🔋\nBattery percentage:  {level}%\nConnection Status: {network_status}')
        else:
            rumps.alert('Jiofi - Disconnected 🔴', 'Please try connecting to JioFi.')

    @staticmethod
    def _get_battery_status(soup):
        return soup.find(id='batterystatus')['value']

    @staticmethod
    def _get_battery_level(soup):
        return soup.find(id='batterylevel')['value']
    
    @staticmethod
    def _get_network_status(soup):
        return soup.find(id='connectedStatus')['value']
    
    def connect(self):
        try:
            response = requests.get('http://192.168.225.1/', timeout=3)
            soup = BeautifulSoup(response.text, features="html.parser")
            status = self._get_battery_status(soup=soup)
            level = self._get_battery_level(soup=soup)
            network_status = self._get_network_status(soup=soup)
            return status, int(level.replace('%', '')), network_status
        except Exception as e: 
            print(e)
            return None, None, None
    

if __name__ == "__main__":
    AwesomeStatusBarApp().run()