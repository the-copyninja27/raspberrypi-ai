from gpiozero import Button
from signal import pause
import os
from RPLCD.i2c import CharLCD
import time
import picamera
import requests
from RPLCD.i2c import CharLCD
from gpiozero import Button
import time
import os
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('twillio_account_sid')
auth_token = os.getenv('twillio_auth_token')
client = Client(account_sid, auth_token)


def send_message(message, message_from='+12762125643', message_to='+919952773994'):
    message = client.messages.create(
        body=message,
        from_=message_from,
        to=message_to
    )
    print(message.sid)


flag = 1


if flag:
    lcd = CharLCD('PCF8574', 0x27)
    lcd.clear()
    lcd.write_string("Script Running")
    time.sleep(3)
    flag = 0
    lcd.clear()


ctr = 1

def display_message(top, bottom=False, count=3):
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

def capture_and_process_image():
    camera = picamera.PiCamera()
    try:
        img_id = len(os.listdir('/home/cotton/Desktop/project/imgs')) + 1
        img_path = f"/home/cotton/Desktop/project/imgs/{img_id}.jpg"
        display_message("Photo capturing")
        camera.capture(img_path)
        time.sleep(1)
        with open(img_path, 'rb') as file:
            url = "https://plantsmbbs.azurewebsites.net/api/pythodoc"
            files = {'crop_image': file}
            display_message("Processing Image", count=7)
            response = requests.post(url, files=files)
            name, disease = str(response.text).split("___")
            display_message("", disease)
            
            if "healthy" in disease.lower():
                send_message("Plant is healthy")
            else:
                send_message(f"Plant diagnosed with {disease}")
    
    except Exception as e:
        print(e)
    
    finally:
        camera.close()

def on_press():
    global ctr
    print(f"Button was pressed - {ctr}")
    capture_and_process_image()
    ctr += 1


button = Button(26)
button.when_pressed = on_press

pause()
