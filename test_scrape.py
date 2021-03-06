import unittest

import scrape


class FindDataTest(unittest.TestCase):
    def test_it_works(self):
        with open('test_data.txt', 'r') as f:
            data = scrape.find_data(f.read())
        self.assertEqual(len(data), 45)

        # Can parse status
        self.assertEqual(data[0]['status'], 'active')
        # self.assertEqual(data[8]['status'], 'partialservice')

        # Can get lat long
        self.assertEqual(data[0]['latitude'], '30.26408')
        self.assertEqual(data[0]['longitude'], '-97.74355')

        # Can get address
        self.assertEqual(data[0]['name'], '2nd & Congress')
        self.assertEqual(data[0]['street'], '151 E. 2nd St.')
        self.assertEqual(data[0]['city'], 'Austin')
        self.assertEqual(data[0]['state'], 'TX')
        self.assertEqual(data[0]['zip'], '78701')
        self.assertEqual(data[0]['state_zip'], 'TX 78701')

        # Can get availability
        self.assertEqual(data[0]['bikes'], 7)
        self.assertEqual(data[0]['docks'], 6)


if __name__ == '__main__':
    unittest.main()
