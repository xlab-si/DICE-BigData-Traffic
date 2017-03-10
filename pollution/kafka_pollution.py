import requests, datetime, re, json

from lxml import html
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['192.168.0.60:9092'],
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))

def process_table(table, date, source):
    header_row, = table.xpath('.//thead/tr')

    headers = [re.sub('[\r\n\t]', '', header_cell.text_content().strip()) for header_cell in header_row.xpath('./th')]

    english = {'ura': 'hour',
               'SO2µg/m3(normativi)': 'so2',
               'NOµg/m3': 'no',
               'NO2µg/m3(normativi)': 'no2',
               'NO×µg/m3': 'nox',
               'COmg/m3(normativi)': 'co',
               'Trdni delci PM10µg/m3(normativi)': 'pm',
               'Temperatura°C': 'temperature',
               'Hitrost vetram/s': 'windspeed',
               'Smer vetra': 'wind_direction',
               'Vlaga%': 'humidity',
               'Pritiskmbar': 'pressure',
               'SonÄ\x8dno sevanjeW/m2': 'solar_radiation',
               'Benzenµg/m3(normativi)': 'benzene',
               'Toluenµg/m3': 'tolulene',
               'Paraksilenµg/m3': 'paraxylene', }

    default = {'hour': None,
               'so2': None,
               'no': None,
               'no2': None,
               'nox': None,
               'co': None,
               'pm': None,
               'temperature': None,
               'windspeed': None,
               'wind_direction': None,
               'humidity': None,
               'pressure': None,
               'solar_radiation': None,
               'benzene': None,
               'tolulene': None,
               'paraxylene': None,
               'scraped': None,
               'location': None}

    english_headers = [english[header] for header in headers if header in english]

    english_headers.append('scraped')
    english_headers.append('location')

    value_rows = table.xpath('.//tbody/tr[not(@class="limits") and not(@class="alarms")]')
    all_rows = []

    for value_row in value_rows:
        row = []

        for value_cell in value_row.xpath('./th|td'):
            v = value_cell.text_content().strip()
            try:
                v = float(v)
            except ValueError:
                pass
            if v == '?':
                v = None
            row.append(v)

        row.append(None)
        row.append(source)
        all_rows.append(dict(zip(english_headers, row)))


    for row in all_rows:
        tmp = default.copy()
        tmp.update(row)
        hour, minute = tmp['hour'].split(':')
        isoformat_date = datetime.datetime.isoformat(date.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0))
        tmp['scraped'] = isoformat_date
        producer.send('pollution_json', tmp)


url = 'http://www.ljubljana.si/si/zivljenje-v-ljubljani/okolje-prostor-bivanje/stanje-okolja/zrak/' \
      '?source={}&day={}&month={}&year={}'

date = datetime.datetime.today()

for source in ['bezigrad', 'vosnjakova-tivolska']:
    response = requests.get(url.format(source, date.day, date.month, date.year))
    etree = html.fromstring(response.text)
    table, = etree.xpath('.//table[@id="air-polution"]')
    process_table(table, date, source)