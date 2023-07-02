import xml.dom.minidom as minidomain
import xml.etree.ElementTree as ET
import weather_info
from time import sleep as timer

'''
-Upon testing, the program is running as it should be. Please contact the developer if there's any error in the program. Do not attempt to change anything in the code.
-To test the program, just uncomment the commented line in the code.
-Comment out the "while True" condition before running code and adjust the indention of every line.
'''




def weather_xml_file():
    xml_path = '/home/lptechnoace/Desktop/weather/WebScraping-System/webscrape.xml'
    try:
        while True:
            weather_information = weather_info.webscrape_data()

            title = ET.Element('Weather_Information')
            location = ET.SubElement(title, 'Location')
            temp = ET.SubElement(title, 'Temperature') 
            precipitation = ET.SubElement(title, 'Precipitation')
            humidity = ET.SubElement(title, 'Humidity')

            location.text = weather_information['Tac_location']
            temp.text = f"Temperature {weather_information['Tac_temperature']} degrees"
            precipitation.text = f"Chance of Rain {weather_information['Tac_precipitation']}"
            humidity.text = f"Humidity {weather_information['Tac_humidity']}"

            tree_str = ET.tostring(title, encoding='utf-8', xml_declaration=False)
            title_domain = minidomain.parseString(tree_str)

            ind_information = title_domain.toprettyxml(indent='\t', newl='\n')
            ind_information = '\n'.join(line for line in ind_information.split('\n') if line.strip())

            with open(xml_path, 'w') as xml_file:
                xml_file.write(ind_information)
            print("Done")
            timer(5 * 60)
    except:
        print("Unable to fetch Data")

if __name__ == "__main__":
    weather_xml_file()



