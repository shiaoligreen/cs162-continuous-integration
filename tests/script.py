import os
import requests
import unittest
from sqlalchemy import create_engine

class tests(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("postgresql:///cs162_user:cs162_password@localhost:5432/cs162")
        self.engine.connect()

    def tearDown(self):
        self.engine.close()

    def test_good_expression(self):
        r = requests.post("http://localhost:5000/add", data={"expression": "42+21"})
        self.assertEqual(r.status_code, 200)

    def test_database(self):
        r = requests.post("http://localhost:5000/add", data={"expression": "42+21"})
        query = self.connection.execute("SELECT * FROM Expression WHERE text='42+21'")
        rows = query.fetchall()
        self.assertEqual(len(rows), 1)

    def test_bad_expression(self):
        r = requests.post("http://localhost:5000/add", data={"expression": "42+"})
        self.assertNotEqual(r.status_code, 200)

    def test_bad_db(self):
        r = requests.post("http://localhost:5000/add", data={"expression": "42+"})
        self.assertNotEqual(r.status_code, 200)
        query = self.connection.execute("SELECT * FROM Expression WHERE text='42+'")
        rows = query.fetchall()
        self.assertEqual(len(rows), 0)

if __name__ == "__main__":
    unittest.main()