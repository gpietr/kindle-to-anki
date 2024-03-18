import genanki
import random

def generate_flashcards(words_with_contexts, translations):
    flash_cards = list(zip(words_with_contexts, translations))
    # remove duplicates from flash_cards by words
    unique_flash_cards = list(set_with_key(flash_cards, func=lambda x: x[0][0]))


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

    return deck

def set_with_key(iterable, func):
    seen=set()
    return {e for e in iterable if func(e) not in seen and not seen.add(func(e))}
