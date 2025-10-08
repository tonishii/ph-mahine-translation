import re
from collections import defaultdict

def clean_hiligaynon(text):
    old_testament_books = [
        "Genesis", "Exodus", "Leviticus", "Numero", "Deuteronomio",
        "Josue", "Hukom", "Ruth", "1 Samuel", "2 Samuel",
        "1 Hari", "2 Hari", "1 Cronica", "2 Cronica", "Ezra", "Nehemias", "Ester",
        "Job", "Salmo", "Hulubaton", "Manugwali", "Kanta", "Isaias", "Jeremias",
        "Panalambiton", "Ezekiel", "Daniel", "Hoseas", "Joel", "Amos", "Obadias", "Jonas",
        "Micas", "Nahum", "Zefanias", "Haggai", "Zacarias", "Malakias"
    ]
    
    new_testament_books = [
        "Mateo", "Marcos", "Lucas", "Juan", "Binuhatan",
        "Roma", "1 Corinto", "2 Corinto", "Galacia", "Efeso", "Filipos", "Colosas",
        "1 Tesalonica", "2 Tesalonica", "1 Timoteo", "2 Timoteo", "Tito", "Filemon",
        "Hebreo", "Santiago", "1 Pedro", "2 Pedro", "1 Juan", "2 Juan", "3 Juan", "Judas", "Pahayag"
    ]
    
    books = old_testament_books + new_testament_books
    
    pattern = r"^(.*?)(?=Genesis\s+1\s)"
    text = re.sub(pattern, "", text)
    
    pattern = r"\d+\s+Ang Pulong Sang Dios \(Hiligaynon Contemporary Bible\) © 1996, 2006, 2011 by Biblica, Inc\.®\.\s+"
    #pattern = r"\d+\n+Ang Pulong Sang Dios\n\(Hiligaynon Contemporary Bible\)\n© 1996, 2006, 2011 by Biblica, Inc\.®.\s+"
    text = re.sub(pattern, "", text)
    
    pattern = r"\s+Hiligaynon - All Bible \(Ang Pulong Sang Dios\)\s+"
    text = re.sub(pattern, " ", text)
    
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
    
    pattern = r"((\d+-)*\d+)(?=[A-Za-z])"
    text = re.sub(pattern, r"\n\1 ", text)
    
    pattern = r"((\d+-)*\d+)(?=[“])"
    text = re.sub(pattern, r"\n\1 ", text)
    
    pattern = r"((\d+-)*\d+)(?=[“‘\"\[\'])"
    text = re.sub(pattern, r"\n\1 ", text)
    
    pattern = r" \s(?=\d+\s\w+)"
    text = re.sub(pattern, "\n", text)
    
    pattern = r"^\d,(.*?)(?=\n)"
    text = re.sub(pattern, "", text, flags=re.MULTILINE)
    
    pattern = r"\n\s*\n"
    text = re.sub(pattern, "\n", text)
    
    pattern = r"^\d+,(.*)+"
    text = re.sub(pattern, "", text, flags=re.MULTILINE)
    
    pattern = r"Esclarecimento(.*)+"
    text = re.sub(pattern, "", text)
    
    pattern = r"(\d+\s+[A-Za-z]+\s+)\d+\n(\d+)\s*\n+"
    text = re.sub(pattern, r"\1\2\n", text)
    
    pattern = r"[A-Za-z]+\n(?=[A-Za-z]+\s+\d+)"
    text = re.sub(pattern, "\n", text)
    
    pattern = r"(?<=Habakuk)\s(Habakuk\s\d)"
    text = re.sub(pattern, r"\n\1", text)
    
    pattern = r"(Habakuk\s2\s)(\d\s(.*))"
    text = re.sub(pattern, r"\n\1\n\2", text)
    
    pattern = r"(Habakuk\s3)(.*)"
    text = re.sub(pattern, r"\n\1", text)
    
    pattern = r"\n(.*?)(?=21-35)"
    text = re.sub(pattern, r"\1\n", text)
    
    pattern = r"(?=36-39)"
    text = re.sub(pattern, r"\n", text)
    
    pattern = r"\n(.*?)(?=40-42)"
    text = re.sub(pattern, r"\1\n", text)
    
    pattern = r"\n(.*?)(?=43-54)"
    text = re.sub(pattern, r"\1\n", text)
    
    pattern = r"(?=55-57)"
    text = re.sub(pattern, r"\n", text)
    
    pattern = r"[‒]*\d+‒"
    text = re.sub(pattern, r"", text)
    
    pattern = r"\n\s*\n"
    text = re.sub(pattern, "\n", text)
    
    pattern = r"\n(.*)(?=26-38)"
    text = re.sub(pattern, r"\1\n", text)
    
    pattern = r"\n(.*)(?=39-42)"
    text = re.sub(pattern, r"\1\n", text)
    
    pattern = r"\n(.*)(?=43-45)"
    text = re.sub(pattern, r"\1\n", text)
    
    pattern = r"\n(.*)(?=46-56)"
    text = re.sub(pattern, r"\1\n", text)
    
    pattern = r"(?=26-38)"
    text = re.sub(pattern, r"\n", text)
  
    #verify(text)
    return text, books

def verify(text):
  old_testament_books = [
      "Genesis", "Exodus", "Leviticus", "Numero", "Deuteronomio",
      "Josue", "Hukom", "Ruth", "1 Samuel", "2 Samuel",
      "1 Hari", "2 Hari", "1 Cronica", "2 Cronica", "Ezra", "Nehemias", "Ester",
      "Job", "Salmo", "Hulubaton", "Manugwali", "Kanta", "Isaias", "Jeremias",
      "Panalambiton", "Ezekiel", "Daniel", "Hoseas", "Joel", "Amos", "Obadias", "Jonas",
      "Micas", "Nahum", "Habakuk", "Zefanias", "Haggai", "Zacarias", "Malakias"
  ]

  new_testament_books = [
      "Mateo", "Marcos", "Lucas", "Juan", "Binuhatan",
      "Roma", "1 Corinto", "2 Corinto", "Galacia", "Efeso", "Filipos", "Colosas",
      "1 Tesalonica", "2 Tesalonica", "1 Timoteo", "2 Timoteo", "Tito", "Filemon",
      "Hebreo", "Santiago", "1 Pedro", "2 Pedro", "1 Juan", "2 Juan", "3 Juan", "Judas", "Pahayag"
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
