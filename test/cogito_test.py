import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
import cogito


class CogitoCheck(unittest.TestCase):

    def setUp(self):
        self.base_path = os.path.dirname(__file__)
        self.iam_file = '{}/files/test.iam'.format(self.base_path)
        self.json_file = '{}/files/test.json'.format(self.base_path)

    def test_cogito_to_json(self):
        with open(self.iam_file) as iam:
            with open(self.json_file) as json:
                self.assertEqual(cogito.to_json(iam.read()), json.read())

    def test_cogito_to_iam(self):
        with open(self.iam_file) as iam:
            with open(self.json_file) as json:
                self.assertEqual(cogito.to_iam(json.read()), iam.read())

    def test_error(self):
        with self.assertRaises(cogito.CogitoError):
            cogito.to_iam("bad json")

if __name__ == '__main__':
    print "Testing cogito at location: {}".format(cogito.__file__)
    unittest.main()
