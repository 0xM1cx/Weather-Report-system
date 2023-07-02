import RPi.GPIO as g
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import multiprocessing
import time, os
import text_to_Speech
from weather_data import fetch_weather
from time import sleep

'''
NOTE
PLEASE DO NOT ATTEMPT TO RUN THIS PROGRAM OR YOUR SYSTEM WILL BE RUINED
'''


# Actual API key - Accuweather
api_key = 'vvFrw5tSDxzlVmghoGcfWml9nWsQVrwZ'
# Tacloban API Key - Tacloban City
location_key = '759549' 

audio_File = '/home/lptechnoace/Desktop/weather/Main_System/weather_condition.mp3'
xml_File = '/home/lptechnoace/Desktop/weather/Main_System/weather_condition.xml'

def weather_data():
    while True:
        weather_info = fetch_weather(api_key, location_key)

        root_Data = ET.Element('Weather_Data')
        location = ET.SubElement(root_Data, 'Location')
        temperature  = ET.SubElement(root_Data, 'Temperature')
        precipitation_info = ET.SubElement(root_Data, 'Precipitation')
        humidity = ET.SubElement(root_Data, 'Humidity')

        temperature.text = f"Temperature: {str(weather_info['Temperature'])} degrees"
        
        precipitation = weather_info['Precipitation']
        location.text = "Tacloban City"
        humidity.text = f"Humidity: {str(weather_info['RelativeHumidity'])} percent"
        # precipitation.text = str(weather_info['Precipitation'])
        
        if precipitation is not None:
            if 'Metric' in precipitation and 'Value' in precipitation['Metric']:
                precipitation_value = precipitation['Metric']['Value']
                precipitation_info.text = str(f': {precipitation_value}')

                if 'Probability' in precipitation:
                    precipitation_probability = precipitation['Probability']
                    precipitation_info.text = str(f'Precipitation: {precipitation_probability} percent')
            else:
                precipitation_info.text = str('Precipitation information not available')
        else:
            precipitation_info.text = str("Chance of Rain: No chance of rain")


        # Data_Tree = ET.ElementTree(root_Data)
        Data_treeStr = ET.tostring(root_Data, encoding='utf-8', xml_declaration=False)
        Dom = minidom.parseString(Data_treeStr)

        indented_Data = Dom.toprettyxml(indent="\t", newl="\n")
        indented_Data = '\n'.join(line for line in indented_Data.split('\n') if line.strip())


        with open(xml_File, 'w', encoding="utf-8") as File:
            File.write(indented_Data)
        sleep(300)

def main():

    # Set up DTMF inputs using gpiozero
    GPIO_D0 = 5
    GPIO_D1 = 6
    GPIO_D2 = 13
    GPIO_D3 = 19
    GPIO_StQ = 26

    g.setmode(g.BCM)
    g.setwarnings(False)

    actual_time = time.time()
    loop_interval = 30 * 60

    # Main loop
    while True:
        sleep(0.1)

        g.setup(GPIO_D0, g.IN)
        g.setup(GPIO_D1, g.IN)
        g.setup(GPIO_D2, g.IN)
        g.setup(GPIO_D3, g.IN)
        g.setup(GPIO_StQ, g.IN)
        
        
        D0 = g.input(GPIO_D0)
        D1 = g.input(GPIO_D1)
        D2 = g.input(GPIO_D2)
        D3 = g.input(GPIO_D3)
        StQ = g.input(GPIO_StQ)
        if StQ == True:
            # Check for DTMF tone input
            key_tone_received = D0+D1+D2+D3

            # Check if the DTMF tone corresponding to number 1 is received
            if key_tone_received == '1':  # Adjust the condition based on your DTMF decoder's logic
                # Play the weather update audio file
                play_audio = f'sox -t mp3 {audio_File} -t wav -  | sudo ./pi_fm_rds -audio -'
                os.system(play_audio)  # Wait until the audio finishes playing
            else:
                time_elapse = time.time() - actual_time
                if time_elapse >= loop_interval:
                    play_audio = f'sox -t mp3 {audio_File} -t wav -  | sudo ./pi_fm_rds -audio -'
                    os.system(play_audio)
                    actual_time = time.time()
                sleep(1)

if __name__ == "__main__":
    weather_condition = multiprocessing.Process(target=weather_data)
    data_to_speech = multiprocessing.Process(target=text_to_Speech.data_to_speech, args=(xml_File,))
    main_system = multiprocessing.Process(target=main)

    weather_condition.start()
    data_to_speech.start()
    main_system.start()

    weather_condition.join()
    data_to_speech.join()
    main_system.join()
