import xml.etree.ElementTree as ET
from time import sleep
from gtts import gTTS

'''
-Upon testing, the program is running as it should be. Please contact the developer if there's any error in the program. Do not attempt to change anything in the code.
-To test the program, just uncomment the commented line in the code.
-Comment out the "while True" condition before running code and adjust the indention of every line
'''


xml_path = '/home/lptechnoace/Desktop/weather/WebScraping-System/webscrape.xml'

def data_to_speech(file):
    try: 
        while True:
            audio_path = '/home/lptechnoace/Desktop/weather/WebScraping-System/weather_condition.mp3'

            tree = ET.parse(file)
            root = tree.getroot()

            humidity = root.find('Humidity').text
            location = root.find('Location').text
            temperature = root.find('Temperature').text
            Precipitation = root.find('Precipitation').text

            weather_Condition = f'Location: {location}, {temperature}, {Precipitation}, {humidity}'

            tts = gTTS(text=weather_Condition, lang='en')
            tts.save(audio_path)
            sleep(5 * 60)
    except:
        print("Unable to fetch data")
# if __name__ == "__main__":
#     data_to_speech(xml_path)