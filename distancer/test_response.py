import unittest
from unittest import mock

from utils import YandexResponse
from werkzeug.exceptions import NotFound


class TestYandexResponse(unittest.TestCase):
    def setUp(self) -> None:
        # Use mock patch to fake GET request
        patcher = mock.patch("utils.requests.get")
        self.mocked_get = patcher.start()
        self.addCleanup(patcher.stop)

        # Instantiate YandexResponse object
        self.addr1 = YandexResponse("MKAD")
        self.addr2 = YandexResponse("Russia, Moscow, Kirovogradskaya Street, 14")
        self.addr3 = YandexResponse("Saint Basil's Cathedral")

        # Define coordinate for each address
        self.addr1.coordinate = (37.632206, 55.898947)
        self.addr2.coordinate = (37.605939, 55.622609)
        self.addr3.coordinate = (-120.200676, 49.064265)

    def test_get_response(self):
        # Ensure that query for yandex is correct
        self.mocked_get.return_value.ok = True
        self.mocked_get.return_value.json.return_value = {
            "response": {
                "GeoObjectCollection": {
                    "metaDataProperty": {"GeocoderResponseMetaData": {"found": 1}}
                }
            }
        }

        api_response = self.addr1.get_response()
        self.mocked_get.assert_called_with(
            "https://geocode-maps.yandex.ru/1.x",
            {
                "geocode": "MKAD",
                "apikey": None,
                "format": "json",
                "lang": "en_US",
            },
        )
        self.assertEqual(
            api_response,
            {
                "response": {
                    "GeoObjectCollection": {
                        "metaDataProperty": {"GeocoderResponseMetaData": {"found": 1}}
                    }
                }
            },
        )

        # Ensure that 404 error is raised correctly if no result from response
        self.mocked_get.return_value.ok = True
        self.mocked_get.return_value.json.return_value = {
            "response": {
                "GeoObjectCollection": {
                    "metaDataProperty": {"GeocoderResponseMetaData": {"found": 0}}
                }
            }
        }

        with self.assertRaises(NotFound):
            self.addr2.get_response()

    def test_get_distance(self):
        # assert that distance calculation is correct up to 1 decimal place
        self.assertAlmostEqual(
            self.addr1.get_distance(self.addr2.coordinate), 30.8, places=1
        )
        self.assertAlmostEqual(
            self.addr1.get_distance((20.3131, 10.8888)), 5226.0, places=1
        )
        self.assertAlmostEqual(self.addr2.get_distance((-3, 5.1)), 6669.1, places=1)

    def test_check_in_mkad(self):
        # test for checking if coordinate is in mkad
        self.assertTrue(self.addr1.check_in_mkad())
        self.assertTrue(self.addr2.check_in_mkad())
        self.assertFalse(self.addr3.check_in_mkad())


if __name__ == "__main__":
    unittest.main()
