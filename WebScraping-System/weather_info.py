from requests_html import HTMLSession
from time import sleep


'''
NOTE 
This program is different from Fetching Data It only fetch data from google weather upon running.
-Upon testing, the program is running as it should be. Please contact the developer if there's any error in the program. Do not attempt to change anything in the code.
-To test the program, just uncomment the commented line in the code.
-Comment out the "while True" condition before running code and adjust the indention of every line
'''


def webscrape_data():
    try:
        # while True:
        object = HTMLSession()

        location = 'tacloban'
        weather_url = f'https://www.google.com/search?q={location}+Weather'

        request = object.get(weather_url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'})


        location = request.html.find('div.eKPi4 span.BBwThe', first=True).text
        temperature = request.html.find('span#wob_tm', first=True).text
        humidity = request.html.find('span#wob_hm', first=True).text
        precipitation = request.html.find('span#wob_pp', first=True).text
        unit = request.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text

        weather_data =  {
            "Tac_location" : location,
            "Tac_temperature" : temperature,
            "Tac_unit" : unit,
            "Tac_humidity" : humidity,
            "Tac_precipitation" : precipitation
        }
        
        return weather_data, sleep(5 * 60)
    except:
        print("Unable to get data")
if __name__ == "__main__":
    webscrape_data()