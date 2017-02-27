import requests
from kafka import KafkaProducer
import json

from kafka.client import KafkaClient

client = KafkaClient(bootstrap_servers=['192.168.0.62:9092'])
client.add_topic('bt_json')

producer = KafkaProducer(bootstrap_servers=['192.168.0.62:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))

n=100
while n > 0:
    try:
        response = requests.get('https://datacloud-timon.xlab.si/data_access/bt_sensors/velocities_avgs_last/',
                                auth=('username', 'password'), verify='DigiCertSHA2SecureServerCA.crt', timeout=0.1)
        if response.status_code == 200:
            data = response.json()
            break
    except:
        n -= 1
else:
    exit()

not_lj = ['BTR0219', 'BTR0218', 'BTR0217', 'BTR0213']

for dist in data['data']:
    if dist['toBtId'] not in not_lj and dist['fromBtId'] not in not_lj:
        producer.send('bt_json', dist)


