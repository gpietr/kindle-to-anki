
#%%
import sqlite3

#%%

# Path to your vocab.db file
vocab_db_path = '''Location/of/the/vocab.db'''

# Connect to the SQLite database
conn = sqlite3.connect(vocab_db_path)
cursor = conn.cursor()

# Query to count words per book
query = """
SELECT b.id, b.title, COUNT(w.word) as word_count
FROM LOOKUPS l
JOIN WORDS w ON l.word_key = w.id
JOIN BOOK_INFO b ON l.book_key = b.id
GROUP BY l.book_key
"""

try:
    cursor.execute(query)
    books_with_word_counts = cursor.fetchall()
    
    print("Books and their looked-up word counts:")
    for book in books_with_word_counts:
        print(f"Title: {book[0]}, Words: {book[1]}")
finally:
    # Ensure the database connection is closed
    conn.close()
# %%

print(books_with_word_counts)
# %%
# now get words and translations for the first book

# Connect to the SQLite database
conn = sqlite3.connect(vocab_db_path)
cursor = conn.cursor()

first_book_id = books_with_word_counts[0][0]

wordsQuery = f"""
SELECT w.stem, l.usage
FROM LOOKUPS l
JOIN WORDS w ON l.word_key = w.id
where l.book_key = '{first_book_id}'
"""

try:
    cursor.execute(wordsQuery)
    looked_up_words = cursor.fetchall()
    
    print("Words and their translations:")
    for word in looked_up_words:
        print(f"Word: {word[0]}, Translation: {word[1]}")
finally:
    # Ensure the database connection is closed
    conn.close()

# %%

from PyMultiDictionary import MultiDictionary


# %%
dictionary = MultiDictionary(tuple(["hola", "mundo"]))
dictionary.set_words_lang('es')


dictionary.get_translations()


#dictionary.translate(lang = 'es', word = "hola", to = 'en')[5][1]

# %%
from deep_translator import GoogleTranslator

translated = GoogleTranslator(source='es', target='en').translate_batch(["Hola", "Mundo"])  # output -> Weiter so, du bist großartig

print(translated)

# %%

english_translations = []

just_words = [word[0] for word in looked_up_words]

translations = GoogleTranslator(source='es', target='en').translate_batch(just_words)

flash_cards = list(zip(looked_up_words, translations))
# %%


print(flash_cards[0])
# %%
conn = sqlite3.connect(vocab_db_path)
cursor = conn.cursor()

all_words_query  = f"""
SELECT w.stem, l.usage
FROM LOOKUPS l
JOIN WORDS w ON l.word_key = w.id
"""

try:
    cursor.execute(all_words_query)
    looked_up_words = cursor.fetchall()
    
    print("Words and their translations:")
    for word in looked_up_words:
        print(f"Word: {word[0]}, Translation: {word[1]}")
finally:
    # Ensure the database connection is closed
    conn.close()

# %%
english_translations = []

just_words = [word[0] for word in looked_up_words]

translations = GoogleTranslator(source='es', target='en').translate_batch(just_words)

flash_cards = list(zip(looked_up_words, translations))
# %%

# remove duplicates from flash_cards by words

def set_with_key(iterable, func):
    seen=set()
    return {e for e in iterable if func(e) not in seen and not seen.add(func(e))}


unique_flash_cards = list(set_with_key(flash_cards, func=lambda x: x[0][0]))
# %%

print(unique_flash_cards)
# %%

#now make anki cards
import genanki
import random

# Create a new Anki deck
deck_id = random.randint(10000000, 99999999)

# Define the Anki model
model_id = random.randint(10000000, 99999999)
model = genanki.Model(
    model_id,
    'Anki Model',
    fields=[
        {'name': 'Word'},
        {'name': 'Translation'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Word}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Translation}}',
        },
    ],
    css = '''
        .card {
        font-family: sans-serif-light;
        font-size: 20px;
        text-align: center;
        }
    '''
)

# Create Anki notes from the flash cards
notes = []
for flash_card in unique_flash_cards:
    word = flash_card[0][0]
    context = flash_card[0][1]
    context = context.replace(word, "<b>" + word + "</b>")
    translation = flash_card[1] + "<br/><small>" + context + "</small>"
    note = genanki.Note(
        model=model,
        fields=[word, translation],
    )
    notes.append(note)

# Create the Anki deck
deck = genanki.Deck(deck_id, 'Kindle Vocab Deck')

for note in notes:
    deck.add_note(note)

# Generate the Anki package
deck.write_to_file('anki_deck.apkg')
# %%
