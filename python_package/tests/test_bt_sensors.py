import unittest
import unittest.mock as mock

from pytraffic.collectors import bt_sensors


@mock.patch('pytraffic.collectors.bt_sensors.BtSensors.__init__',
            mock.Mock(return_value=None))
class BtSensorsTest(unittest.TestCase):
    @mock.patch('pytraffic.collectors.bt_sensors.files')
    def test_load_data(self, mock_files):
        bt = bt_sensors.BtSensors()
        bt.get_web_data = mock.Mock()
        bt.get_local_data = mock.Mock()
        bt.sensors_data_file = 'file.json'

        mock_files.old_or_not_exists.return_value = False
        bt.load_data()
        bt.get_web_data.assert_not_called()
        bt.get_local_data.assert_called_once()

        mock_files.old_or_not_exists.return_value = True
        bt.load_data()
        bt.get_web_data.assert_called_once()

    @mock.patch('pytraffic.collectors.bt_sensors.open')
    @mock.patch('pytraffic.collectors.bt_sensors.json')
    def test_get_local_data(self, mock_json, mock_open):
        bt = bt_sensors.BtSensors()
        bt.sensors_data_file = 'file.json'
        data_file = mock.Mock()
        mock_open.return_value.__enter__.return_value = data_file
        mock_json.load.return_value = {'data': [1, 2, 3]}
        bt.get_local_data()
        mock_open.assert_called_once_with('file.json')
        mock_json.load.assert_called_once_with(data_file)
        self.assertEqual(bt.sensors_data, [1, 2, 3])

    @mock.patch('pytraffic.collectors.bt_sensors.open')
    @mock.patch('pytraffic.collectors.bt_sensors.json')
    def test_get_web_data(self, mock_json, mock_open):
        data_file = mock.Mock()
        mock_open.return_value.__enter__.return_value = data_file
        bt = bt_sensors.BtSensors()
        bt.sensors_data_file = 'file.json'
        bt.w_scraper = mock.Mock(
            **{'get_json.return_value': {'data': [1, 2, 3]}})

        bt.get_web_data()
        mock_open.assert_called_once_with('file.json', 'w')
        mock_json.dump.assert_called_once_with({'data': [1, 2, 3]}, data_file)
        self.assertEqual(bt.sensors_data, [1, 2, 3])

        bt.get_local_data = mock.Mock()
        bt.w_scraper = mock.Mock(**{'get_json.return_value': None})
        bt.get_web_data()
        bt.get_local_data.assert_called_once()

    def test_run(self):
        bt = bt_sensors.BtSensors()
        bt.w_scraper = mock.Mock()
        bt.w_scraper.get_json.return_value = {
            "totalPages": 1,
            "currentPage": 1,
            "totalElements": 28,
            "elementsPerPage": 100,
            "data": [
                {
                    "count": 1,
                    "avgSpeed": 44.643,
                    "timestampFrom": "2017-03-28T10:55:00+02:00",
                    "allCount": 1,
                    "toBtId": "BTR0206",
                    "fromBtId": "BTR0215",
                    "avgTravelTime": 0.112,
                    "timestampTo": "2017-03-28T11:10:00+02:00",
                    "id": "58da2a40c0a6834de258bfa6"
                },
                {
                    "count": 17,
                    "avgSpeed": 35.66241176470588,
                    "timestampFrom": "2017-03-28T11:15:00+02:00",
                    "allCount": 18,
                    "toBtId": "BTR0212",
                    "fromBtId": "BTR0202",
                    "avgTravelTime": 0.030294117647058826,
                    "timestampTo": "2017-03-28T11:30:00+02:00",
                    "id": "58da2ef0c0a6834de258c020"
                }
            ]
        }

        bt.sensors_data = [
            {
                "neighbours": [
                    {
                        "distance": 500,
                        "btId": "BTR0201"
                    },
                    {
                        "distance": 1800,
                        "btId": "BTR0203"
                    },
                    {
                        "distance": 1010,
                        "btId": "BTR0212"
                    }
                ],
                "btId": "BTR0202",
                "id": "57531a9fbffebc11048b4567",
                "loc": {
                    "lng": 14.50978,
                    "lat": 46.06826
                }
            },
            {
                "neighbours": [
                    {
                        "distance": 470,
                        "btId": "BTR0205"
                    },
                    {
                        "distance": 5000,
                        "btId": "BTR0215"
                    },
                    {
                        "distance": 2010,
                        "btId": "BTR0216"
                    }
                ],
                "btId": "BTR0206",
                "id": "57535b23bee8e3121ed7df95",
                "loc": {
                    "lng": 14.50072,
                    "lat": 46.04619
                }
            },
            {
                "neighbours": [
                    {
                        "distance": 1010,
                        "btId": "BTR0202"
                    }
                ],
                "btId": "BTR0212",
                "id": "57535b23bee8e3121ed7df99",
                "loc": {
                    "lng": 14.49663,
                    "lat": 46.06703
                }
            }]

        bt.not_lj = ['BTR0215']

        res = {
            'toBtLng': 14.49663,
            'id': '58da2ef0c0a6834de258c020',
            'toBtLat': 46.06703,
            'avgTravelTime': 0.030294117647058826,
            'timestampTo': '2017-03-28T11:30:00+02:00',
            'timestampFrom': '2017-03-28T11:15:00+02:00',
            'fromBtId': 'BTR0202',
            'fromBtLng': 14.50978,
            'fromBtLat': 46.06826,
            'toBtId': 'BTR0212',
            'avgSpeed': 35.66241176470588,
            'count': 17,
            'allCount': 18,
            'distance': 1010
        }

        bt.producer = mock.Mock()
        bt.run()
        bt.producer.send.assert_called_once_with(res)

    @mock.patch('pytraffic.collectors.bt_sensors.plot')
    def test_plot(self, mock_plot):
        bt = bt_sensors.BtSensors()
        bt.sensors_data = [
            {
                "neighbours": [
                    {
                        "distance": 500,
                        "btId": "BTR0201"
                    },
                    {
                        "distance": 1800,
                        "btId": "BTR0203"
                    },
                    {
                        "distance": 1010,
                        "btId": "BTR0212"
                    }
                ],
                "btId": "BTR0202",
                "id": "57531a9fbffebc11048b4567",
                "loc": {
                    "lng": 14.50978,
                    "lat": 46.06826
                }
            },
            {
                "neighbours": [
                    {
                        "distance": 470,
                        "btId": "BTR0205"
                    },
                    {
                        "distance": 5000,
                        "btId": "BTR0215"
                    },
                    {
                        "distance": 2010,
                        "btId": "BTR0216"
                    }
                ],
                "btId": "BTR0206",
                "id": "57535b23bee8e3121ed7df95",
                "loc": {
                    "lng": 14.50072,
                    "lat": 46.04619
                }
            },
            {
                "neighbours": [
                    {
                        "distance": 1010,
                        "btId": "BTR0202"
                    }
                ],
                "btId": "BTR0212",
                "id": "57535b23bee8e3121ed7df99",
                "loc": {
                    "lng": 14.49663,
                    "lat": 46.06703
                }
            },
            {
                "neighbours": [
                    {
                        "distance": 5000,
                        "btId": "BTR0206"
                    },
                    {
                        "distance": 4600,
                        "btId": "BTR0218"
                    }
                ],
                "btId": "BTR0215",
                "id": "57535b23bee8e3121ed7df9c",
                "loc": {
                    "lng": 14.54398,
                    "lat": 46.01633
                }
            }]
        bt.not_lj = ['BTR0215']

        bt.plot_map('title', (10, 10), 100, 15, 5, (0.1, 0.2), 10, 'image.png')
        mock_plot.PlotOnMap.assert_called_once_with(
            [14.50978, 14.50072, 14.49663],
            [46.06826, 46.04619, 46.06703],
            'title')
        mock_plot.PlotOnMap().generate.assert_called_once_with(
            (10, 10), 100, 15, 5)
        mock_plot.PlotOnMap().label.assert_called_once_with(
            ['BTR0202', 'BTR0206', 'BTR0212'], (0.1, 0.2), 10)
        mock_plot.PlotOnMap().save.assert_called_once_with(None, 'image.png')


if __name__ == '__main__':
    unittest.main()
