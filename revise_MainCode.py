import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import requests
import json, itertools
import os
import RPi.GPIO as GPIO
import datetime
from gtts import gTTS
from requests_html import HTMLSession
from time import sleep


class WeatherForecast:
    def __init__(self, api_Location, api_Key):
        self.location = api_Location
        self.apiKey = api_Key

    def load_JSONResponse(self):
        weatherAPI_URL = requests.get('http://api.weatherapi.com/v1/forecast.json?key={}&q={}&days=1&aqi=yes&alerts=yes'.format(self.apiKey, self.location))
        weatherAPI_URL.raise_for_status
        weatherAPI_Response = json.loads(weatherAPI_URL.text)

        return weatherAPI_Response

    def weatherForecast_Dict(self):
        try: 
            weatherResponse = self.load_JSONResponse()
            weatherInformation = {
                "Today-is": "{}".format(str(datetime.datetime.now().strftime("%B %d %Y. The time is %I:%M %p"))),
                "Weather-Report-in": "{}".format(weatherResponse['location']['name']),
                "Temperature": '{} degrees'.format(weatherResponse['current']['temp_c']),
                "Humidity": '{}%'.format(weatherResponse['current']['humidity']),
                "Chance-Of-Rain": '{}%'.format(weatherResponse['forecast']['forecastday'][0]['day']['daily_chance_of_rain'])
                }
            return weatherInformation
        
        except Exception as error:
            print(f"An error occur {error}")
    
    def weatherInformation_to_XML(self):
        weatherInformation = self.weatherForecast_Dict()

        XML_title = ET.Element('Weather-Data')
        for keys, values in weatherInformation.items():
            elementTag = ET.SubElement(XML_title, keys)
            elementTag.text = str(values)

        XMLTree = ET.tostring(XML_title, encoding='utf-8')
        XMLDomain = (minidom.parseString(XMLTree)).toprettyxml(indent='\t', newl='\n')
        with open('weatherInformation.xml', 'w') as weatherReport:
            weatherReport.write(XMLDomain)
        
        return XMLDomain

    def weatherInformation_to_Audio(self):
        weatherInformation = self.weatherInformation_to_XML()

        weatherReport = ET.fromstring(weatherInformation)
        weatherText = ''

        for elements in weatherReport.iter():
            if elements.text is not None:
                weatherText += '{}, {}, '.format(elements.tag, elements.text)

        todayForecast = gTTS(text=weatherText, lang='en')
        todayForecast.save('weatherInformation.mp3')
        os.system('nvlc weatherInformation.mp3')


