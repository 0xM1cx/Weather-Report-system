import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
from weather_data import fetch_weather
from datetime import datetime 
from time import sleep

'''
Reminder!!
-Please run this program first before trying to run "text_to_speech.py"
-Uncomment the 'time' and 'time.text' if you prefer to have a current time.
-Upon testing, the program is running. Please contact the developer if there's any error in the program. Do not attempt to change anything in the code.
'''


# Actual API key - Accuweather
api_key = 'vvFrw5tSDxzlVmghoGcfWml9nWsQVrwZ'
# Tacloban API Key - Tacloban City
location_key = '759549' 

xml_File = '/home/lptechnoace/Desktop/weather/Main_System/weather_condition.xml'


def weather_data():
    while True:
        weather_info = fetch_weather(api_key, location_key)

        root_Data = ET.Element('Weather_Data')
        location = ET.SubElement(root_Data, 'Location')
        temperature  = ET.SubElement(root_Data, 'Temperature')
        precipitation_info = ET.SubElement(root_Data, 'Precipitation')
        humidity = ET.SubElement(root_Data, 'Humidity')
        # time = ET.SubElement(root_Data, 'Time')


        # time.text = f'Current Time: {datetime.now().strftime("%I:%M %p")}'
        temperature.text = f"Temperature: {str(weather_info['Temperature'])} degrees"
        precipitation = weather_info['Precipitation']
        location.text = "Tacloban City"
        humidity.text = f"Humidity: {str(weather_info['RelativeHumidity'])} percent"
        
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
        print("Done!")
        sleep(300) 

if __name__ == "__main__":
    weather_data()