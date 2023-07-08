import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import requests, json, os, time
import RPi.GPIO as g
from gtts import gTTS
from time import sleep
from datetime import datetime 
''''
Tacloban City
Temperature: 69 degrees
Chance of rain: 69%
Humidity: 69%
'''

class weather: 
    '''Initializing'''
    def __init__(self, api_location, api_key):
        self.location = api_location
        self.key = api_key
        self.accuweather_url = requests.get('http://api.weatherapi.com/v1/forecast.json?key={}&q={}&days=1&aqi=yes&alerts=yes'.format(self.key, self.location))
        self.accuweather_url.raise_for_status
        self.weather_response = json.loads(self.accuweather_url.text)
    
    def weather_data(self):
        '''Getting some information on WeatherAPI as Dicktionary'''
        self.weather_information = {
            "Location" : self.weather_response['location']['name'],
            "Temperature" : '{} degrees'.format(self.weather_response['current']['temp_c']),
            "Humidity" : '{} percent'.format(self.weather_response['current']['humidity']),
            "Precipitation" : '{} percent'.format(self.weather_response['forecast']['forecastday'][0]['day']['daily_chance_of_rain'])

        }   
        return self.weather_information

    def xml_data(self): 
        #Weather_Data an root ng xml file
        self.xml_title = ET.Element('Weather_Data')

        for keys, values in self.weather_data().items():
            element = ET.SubElement(self.xml_title, keys) #Yung keys po ung mga subelement sa xml file
            element.text = str(values) # tapos adi an content ng bawat subelemet

        '''Don't mind this line, gin seset la ini para tanggapin sa xml file'''
        self.file_tree = ET.tostring(self.xml_title, encoding='utf-8', xml_declaration=False)
        self.file_tree_domain = minidom.parseString(self.file_tree)
        '''Adi nag seset ng indention para maayos tingnan'''
        self.weather_report = self.file_tree_domain.toprettyxml(indent='\t', newl='\n')
        self.weather_report = '\n'.join(line for line in self.weather_report.split('\n') if line.strip())

        '''Tapos adi ginsasave ha xml file an mga weather information'''
        with open('weather_report.xml', 'w') as report_xml:
            report_xml.write(self.weather_report)
    
    def xml_speech(self):
        self.xml_data() #gin call la an xml_data() method


        self.weather_Condition = ET.fromstring(self.file_tree)
        weather_mp3 = '' #Empty String la ini

        '''loop adi para ipasok sa ung bawat laman ng xml file into the weather_mp3 variable'''
        for element in self.weather_Condition.iter(): 
            if element.text is not None: #nag condition po ako ng Not None para ma skip an root
                weather_mp3 += '{}, {}, \n'.format(element.tag, element.text) 

        '''gin Save la an mp3'''
        speech_mp3 = gTTS(text=weather_mp3, lang='en')
        speech_mp3.save('weather.mp3')

class weather_alert(weather):
    def __init__(self, api_key, location_key):
        super().__init__(api_key, location_key)

    def alerts(self):
        if 'alerts' in self.weather_response:
            alert_information = {
                    "Alert_Kind": self.weather_response['alerts']['alert'][0]['event'],
                    'Covered_Area': self.weather_response['alerts']['alert'][0]['areas'],
                    "Severeness": self.weather_response['alerts']['alert'][0]['severity'],
                    "Alert_Details": self.weather_response['alerts']['alert'][0]['desc'],
                    "Instruction": self.weather_response['alerts']['alert'][0]['instruction']
                }
        return alert_information

    def alert_data(self): 
        #Weather_Data an root ng xml file
        self.xmlalert_title = ET.Element('Weather_Data')

        if self.alerts() is not None:
            for keys, values in self.alerts().items():
                alert = ET.SubElement(self.xmlalert_title, keys) #Yung keys po ung mga subelement sa xml file
                alert.text = str(values) # tapos adi an content ng bawat subelemet

        '''Don't mind this line, gin seset la ini para tanggapin sa xml file'''
        self.alert_tree = ET.tostring(self.xmlalert_title, encoding='utf-8', xml_declaration=False)
        self.alert_tree_domain = minidom.parseString(self.alert_tree)
        '''Adi nag seset ng indention para maayos tingnan'''
        self.alert_report = self.alert_tree_domain.toprettyxml(indent='\t', newl='\n')
        self.alert_report = '\n'.join(line for line in self.alert_report.split('\n') if line.strip())

        '''Tapos adi ginsasave ha xml file an mga weather information'''
        with open('weather_alert.xml', 'w') as alert_xml:
            alert_xml.write(self.alert_report)
    
    def alert_speech(self):
        self.alert_data() #gin call la an xml_data() method

        self.alert_Condition = ET.fromstring(self.file_tree)
        weather_alert_mp3 = '' #Empty String la ini

        '''loop adi para ipasok sa ung bawat laman ng xml file into the weather_mp3 variable'''
        for alert in self.alert_Condition.iter(): 
            if alert.text is not None: #nag condition po ako ng Not None para ma skip an root
                weather_alert_mp3 += '{}, {}, \n'.format(alert.tag, alert.text) 

        '''gin Save la an mp3'''
        speech_mp3 = gTTS(text=weather_alert_mp3, lang='en')
        speech_mp3.save('alert.mp3')
        os.system('alert.mp3')

class time_check:
    def __init__(self):
        self.time()

    def time(self):
        time = str(datetime.now().strftime("%I:%M %p"))
        time_mp3 = gTTS(text=time, lang='en')
        time_mp3.save('time.mp3')
        os.system('time.mp3')

#Adi an mga Class Objects
data = weather('Tacloban City', 'cc411f08a7b9463fbb2131058232406')
alert = weather_alert('Tacloban City', 'cc411f08a7b9463fbb2131058232406')
        
if __name__ == "__main__":
    '''Adi an tikang sa dtmf.py'''
    GPIO_D0  = 5
    GPIO_D1  = 6
    GPIO_D2  = 13
    GPIO_D3  = 19
    GPIO_StQ = 26   
    
    g.setmode(g.BCM)
    g.setwarnings(False)
    
    #nag set lang ak ng interval time
    actual_time = time.time()
    loop_interval = 30 * 60

    #infinite po magrurun ung program once na ma run an file
    while True:

        sleep(0.1) # standaard warde is 0.1 sec
        g.setup(GPIO_D0, g.IN)
        g.setup(GPIO_D1, g.IN)
        g.setup(GPIO_D2, g.IN)
        g.setup(GPIO_D3, g.IN)
        g.setup(GPIO_StQ, g.IN)

        D0 = g.input(GPIO_D0)
        D1 = g.input(GPIO_D1)
        D2 = g.input(GPIO_D2)
        D3 = g.input(GPIO_D3)
        StQ= g.input(GPIO_StQ)
        
        if StQ == True:
            # Check for DTMF tone input
            key_tone_received = str(D0+D1+D2+D3)

            '''adi an para ha input ng DTMF'''
            if key_tone_received == str(1000):
                data.xml_speech() #if 1 an pinindot, magrurun an weather forecast
            else:
                time_elapse = time.time() - actual_time
                if time_elapse >= loop_interval:
                    data.xml_speech()
                    actual_time = time.time() #every 30 minutes magrurun an system
                sleep(1)
            if key_tone_received == '0100':
                data = time_check().time #if 2 namn po an pinindot, gagana an time check. Time lang po yan di kasama ung month and day
    
        #mag rurun la adi if may alerts na
        if alert.alerts() is not None:
            alert.alert_speech
