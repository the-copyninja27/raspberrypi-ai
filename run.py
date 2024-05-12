import picamera
import requests
from RPLCD.i2c import CharLCD
import time
import os
from sms import send_message

camera = picamera.PiCamera()



def display_message(top,bottom=False,count=3):
    lcd = CharLCD('PCF8574', 0x27)
    lcd.clear()
    lcd.write_string(top)
    lcd.crlf()
    if bottom:
        lcd.write_string(bottom)
    else:
        for i in range(count):
            lcd.write_string(f"Loading {'.' * i}")
            time.sleep(0.5)
            lcd.cursor_pos = (1, 0)
            lcd.write_string(" " * 16)
            lcd.cursor_pos = (1, 0)


try:
    img_id = len(os.listdir('imgs'))+1
    img_path = f"imgs/{img_id}.jpg"
    display_message("Photo capturing")
    camera.capture(img_path)
    camera.close()
    time.sleep(1)
    with open(img_path,'rb') as file:
        url = "https://plantsmbbs.azurewebsites.net/api/pythodoc"
        img_abs_path = f'/home/cotton/Desktop/project/imgs/{img_id}.jpg'
        files = {'crop_image': open(img_abs_path, 'rb')}
        display_message("Processing Image",count=7)
        response = requests.post(url,headers={},files=files)
        print(response.text)
        name , disease = str(response.text).split("___")
        print("",disease)
        display_message("",disease)
        if disease.lower() in "healthy":
            send_message("Plant is healthy")
        else:
            send_message(f"Plant diagnosed with {disease}")
except Exception as e:
    print(e)
finally:
    camera.close()
