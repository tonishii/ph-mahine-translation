import regex as re
from collections import defaultdict

books = [
    "Nahum", "Genesis", "Habakkuk", "Exodus", "Sephaniah", "Libiticus", "Haggai",
    "Numbers", "Sekariah", "Deuteronomy", "Malachi", "Joshua", "Hanadan Huwes", "Ruth",
    "Mateo", "1 Samuel", "Marcos", "2 Samuel", "Lucas", "1 Patul", "Juan", "2 Patul",
    "Apostoles", "1 Chronicles", "Roma", "2 Chronicles", "1 Corinth", "Ezra", "2 Corinth",
    "Nehemiah", "Galatia", "Esther", "Ephesus", "Job", "Philippi", "Psalms", "Colossae",
    "Proverbs", "1 Tesalonika", "Ecclesiastes", "2 Tesalonika", "Song of Songs",
    "1 Timothy", "Isaiah", "2 Timothy", "Jeremiah", "Titus", "Lamentations", "Pilimon",
    "Ezekiel", "Hebrews", "Daniel", "James", "Hosea", "1 Pedro", "Joel", "2 Pedro",
    "Amos", "1 Juan", "Obadiah", "2 Juan", "Jonah", "3 Juan", "Mikah", "Juda", "Revelation"
]

def clean_tuwali(text):
    # Remove footer
    pattern = r"\b\d+\s+NAN KALIN APU DIOS © Wycliffe Bible Translators, Inc\.\s*"
    text = re.sub(pattern, "", text)

    # Separate by book + chapter
    book_pattern = "|".join(books)
    pattern = rf"(?:\b({book_pattern}))\s+(?:\1\s+)?(\d+(?:,\d+)*)\b(?![:\dA-Za-z])"
    text = re.sub(pattern, r"\n\n\1 \2", text)

    # Add space after verse ranges (e.g. 3-5a → 3-5 a)
    pattern = r"\b(\d+)[,-](\d+)([\"“”'’ꞌA-Za-z]+)\b(?![^()]*\))"
    text = re.sub(pattern, r"\n\1-\2 \3", text)

    # Add space after single verse numbers (e.g. 3a → 3 a)
    pattern = r"\b(\d+(?![-–—]))([\"“”'’ꞌA-Za-z]+)\b(?![^()]*\))"
    text = re.sub(pattern, r"\n\1 \2", text)

    # Remove cross references like Juan 3:16
    pattern = rf"[(;\[{{\.,]*\b({book_pattern})\s+\d+:\d+(?:[–—-]\d+:\d+)?(?:[–—-]\d+)?(?:,\s*\d+)?[)\]}}\.,;]*"
    text = re.sub(pattern, "", text)

    # Replace multiple spaces or tabs with one space
    pattern = r"[ \t]+"
    text = re.sub(pattern, " ", text)

    # Normalize spacing for punctuation
    pattern = r"\s+([.,])"
    text = re.sub(pattern, r"\1", text)

    # Remove everything after book + chapter
    pattern = rf"({book_pattern})\s+(\d+).*"
    text = re.sub(pattern, r"\1 \2", text)

    text = re.sub(r'\b\d+:\d+(?:-\d+:\d+|-\d+)?\b', '', text)
    
    # Remove parentheses but keep contents
    pattern = r"[()]+"
    text = re.sub(pattern, "", text)

    # Remove “Esclarecimento” and everything after
    pattern = r"Esclarecimento(.|\n)*"
    text = re.sub(pattern, "", text)

    # Remove double newlines
    text = re.sub(r'\n\n+', '\n', text)

    # Remove leading newlines
    text = re.sub(r'^\s*\n+', '', text)
    
    return text, books
