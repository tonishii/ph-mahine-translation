import re
from collections import defaultdict

def clean_pangasinese(text):
    new_testament_books = [
        "Mateo", "Marcos", "Lucas", "Juan", "Gawgawa",
        "Roma", "1 Corinto", "2 Corinto", "Galacia", "Efeso", "Filipos", "Colosas",
        "2 Tesalonica", "1 Timoteo", "2 Timoteo", "Tito", "Filemon",
        "Hebreo", "Santiago", "1 Pedro", "2 Pedro", "1 Juan", "2 Juan", "3 Juan", "Judas", "Puyan"
    ]

    books = new_testament_books

    pattern = r"\d+\s+Pangasinan Maung a Balita Biblia New Testament © 1977, Bible © 1983, Philippine Bible Society\.\s+"
    text = re.sub(pattern, "", text)

    pattern = r"^(.*?)(?=Mateo\s+1\s)"
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

    pattern = r"((\d+-)*\d+) (?=[A-Za-z])"
    text = re.sub(pattern, r"\n\1 ", text)

    pattern = r"^\d,(.*?)(?=\n)"
    text = re.sub(pattern, "", text, flags=re.MULTILINE)

    pattern = r"\n\s*\n"
    text = re.sub(pattern, "\n", text)

    pattern = r"Esclarecimento(.*)+"
    text = re.sub(pattern, "", text)

    pattern = r"(\d+\s+[A-Za-z]+\s+)\d+\n(\d+)\s*\n+"
    text = re.sub(pattern, r"\1\2\n", text)

    pattern = r"[A-Za-z]+\n(?=[A-Za-z]+\s+\d+)"
    text = re.sub(pattern, "\n", text)
    
    pattern = r"1 Tesalonica\s\n+(?=1)"
    text = re.sub(pattern, "", text)
    
    pattern = r"(1 Tesalonica\s)\n+(?=\d)"
    text = re.sub(pattern, r"\1", text)

    #verify(text)
    return text, books

def verify(text):

  new_testament_books = [
      "Mateo", "Marcos", "Lucas", "Juan", "Gawgawa",
      "Roma", "1 Corinto", "2 Corinto", "Galacia", "Efeso", "Filipos", "Colosas",
      "1 Tesalonica", "2 Tesalonica", "1 Timoteo", "2 Timoteo", "Tito", "Filemon",
      "Hebreo", "Santiago", "1 Pedro", "2 Pedro", "1 Juan", "2 Juan", "3 Juan", "Judas", "Puyan"
  ]

  books = new_testament_books

  chapter_counts = [
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
