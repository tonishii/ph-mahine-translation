import regex as re
from collections import defaultdict

books = [
    "Nahum", "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua",
    "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles",
    "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalm", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Songs", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel",
    "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Habakkuk",
    "Sephaniah", "Haggai", "Sekariah", "Malachi", "Mathew", "Matthew", "Mark", "Luke", "John",
    "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy",
    "2 Timothy", "Titus", "Pilimon", "Hebrews", "James", "1 Peter", "2 Peter",
    "1 John", "2 John", "3 John", "Jude", "Revelation"
]


def clean_kalanguya(text):
    # Remove footer
    pattern = r"\b\d+\s+Ya ehel apu Dios © 2009, Wycliffe Bible Translators, Inc\.\s*"
    text = re.sub(pattern, "", text)

    # Separate by book + chapter
    book_pattern = "|".join(books)
    pattern = rf"(?:\b({book_pattern}))\s+(?:\1\s+)?(\d+)\b(?!:)(?![\"“]?[A-Za-z])"
    text = re.sub(pattern, r"\n\n\1 \2", text)

    # Add space after verse ranges (e.g. 3-5a → 3-5 a)
    pattern = r"\b(\d+)-(\d+)([\"“”'’ꞌA-Za-z]+)\b(?![^()]*\))"
    text = re.sub(pattern, r"\n\1-\2 \3", text)

    # Add space after single verse numbers (e.g. 3a → 3 a)
    pattern = r"\b(\d+(?![-–—]))([\"“”'’ꞌA-Za-z]+)\b(?![^()]*\))"
    text = re.sub(pattern, r"\n\1 \2", text)

    # Remove inline references like (Genesis 1:1)
    pattern = rf"[(;\[{{\.,]*\b(?:{book_pattern})\s+\d+:\d+(?:-\d+)?(?:,\s*\d+)?[)\]}}\.,;]*"
    text = re.sub(pattern, "", text)

    # Remove standalone hyphens
    pattern = r"(?<!\w)-(?!\w)"
    text = re.sub(pattern, "", text)

    # Replace multiple spaces with one space
    pattern = r"[ \t]+"
    text = re.sub(pattern, " ", text)

    # Normalize spacing for punctuation
    pattern = r"\s+([.,])"
    text = re.sub(pattern, r"\1", text)

    # Keep only book name and chapter
    pattern = rf"({book_pattern})\s+(\d+).*"
    text = re.sub(pattern, r"\1 \2", text)
    
    text = re.sub(r'\b\d+:\d+(?:-\d+:\d+|-\d+)?\b', '', text)

    # Remove parentheses but keep contents
    pattern = r"[()]+"
    text = re.sub(pattern, "", text)

    # Remove “Esclarecimento” and everything after
    pattern = r"Esclarecimento(.|\n)*"
    text = re.sub(pattern, "", text)

    # Clean up excess newlines
    text = re.sub(r'\n\n+', '\n', text)
    text = re.sub(r'^\s*\n+', '', text)
    
    return text, books
