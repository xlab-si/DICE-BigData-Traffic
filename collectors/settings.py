import os

# Apache Kafka settings
KAFKA_HOST = 'host'
KAFKA_PORT = 'port'

# Bluetooth sensors
BT_SENSORS_LAST_URL = 'https://datacloud-timon.xlab.si/data_access/bt_sensors/velocities_avgs_last/'
BT_SENSORS_URL = 'https://datacloud-timon.xlab.si/data_access/bt_sensors/sensors/'
TIMON_USERNAME = 'username'
TIMON_PASSWORD = 'password'
BT_SENSORS_NOT_USE = ['BTR0219', 'BTR0218', 'BTR0217', 'BTR0213']
BT_SENSORS_KAFKA_TOPIC = 'bt_json'

# Traffic counters
COUNTERS_URL = 'https://opendata.si/promet/counters/'
COUNTERS_KAFKA_TOPIC = 'counter_json'

# Inductive loops
INDUCTIVE_LOOPS_HOST = '10.30.1.132'
INDUCTIVE_LOOPS_PORT = 9200
INDUCTIVE_LOOPS_KAFKA_TOPIC = 'inductive_json'

# LPP traffic
LPP_STATION_URL = 'http://194.33.12.24/stations/getRoutesOnStation'
LPP_STATION_KAFKA_TOPIC = 'lpp_station_json'
LPP_STATION_FILE = 'stations_lj.csv'

LPP_STATIC_URL= 'http://194.33.12.24/timetables/getArrivalsOnStation'
LPP_STATIC_KAFKA_TOPIC = 'lpp_static_json'

LPP_LIVE_URL = 'http://194.33.12.24/timetables/liveBusArrival'
LPP_LIVE_KAFKA_TOPIC = 'lpp_live_json'

LPP_ROUTE_GROUPS_URL = 'http://194.33.12.24/routes/getRouteGroups'
LPP_ROUTE_URL = 'http://194.33.12.24/routes/getRoutes'
LPP_ROUTE_FILE = 'routes_ijs.json'

# Air pollution
POLLUTION_URL = 'http://www.ljubljana.si/si/zivljenje-v-ljubljani/okolje-prostor-bivanje/stanje-okolja/zrak/'
POLLUTION_KAFKA_TOPIC = 'pollution_json'

# Ljubljana loaction
LJ_MIN_LNG = 14.44
LJ_MAX_LNG = 14.58
LJ_MIN_LAT = 46.0
LJ_MAX_LAT = 46.1

# Environment overrides
locals().update(os.environ)

# Local overrides
try:
    from collectors.local_settings import *
except ImportError:
    pass

KAFKA_URL = KAFKA_HOST + ':' + KAFKA_PORT