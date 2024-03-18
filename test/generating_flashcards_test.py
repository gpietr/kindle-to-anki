import unittest

from flashcard_generator import generate_flashcards


class TestKindleVocabDatabase(unittest.TestCase):
    def test_read_kindle_vocab_database(self):
        deck = generate_flashcards([tuple(["hola", "Yo digo hola"]), tuple(["adios", "aa"])], ["hello", "bye"])

        self.assertEqual(len(deck.notes), 2)

if __name__ == '__main__':
    unittest.main()