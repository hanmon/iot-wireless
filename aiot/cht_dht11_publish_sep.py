import requests
import numpy as np
import time
import json
import configparser 

config = configparser.ConfigParser()
config.read('../ifttt.conf')
web_hook_key = config.get('web_hook_key', 'key')
event='toggle_the_plug'
apiURL = 'https://maker.ifttt.com/trigger/'+ event + '/json/with/key/'+ web_hook_key
headers = {"Content-Type": "application/json"}
v1=np.random.randint(0,100)
v2=np.random.randint(0,100)
v3=np.random.randint(0,100)
payload={"value1":str(v1), "value2":str(v2),"value3":str(v3)}
print(payload)
print(apiURL)
data=json.dumps(payload)
print(data)
response = requests.post(apiURL, data=data ,headers=headers)
print(response.text)
