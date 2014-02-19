import unittest

import scrape


class FindDataTest(unittest.TestCase):
    def test_it_works(self):
        with open('test_data.txt', 'r') as f:
            data = scrape.find_data(f.read())
        self.assertEqual(len(data), 26)



if __name__ == '__main__':
    unittest.main()
