import regex as re
from collections import defaultdict

books = [
    "Matiyu", "Markus", "Lukas", "Yahiya", "Kiyawakilan", "Rüm",
    "1 Kurintu", "2 Kurintu", "Galatiya", "Ipisus", "Pilipi", "Kulussa",
    "1 Tisalunika", "2 Tisalunika", "1 Tiuti", "2 Timuti", "Titus", "Pilimun",
    "Hibrani", "Ya’kub", "1 Pitrus", "2 Pitrus",
    "1 Yahiya", "2 Yahiya", "3 Yahiya", "Jahud", "Pagpanyataꞌ"
]

def clean_tausug(text):
    
    # Remove footer
    pattern = r"\b\d+\s+Tausug KITAB INJIL © 1998, Wycliffe Bible Translators, Inc\.\s*"
    text = re.sub(pattern, "", text)

    # Separate by book + chapter
    book_pattern = "|".join(books)
    pattern = rf"(?:\b({book_pattern}))\s+(?:\1\s+)?(\d+)\b(?![\"“]?[A-Za-z])"
    text = re.sub(pattern, r"\n\n\1 \2", text)

    # Add space after verse ranges (e.g. 3-5a → 3-5 a)
    pattern = r"\b(\d+)-(\d+)([\"“”'’ꞌA-Za-z]+)\b(?![^()]*\))"
    text = re.sub(pattern, r"\n\1-\2 \3", text)

    # Add space after single verse numbers (e.g. 3a → 3 a)
    pattern = r"(?<!-)\b(\d+)\s*([\"“”'’ꞌ\p{L}]+)\b(?![^()]*\))"
    text = re.sub(pattern, r"\n\1 \2", text)

    # Remove standalone ꞌ
    pattern = r"\bꞌ\b"
    text = re.sub(pattern, "", text)
    
    pattern = r"[\(\[\{;,\-]*[A-Z][a-z]{1,3}\.\s*\d+:\d+(?:-\d+)?[\)\]\};,\-]*"
    text = re.sub(pattern, "", text)
    

    # Replace multiple spaces with one space
    pattern = r"[ \t]+"
    text = re.sub(pattern, " ", text)

    # Normalize spacing for punctuation
    pattern = r"\s+([.,])"
    text = re.sub(pattern, r"\1", text)

    # Remove everything after book + chapter
    pattern = rf"({book_pattern})\s+(\d+).*"
    text = re.sub(pattern, r"\1 \2", text)

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
    
    return text
