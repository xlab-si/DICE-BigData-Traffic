import requests, json

from time import sleep
from kafka import KafkaProducer

from collectors.settings import KAFKA_URL, BT_SENSORS_KAFKA_TOPIC, BT_SENSORS_LAST_URL, TIMON_USERNAME, TIMON_PASSWORD, \
    BT_SENSORS_NOT_USE

with open('data/bt_sensors.json') as data_file:
    bt_sensors_data = json.load(data_file)['data']

n = 20
while n > 0:
    sleep(2)
    try:
        response = requests.get(BT_SENSORS_LAST_URL, auth=(TIMON_USERNAME, TIMON_PASSWORD), verify='crt/datacloud.crt',
                                timeout=0.1)
        if response.status_code == 200:
            data = response.json()
            break
    except:
        n -= 1
else:
    exit()

producer = KafkaProducer(bootstrap_servers=[KAFKA_URL], value_serializer=lambda m: json.dumps(m).encode('utf-8'))

not_lj = BT_SENSORS_NOT_USE

for dist in data['data']:
    if dist['toBtId'] not in not_lj and dist['fromBtId'] not in not_lj:
        sensor_from = next(s for s in bt_sensors_data if s["btId"] == dist['fromBtId'])
        sensor_to = next(s for s in bt_sensors_data if s["btId"] == dist['toBtId'])

        dist['fromBtLng'] = sensor_from['loc']['lng']
        dist['fromBtLat'] = sensor_from['loc']['lat']
        dist['toBtLng'] = sensor_to['loc']['lng']
        dist['toBtLat'] = sensor_to['loc']['lat']
        dist['distance'] = next(s for s in sensor_from['neighbours'] if s["btId"] == dist['toBtId'])['distance']

        producer.send(BT_SENSORS_KAFKA_TOPIC, dist)
