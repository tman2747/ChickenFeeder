import paho.mqtt.client as mqtt
from time import sleep
import settings
from ChickenServo import ChickenServo
import subprocess

def start_pigpiod(): 
    # I was having trouble getting pidpiod to load on my pi using the service. 
    # I think adjusting to After=multi-user.target would have 
    # fixed this but this works too and currently I dont see a reason to look into it further.
    try:
        subprocess.check_output(['pgrep', 'pigpiod'])
    except subprocess.CalledProcessError:
        subprocess.run(['sudo', 'pigpiod'])
        sleep(5)

# Call the function to start pigpiod
start_pigpiod()
stop_threads = False 

mainServo = ChickenServo(17)
mainServo.servo.min()

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("test/testing")

def on_message(client, userdata, msg):
    global stop_threads # need this global to end thread
    print(msg.topic+" "+str(msg.payload))
    message = msg.payload.decode('utf-8')
    if message == "kill":
        stop_threads = True
    if message == "next":
        mainServo.dropFood()
        mainServo.printAngle()



def mqtt_client_thread():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    username = settings.usernamemqtt # if you use settings.username it actually returns the desktop users username LOL
    password = settings.password
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    broker_address = settings.dns
    port = 1883
    client.connect(broker_address, port=port, keepalive=60)
    client.loop_start()

    try:
        while not stop_threads:
            sleep(1)
    finally:
        client.loop_stop()
        client.disconnect()

mqtt_client_thread() # left over name from when I was messing with mqtt at first