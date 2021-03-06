import unittest
import unittest.mock as mock

from pytraffic.collectors.util import es_search


@mock.patch('pytraffic.collectors.util.es_search.Elasticsearch')
class EsSearchTest(unittest.TestCase):
    def test_connect(self, mock_es):
        es_search.EsSearch('host', 'port', 'index')
        mock_es.assert_called_once_with([{'host': 'host', 'port': 'port'}])

    def test_get_json(self, mock_es):
        es = es_search.EsSearch('host', 'port', 'index')
        mock_es().search.return_value = {'test': [1, 2, 3]}
        self.assertEqual(
            es.get_json({"query": {"updated": {"gte": "now-15m"}}}),
            {'test': [1, 2, 3]})
        mock_es().search.assert_called_once_with(index='index', body={
            "query": {"updated": {"gte": "now-15m"}}})


if __name__ == '__main__':
    unittest.main()
