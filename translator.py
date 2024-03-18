from deep_translator import GoogleTranslator


def translate(words, reportProgress):
    translations = []
    translator = GoogleTranslator(source='es', target='en')

    for i, word in enumerate(words):
        translations.append(translator.translate(word))
        reportProgress(i, len(words))
        
    return translations