class weatherTyphoonAlert:
    def __init__(self, webURL):
        self.url = webURL
        self.alertReport = []
        self.forecastReport = []
        #For Wind signals
        self.typhoonAdvisory = {}
        self.areas = []
        self.LuzVisMin = []
        #Combinations 
        self.affectedAreas = []
        self.newPairs_of_AffectedAreas = []
    
    def requestTyphoonInformation(self):

        session = HTMLSession()
        requestWeatherReport = session.get(self.url, headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}, verify=False)
        requestWeatherReport.raise_for_status()

        return requestWeatherReport
    
    def typhoonInformation(self):
        request = self.requestTyphoonInformation()

        try:
            if request:
                #For Conditionals variables
                windSignal = request.html.find('table.table tbody tr td ul li strong', first=True)
                noWindSignal = request.html.find('.panel-body span', first=True)

                #Elements that are in list[]
                typhoonInfo = request.html.find('.panel-body p') #Position, Movement, Location of the center/eye
                typhoonForecast = request.html.find('.panel-body li') #Forecast Position
                warningSignals = request.html.find('table.table thead th') #Warning Signals
                locations = request.html.find('table.table tbody tr td ul li ul li') #Cities and Provinces
                locationsIsland = request.html.find('table.table tbody tr td ul li strong') #Luzon,Visayas, Mindanao
                signal_no = len(warningSignals)

                # For Loops of every list including wind signals
                for content in typhoonInfo:
                    self.alertReport.append(content.text.replace("°", " degrees "))

                for forecast in typhoonForecast:
                    self.forecastReport.append(forecast.text.replace("°", " degrees "))
                
                for islands in locationsIsland:
                    self.LuzVisMin.append(islands.text)

                for area in locations:
                    if area.text == '-':
                        self.areas.append(area.text.replace('-', 'No Tropical Cyclone Wind signal'))
                    else:
                        self.areas.append(area.text.replace('ñ', 'n').replace("'", ' '))

                for islands, provinces in itertools.zip_longest(self.LuzVisMin, self.areas, fillvalue=None):
                    self.affectedAreas.append([f"{islands}, {provinces}"])

                for pairs in range(0, len(self.affectedAreas), 3):
                    subList = self.affectedAreas[pairs:pairs + 3]
                    self.newPairs_of_AffectedAreas.append(subList)

                for windSignals, affectedAreas in itertools.zip_longest(warningSignals, self.newPairs_of_AffectedAreas, fillvalue=[]):
                    combined_warnings_with_places = [item for sublist in affectedAreas for item in sublist]
                    self.typhoonAdvisory[f"{windSignals.text.replace('no.', 'number')} {signal_no}"]  = combined_warnings_with_places
                    signal_no -= 1


                if noWindSignal:
                    typhoonInformation = {
                        'Typhoon-Name': request.html.find('div.tab-content h3', first=True).text,
                        'Issued': request.html.find('div.row h5', first=True).text,
                        'Location-of-eye': self.alertReport[0],
                        'Movement': self.alertReport[1],
                        'Strength': self.alertReport[2],
                        'Wind-Signals': request.html.find('.panel-body span', first=True).text,
                        'Forecast-Position': f'{self.forecastReport[0]}, {self.forecastReport[1]}, {self.forecastReport[2]}'
                    }
                    return typhoonInformation

                elif windSignal:
                    typhoonInformation = {
                        'Typhoon-Name': request.html.find('div.tab-content h3', first=True).text,
                        'Issued': request.html.find('div.row h5', first=True).text,
                        'Location-of-eye': self.alertReport[0],
                        'Movement': self.alertReport[1],
                        'Strength': self.alertReport[2],
                        'Wind-Signal': self.typhoonAdvisory,
                        'Forecast-Position': f'{self.forecastReport[0]}, {self.forecastReport[1]}, {self.forecastReport[2]}'
                    }
                    return typhoonInformation
                else:
                    pass
        except Exception as e:
            print(e)
            return None
        
    def typhoonAlert_to_xml(self):
        typhoonInformation = self.typhoonInformation()
        alertTitle = ET.Element('Alert-Information')
        
        if typhoonInformation is not None:
            for keys, values in typhoonInformation.items():
                alertTag = ET.SubElement(alertTitle, keys)
                alertTag.text = str(values)
        else:
            alertTag = ET.SubElement(alertTitle, 'Alert-Report')
            alertTag.text = "No Active Tropical Cyclone inside the Philippine Area of Responsibilities"

        alertTree = ET.tostring(alertTitle, encoding='utf-8')
        alertDomain = (minidom.parseString(alertTree)).toprettyxml(indent='\t', newl='\n')

        with open('typhoonAlert.xml', 'w') as typhoonFile:
            typhoonFile.write(alertDomain)

    def typhoonXML_to_Audio(self):
        self.typhoonAlert_to_xml()
        #If the time is 11:15am | 5:15pm | 11:15pm | 5:15am, the line under this comment will run.
        if weatherAlert.typhoonInformation() is not None:
            typhoonXMLInformation = ET.parse('typhoonAlert.xml')
            typhoonXMLData = typhoonXMLInformation.getroot()
            typhoonMP3 = ''

            for elements in typhoonXMLData.iter():
                if elements.text is not None:
                    typhoonMP3 += '{}, {}, '.format(elements.tag, elements.text.replace('{', '').replace('}', '').replace('[', '').replace(']', ''))
        else:
            typhoonXMLInformation = ET.parse('typhoonAlert.xml')
            typhoonXMLData = typhoonXMLInformation.getroot()
            typhoonMP3 = ''

            for elements in typhoonXMLData.iter():
                if elements.text is not None:
                    typhoonMP3 += '{}, {}, '.format(elements.tag, elements.text)
        
            typhoonForecast = gTTS(text=typhoonMP3, lang='en')
            typhoonForecast.save('alertInformation.mp3')
            os.system('nvlc alertInformation.mp3')

