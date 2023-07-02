import xml.etree.ElementTree as ET
from gtts import gTTS
from time import sleep

'''
NOTE 
Please do not attempt to run this code.
'''



def alert_wav(file):
    while True:
        sleep(5)
        alert_content = ET.parse(file)
        data_root = alert_content.getroot()

        location = data_root.find('Location').text
        alert_kind  = data_root.find('Alert_Kind').text
        area_covered = data_root.find('Area_Covered').text
        severness = data_root.find('Severeness').text
        alert_details = data_root.find('Alert_Details').text
        alert_instruction = data_root.find('Alert_Instrution').text

        alert_information = f'Location {location}, {alert_kind}, {area_covered}, {severness}, {alert_details}, {alert_instruction}'

        audio = gTTS(text=alert_information, lang='en')

        audio.save('alert_information.mp3')


