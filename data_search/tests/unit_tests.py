import unittest
from unittest.mock import patch

from return_values import ret_val

from data_search.data_search import run_search


class TestMyMethod(unittest.TestCase):
    @patch('builtins.input', side_effect=['hans', 'julie'])
    def test1(self, input):
        result = run_search()
        self.assertEqual(result, ret_val[0])

    @patch('builtins.input', side_effect=['nonexisting', 'julie'])
    def test2(self, input):
        result = run_search()
        self.assertEqual(result, ret_val[1])

    @patch('builtins.input', side_effect=['Dietrich Rusche', 'Margit Schaumäker'])
    def test3(self, input):
        result = run_search()
        self.assertEqual(result, ret_val[2])


if __name__ == '__main__':
    unittest.main()