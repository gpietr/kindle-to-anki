import unittest

from translator import translate

class TestTranslations(unittest.TestCase):
    def test_read_kindle_vocab_database(self):
        # that's a flaky test using 3rd party service and expecting it to return the same result
        results = translate(["hola", "adios"], lambda i, total: None)
        self.assertEqual(results, ['hello', 'bye'])

if __name__ == '__main__':
    unittest.main()