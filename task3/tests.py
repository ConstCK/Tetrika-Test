import unittest

from solution import appearance
from constants import TESTS

class TestAppearanceFunction(unittest.TestCase):
    def test_appearance(self):
        for test_case in TESTS:
            intervals = test_case['intervals']
            expected_answer = test_case['answer']
            with self.subTest(intervals=intervals, expected_answer=expected_answer):
                result = appearance(intervals)
                self.assertEqual(result, expected_answer)

# Запуск тестов
if __name__ == '__main__':
    unittest.main()