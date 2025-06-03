import unittest
from solution import strict


class TestAnnotationsDecorator(unittest.TestCase):
    def test_correct_types(self):
        """Тестирование корректных аргументов."""
        @strict
        def test_func(a: int, b: str) -> str:
            return f'Значения {a} и {b}'

        result = test_func(1, '2')
        self.assertEqual(result, 'Значения 1 и 1')

    def test_incorrect_types(self):
        """Тестирование некорректных аргументов."""
        @strict
        def test_func(a: int, b: str) -> str:
            return f'Значения {a} и {b}'

        with self.assertRaises(TypeError):
            test_func('1', 2)



if __name__ == "__main__":
    unittest.main()
