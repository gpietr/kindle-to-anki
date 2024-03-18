from flashcard_generator import generate_flashcards, set_with_key
from kindle_database_reader import read_kindle_vocab_database
from translator import translate


vocab_db_path = '''Location/of/the/vocab.db'''

words = read_kindle_vocab_database(vocab_db_path)

unique_words = list(set_with_key(words, func=lambda x: x[0]))


print("read words from kindle database")

def report_progress(i, total):
    print(f"Translated {i} of {total} words")

translations = translate([word[0] for word in unique_words], report_progress)

print("translated words")

deck = generate_flashcards(unique_words, translations)

deck.write_to_file("kindle_vocab_flashcards.apkg")

print("flashcards written to file")