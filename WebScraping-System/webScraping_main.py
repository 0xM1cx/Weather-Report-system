import RPi.GPIO as g
import os
import webscrap_ts 
import data_to_xml
import time
from time import sleep
import multiprocessing

'''
NOTE
PLEASE DO NOT ATTEMPT TO RUN THIS PROGRAM OR YOUR SYSTEM WILL BE RUINED
'''




# Variables
mp3_file = '/home/lptechnoace/Desktop/weather/WebScraping-System/weather_condition.mp3'
xml_file = '/home/lptechnoace/Desktop/weather/WebScraping-System/webscrape.xml'
wav_file = '/home/lptechnoace/Desktop/weather/WebScraping-System/webscrape.wav'


def main_system():

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
                # play_audio = f'sudo ./pi_fm_rds -audio {wav_file}'
                play_audio = f'sox -t mp3 {mp3_file} -t wav -  | sudo ./pi_fm_rds -audio -'
                os.system(play_audio)
            
            else:
                time_elapse = time.time() - actual_time
                if time_elapse >= loop_interval:
                    # play_audio = f'sudo ./pi_fm_rds -audio {wav_file}'
                    play_audio = f'sox -t mp3 {mp3_file} -t wav -  | sudo ./pi_fm_rds -audio -'
                    os.system(play_audio)
                    actual_time = time.time()
                sleep(5)

if __name__ == "__main__":
    weather_information = multiprocessing.Process(target=data_to_xml.weather_xml_file)
    weather_condition_tts = multiprocessing.Process(target=webscrap_ts.data_to_speech, args=(xml_file,))
    main_program = multiprocessing.Process(target=main_system)

    weather_information.start()
    weather_condition_tts.start()
    main_program.start()

    weather_information.join()
    weather_condition_tts.join()
    main_program.join()

