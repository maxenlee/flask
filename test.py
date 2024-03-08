import main as foo
import pandas as pd
import unittest
import os
from main import create_app

# x = pd.Series(['Agoobi Agoobo', 'choo choo'])
# bar = foo.pickle_blobber(x)
# print(bar)



class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def tearDown(self):
        # Clean up after each test
        if os.path.exists('word_pickle.p'):
            os.remove('word_pickle.p')

    def test_process_text_route(self):
        # Simulate a POST request with JSON data
        response = self.client.post('/process_text', json={'texts': ["testing singularization", "birds flying high"]})
        
        # Check if the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertIn('Processed and pickled successfully.', response.get_json()['message'])
        # Optionally, check if the pickle file is created
        self.assertTrue(os.path.exists('word_pickle.p'))

if __name__ == '__main__':
    unittest.main()