def currrentTime():
    current_time = str(datetime.datetime.now().strftime("Today is %B %d %Y. The time is %I:%M %p"))
    time_MP3 = gTTS(text=current_time, lang='en')
    time_MP3.save('currentTime.mp3')
    os.system('nvlc currrentTime.mp3')

def intervalTime():
    currentMinute = datetime.datetime.now().minute
    currentSeconds = datetime.datetime.now().second

    calcRemainingMinute = 30 - ((currentMinute + 1) % 30)
    calcRemainingSeconds = 60 - currentSeconds

    if calcRemainingMinute == 0 and calcRemainingSeconds < 60:
        calcRemainingMinute = 30
    
    totalRemainingTime = (calcRemainingMinute * 60) + calcRemainingSeconds
    sleep(totalRemainingTime)

def checkCurrentTime():
    time = datetime.datetime.now().time()
    currentHour = time.hour
    currentMinute = time.minute
    currentTime = int(f'{currentHour}{currentMinute}')
    return currentTime

weatherForecast = WeatherForecast('Tacloban City', 'cc411f08a7b9463fbb2131058232406')
weatherAlert = weatherTyphoonAlert('https://bagong.pagasa.dost.gov.ph/tropical-cyclone/severe-weather-bulletin')

if __name__ == "__main__":
    GPIO_D0 = 5
    GPIO_D1 = 6
    GPIO_D2 = 13
    GPIO_D3 = 19
    GPIO_StQ = 26

    # GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    while True:        
        # Button debounce time (in seconds)
        DEBOUNCE_TIME = 0.2

        # Set up GPIO pins
        GPIO.setup(GPIO_D0, GPIO.IN)
        GPIO.setup(GPIO_D1, GPIO.IN)
        GPIO.setup(GPIO_D2, GPIO.IN)
        GPIO.setup(GPIO_D3, GPIO.IN)
        GPIO.setup(GPIO_StQ, GPIO.IN)

        def button_pressed(channel):
            # Add your button press logic here
            key_tone_received = GPIO.input(GPIO_D0) + (GPIO.input(GPIO_D1) * 2) + (GPIO.input(GPIO_D2) * 4) + (GPIO.input(GPIO_D3) * 8)
            if key_tone_received == 1:
                weatherForecast.weatherInformation_to_Audio()  # Play weather forecast
            elif key_tone_received == 2:
                currrentTime()  # Display current time
            elif key_tone_received == 3:
                weatherAlert.typhoonXML_to_Audio() #Play Alert Information

        # event detection for StQ pin
        GPIO.add_event_detect(GPIO_StQ, GPIO.RISING, callback=button_pressed, bouncetime=int(DEBOUNCE_TIME * 1000))

        # try-finally block for proper GPIO cleanup
        try:
            while True:
                try:
                    if weatherAlert.typhoonInformation() is not None:
                        intervalTime()
                        weatherAlert.typhoonXML_to_Audio()
                        weatherForecast.weatherInformation_to_Audio()
                    else:
                        intervalTime()
                        weatherForecast.weatherInformation_to_Audio()
                except:
                    intervalTime()
                    weatherForecast.weatherInformation_to_Audio()
        finally:
            GPIO.cleanup()
