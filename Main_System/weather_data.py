import requests
import json

'''
Note: This program is connected to "weather_DATA.py". To test this program, just uncomment the commented lines.
-Upon testing, the program is running as it should be. Please contact the developer if there's any error in the program. Do not attempt to change anything in the code.
'''

# accuweather_api_key = 'vvFrw5tSDxzlVmghoGcfWml9nWsQVrwZ'
# tacloban_key = '759549'

def fetch_weather(api_key, location_key):
    Accuweather_URL = f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}&details=true'

    try:
        response = requests.get(Accuweather_URL)
        response.raise_for_status()
        weather_Information = json.loads(response.text)

        weather_info = {
            "RelativeHumidity": weather_Information[0]['RelativeHumidity'],
            "Temperature": weather_Information[0]['Temperature']['Metric']['Value'],
            "Temp_Unit": weather_Information[0]['Temperature']['Metric']['Unit'],
            "Precipitation": weather_Information[0].get('Precipitation'),
            "DateAndTime": weather_Information[0]['LocalObservationDateTime']
        }
        # print(weather_info)
        return weather_info

    except requests.exceptions.RequestException as e:
        print("Error occurred while fetching weather data:", e)
 

# if __name__ == "__main__":
#     fetch_weather(accuweather_api_key, tacloban_key)