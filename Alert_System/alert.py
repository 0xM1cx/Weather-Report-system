import requests 
import json
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
from time import sleep


'''
NOTE
Please take note that we don't recommend to run this program as per the WEATHERAPI alert is NULL.
-This program is only tested by making own dictionary of weather alert report that is base on the WEATHERAPI format. 
-If you wish to test this program, just uncomment the commented lines of the program.
-Do not change anything in the code, please contact the developer for any concern.
'''

weather_api = 'cc411f08a7b9463fbb2131058232406'
location = 'Tacloban'
xml_file = 'D:\Programming - Copy\Weather_Data_Projects\Alert_System\weather_alert.xml'


def alert_call():

    weatherapi_url = f'http://api.weatherapi.com/v1/forecast.json?key={weather_api}&q={location}&days=1&aqi=yes&alerts=yes'
    while True:
        try:
            response = requests.get(weatherapi_url)
            response.raise_for_status
            alert_information = json.loads(response.text)

            if 'alerts' in alert_information:    
                weather_information = {
                    "Alert_Kind": alert_information['alerts']['alert'][0]['event'],
                    'Covered_Area': alert_information['alerts']['alert'][0]['areas'],
                    "Severeness": alert_information['alerts']['alert'][0]['severity'],
                    "Alert_Details": alert_information['alerts']['alert'][0]['desc'],
                    "Instruction": alert_information['alerts']['alert'][0]['instruction']
                }
                print(weather_information)
                return weather_information
            
            else:
                print("No current alerts")
            sleep(5 * 60)
        except  IndexError:
            print("No current alert data")
        except requests.exceptions.RequestException as error:
            print('Error occured during fetching data:', error)

def alert_to_xml():
    while True:
        alert_information = alert_call()

        alert_data = ET.Element('Weather_Alert_Information')
        location = ET.SubElement(alert_data, 'Location')
        alert_kind = ET.SubElement(alert_data, "Alert_Kind")
        area_covered = ET.SubElement(alert_data, "Area_Covered")
        severness = ET.SubElement(alert_data, "Severeness")
        alert_details = ET.SubElement(alert_data, "Alert_Details")
        alert_instruction = ET.SubElement(alert_data, "Alert_Instrution")

        location.text = f'Tacloban City'
        alert_kind.text = f"Kind of Alert {alert_information['Alert_Kind']}"
        area_covered.text = f"Area Covered {alert_information['Covered_Area']}"
        severness.text = f"Severeness {alert_information['Severeness']}"
        alert_details.text = f"Information {alert_information['Alert_Details']}"
        alert_instruction.text = f"Instruction {alert_information['Instruction']}"


        alert_str = ET.tostring(alert_data, encoding='utf-8', xml_declaration=False)
        alert_domain = minidom.parseString(alert_str)

        alert_xml = alert_domain.toprettyxml(indent="\t", newl="\n")
        alert_xml = '\n'.join(line for line in alert_xml.split('\n') if line.strip())

        with open(xml_file, 'w') as alert_file:
            alert_file.write(alert_xml)

        sleep(5 * 60)


# if __name__ == "__main__":
#     alert_call()
