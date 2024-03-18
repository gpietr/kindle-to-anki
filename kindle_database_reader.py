import sqlite3


def read_kindle_vocab_database(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    all_words_query  = f"""
    SELECT w.stem, l.usage
    FROM LOOKUPS l
    JOIN WORDS w ON l.word_key = w.id
    """

    try:
        cursor.execute(all_words_query)
        looked_up_words = cursor.fetchall()
        return looked_up_words
    finally:
        # Ensure the database connection is closed
        conn.close()

