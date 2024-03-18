import unittest

from kindle_database_reader import read_kindle_vocab_database


class TestKindleVocabDatabase(unittest.TestCase):
    def test_read_kindle_vocab_database(self):
        database_path = "./test/vocab.db"
        entries = read_kindle_vocab_database(database_path)
        self.assertIsNotNone(entries)
        self.assertGreater(len(entries), 0)

if __name__ == '__main__':
    unittest.main()