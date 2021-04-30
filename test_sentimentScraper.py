import unittest
import main

class MyTestCase(unittest.TestCase):
    def test_request_page(self):
        self.assertNotEqual(None,main.getSoup())

    def test_get_sentiment(self):
        my_soup = main.getSoup()
        sentiment = my_soup.find("tr")  # find sentiment block
        sentiment_liste = main.getSentiment(sentiment)
        self.assertEqual(len(sentiment_liste),2)

    def test_last_update(self):
        my_soup = main.getSoup()
        lastUpdateTime = main.getLastUpdate(my_soup)
        self.assertEqual(len(lastUpdateTime) ,8)


if __name__ == '__main__':
    unittest.main()
