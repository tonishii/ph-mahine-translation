import re
from collections import defaultdict

def clean_english(text):
    old_testament_books = [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
        "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
        "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
        "Ezra", "Nehemiah", "Esther", "Job", "Psalms",
        "Proverbs", "Ecclesiastes", "Song of Songs", "Isaiah",
        "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea",
        "Joel", "Amos", "Abadiah", "Jonah", "Micah", "Nahum",
        "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"
    ]

    new_testament_books = [
        "Matthews", "Mark", "Luke", "John", "The Acts",
        "Romans", "1 Corinthians", "2 Corinthians",
        "Galatians", "Ephesians", "Philippians", "Colossians",
        "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy",
        "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter",
        "1 John", "2 John", "3 John", "Jude", "Revelation"
    ]

    books = old_testament_books + new_testament_books
    
    pattern = r"^(.*?)(?=Genesis\s+1\s)"
    text = re.sub(pattern, "", text)
    
    pattern = r"\d+\s+King James Version 1611, spelling, punctuation and text formatting modernized by ABS in 1962; © 2010 American Bible Society\s+"
    #pattern = r"\d+\n+Ang Pulong Sang Dios\n\(Hiligaynon Contemporary Bible\)\n© 1996, 2006, 2011 by Biblica, Inc\.®.\s+"
    text = re.sub(pattern, "", text)
    
    pattern = r"\((.*?)\)|\{(.*?)\}"
    text = re.sub(pattern, "", text)
    
    pattern = r'\s+([.,;:!?])'
    text = re.sub(pattern, "", text)
    
    pattern = r'\s+([-])'
    text = re.sub(pattern, "-", text)
    
    pattern = r'([-])\s+'
    text = re.sub(pattern, "-", text)
    
    books_pattern = "|".join(books)
    
    pattern = r"({})\s+(\d+)\s(.*?)(?=\d+\s*)".format(books_pattern)
    text = re.sub(pattern, r"\1 \2 ", text)

    pattern = rf"(^|\s)({books_pattern})\s(\d+)\s\n*(\d+)"
    text = re.sub(pattern, r"\n\1 \2 \3\n\4", text)
    
    pattern = r"^\s+"
    text = re.sub (pattern, "", text, flags=re.MULTILINE)
    
    pattern = r"\s\n(Juan\s+\d+)[ \t]*\n([A-Za-z])"
    text = re.sub(pattern, r" \1\2", text, flags=re.MULTILINE)
    
    pattern = r"((\d+-)*\d+)\s*(?=[A-Za-z])"
    text = re.sub(pattern, r"\n\1 ", text)
    
    pattern = r"^\d,(.*?)(?=\n)"
    text = re.sub(pattern, "", text, flags=re.MULTILINE)
    
    pattern = r"\n\s*\n"
    text = re.sub(pattern, "\n", text)
    
    pattern = r"^\d+,(.*)+"
    text = re.sub(pattern, "", text, flags=re.MULTILINE)
    
    pattern = r"\n\s*\n"
    text = re.sub(pattern, "\n", text)
    
    pattern = r"Esclarecimento(.*)+"
    text = re.sub(pattern, "", text)
    
    pattern = r"(\d+\s+[A-Za-z]+\s+)\d+\n(\d+)\s*\n+"
    text = re.sub(pattern, r"\1\2\n", text)
    
    pattern = r"\s+English-All Bible\s+"
    text = re.sub(pattern, " ", text)
    
    pattern = r"[A-Za-z]+\n(?=[A-Za-z]+\s+\d+)"
    text = re.sub(pattern, "\n", text)
    
    pattern = r"The Acts\n"
    text = re.sub(pattern, "\n", text)
    
    pattern = r"(2 Kings) 2\n1(.*)\n(?=1)"
    text = re.sub(pattern, r"\1 1\n", text)
    
    #verify(text)
    return text, books

def verify(text):
    old_testament_books = [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
        "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
        "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther",
        "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
        "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah",
        "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"
    ]

    new_testament_books = [
        "Matthew", "Mark", "Luke", "John", "Acts",
        "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians",
        "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon",
        "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
    ]


    books = old_testament_books + new_testament_books

    chapter_counts = [
        # Old Testament
        50, 40, 27, 36, 34,   # Genesis – Deuteronomio
        24, 21, 4, 31, 24,    # Josue – 2 Samuel
        22, 25, 29, 36, 10, 13, 10,  # 1 Hari – Ester
        42, 150, 31, 12, 8,   # Job – Kanta
        66, 52, 5, 48, 12,    # Isaias – Daniel
        14, 3, 9, 1, 4,       # Hoseas – Jonas
        7, 3, 3, 3, 2, 14, 4, # Micas – Malakias

        # New Testament
        28, 16, 24, 21, 28,   # Mateo – Binuhatan
        16, 16, 13, 6, 6, 4, 4,  # Roma – Colosas
        5, 3, 6, 4, 3, 1,     # 1 Tesalonica – Filemon
        13, 5, 5, 3, 5, 1, 1, 1, 22  # Hebreo – Pahayag
    ]

    # Build regex pattern safely
    book_pattern = "|".join(map(re.escape, books))
    pattern = rf"(?m)^({book_pattern})\s+(\d+)\b"

    chapters = re.findall(pattern, text)

    book_chapters = defaultdict(list)
    for book, chap in chapters:
        book_chapters[book].append(int(chap))

    for ((book, chaps), count) in zip(book_chapters.items(), chapter_counts):
        if chaps != sorted(chaps):
            print(f"Chapters out of order in {book}: {chaps}")
        else:
            if count == len(chaps):
                print(f"{book} chapters ({len(chaps)}) in order ✓")
            else:
                print(f"{book} chapters ({len(chaps)}) NOT in order x")
