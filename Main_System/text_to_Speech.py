from time import sleep
from gtts import gTTS
import xml.etree.ElementTree as ET

'''
Reminder!!!!
- Before running this program, please run filename "weather-data.py" first.
- After that, uncomment the commented file. Please ensure that "weather_condition.xml" has a content or you may encounter errors.
'''


# file_path = '/home/lptechnoace/Desktop/weather/Main_System/weather_condition.xml'

def data_to_speech(file):
    audio_location = '/home/lptechnoace/Desktop/weather/Main_System/weather_condition.mp3'
    
    # while True:
    sleep(1)
    tree = ET.parse(file)
    root = tree.getroot()
    
    humidity = root.find('Humidity').text
    location = root.find('Location').text
    temperature = root.find('Temperature').text
    precipitation = root.find('Precipitation').text
    
    weather_Condition = f'Location: {location}, {temperature}, {precipitation}, {humidity}'
    
    weather_to_speech = gTTS(text=weather_Condition, lang='en')
    weather_to_speech.save(audio_location)
    print('done!')

# if __name__ == "__main__":
#     data_to_speech(file_path)