#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import requests
import json
import warnings
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# Now, to clear the screen
cls()
# --- MQTT Configuration ---

print("hello")

MQTT_PORT = 1883  # Default MQTT port

# Load configuration from config.yaml
with open("/data/options.json", "r") as config_file:
    config = json.load(config_file)

MQTT_BROKER = config.get("MQTT_BROKER")
MQTT_TOPIC = config.get("MQTT_TOPIC")
MQTT_USERNAME = config.get("MQTT_USERNAME")
MQTT_PASSWORD = config.get("MQTT_PASSWORD")

print("this is the IP " + MQTT_BROKER)
print("this is the Topic " + MQTT_TOPIC)
print("this is the USer " + MQTT_USERNAME)
print("this is the Pass " + MQTT_PASSWORD)

warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning) 

# Function to update the traffic route
def update_traffic_route(message):
    headers = {
        'Host': '192.168.1.1',
        # 'Content-Length': '86',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Ch-Ua': '"Chromium";v="129", "Not=A?Brand";v="8"',
        'Content-Type': 'application/json',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36',
        'Accept': '*/*',
        'Origin': 'https://192.168.1.1',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Priority': 'u=1, i',
    }

    json_data = {
        'username': 'APITest',
        'password': 'hYrDeaRfARY4K6eBiLev',
        'token': '',
        'rememberMe': False,
    }

    response = requests.post('https://192.168.1.1/api/auth/login', headers=headers, json=json_data, verify=False)

    responseJSON = response.json()

    #print(response.headers)

    device_token = responseJSON['deviceToken']
    XCSRF_Token = response.headers['X-CSRF-Token']

    #print(XCSRF_Token)
    #print(XCSRF_Token)

    #print(response.cookies)

    #  `response` holds your response object
    cookies = response.cookies

    # Get the TOKEN cookie value
    token_value = cookies.get("TOKEN")

    #print(token_value)

    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.
    #data = '{"username":"APITest","password":"hYrDeaRfARY4K6eBiLev","token":"","rememberMe":false}'


    url = "https://192.168.1.1/proxy/network/v2/api/site/default/trafficroutes/672d66d5c1ea4153e100edca"

    payload = json.dumps({
     "_id": "672d66d5c1ea4153e100edca",
     "description": "TV to Parsippany",
     "domains": [],
     "enabled": message,  # Use the 'enabled' value from MQTT
     "ip_addresses": [],
     "ip_ranges": [],
     "kill_switch_enabled": True,
     "matching_target": "INTERNET",
     "network_id": "672d64c3c1ea4153e100ed66",
     "next_hop": "",
     "regions": [],
     "target_devices": [
      {
       "client_mac": "34:51:80:61:94:7b",
       "type": "CLIENT"
      },
      {
       "client_mac": "34:5e:08:4d:4a:13",
       "type": "CLIENT"
      },
      {
       "client_mac": "c4:98:5c:99:77:c0",
       "type": "CLIENT"
      },
      {
       "client_mac": "84:ea:ed:88:a5:cb",
       "type": "CLIENT"
      },
      {
       "client_mac": "44:07:0b:4f:f8:fd",
       "type": "CLIENT"
      }
     ],
     "isAllTab": True,
     "interfaceName": "Parsippany",
     "isLocalNetwork": False
    })
    headers2 = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
     'Accept': 'application/json, text/plain, */*',
     'Accept-Language': 'en-US,en;q=0.5',
     'Accept-Encoding': 'gzip, deflate, br, zstd',
     'Origin': 'https://192.168.1.1',
     'Connection': 'keep-alive',
     'Cookie': f'TOKEN={token_value}',
     'Sec-Fetch-Dest': 'empty',
     'Sec-Fetch-Mode': 'no-cors',
     'Sec-Fetch-Site': 'same-origin',
     'TE': 'trailers',
     'Content-Type': 'application/json',
     'X-CSRF-Token': f'{XCSRF_Token}',
     'Priority': 'u=0',
     'Pragma': 'no-cache',
     'Cache-Control': 'no-cache',
     'Authorization': f'Bearer {device_token}'
    }
    #print(headers2)
    requests.request("PUT", url, headers=headers2, data=payload, verify=False)
    print("Unifi Changed")
    #print(response2)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        message = msg.payload.decode()
        print(f"Received message: {message}, Setting enabled to: {message}")
        update_traffic_route(message)
    except Exception as e:
        print(f"Error processing message: {e}")


client = mqtt.Client(protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD) 
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()