import re, pandas as pd
from collections import defaultdict

books = [
  "Mateo", "Marcos", "Lucas", "Juan", "Maga Apostoles", "Roma", "1 Corinto",
  "2 Corinto", "Galacia", "Efeso", "Filipos", "Colosas", "1 Tesalonica",
  "2 Tesalonica", "1 Timoteo", "2 Timoteo", "Tito", "Filemon", "Hebreo",
  "Santiago", "1 Pedro", "2 Pedro", "1 Juan", "2 Juan", "3 Juan", "Judas", "El Revelacion",
]

book_pattern = "|".join(books)

def clean_chavacano(text):
  # Remove parentheses but keep the contents
  pattern = r"\((.*?)\)"
  text = re.sub(pattern, r"\1", text)

  pattern = r"<\n\d+\n>\n© 1981 WBT\n"
  text = re.sub(pattern, "", text)

  # Remove everything from the book title to the first verse number
  pattern = rf"({book_pattern})\s(\d+)(.*?)(?=\d+\s[a-zA-Z])"
  text = re.sub(pattern, r"\1 \2\n", text, flags=re.S)

  # Remove the titles
  pattern = rf"\n({book_pattern})\n"
  text = re.sub(pattern, "\n", text)

  # Separates by verse number
  pattern = r"\s\s+(?=\d+\s)"
  text = re.sub(pattern, "\n", text)

  # Separates by verse range
  pattern = r"\s+(?=\d+-\d+\s)"
  text = re.sub(pattern, "\n", text)

  # Removes the last newline
  pattern = r"\n$"
  text = re.sub(pattern, "", text)

  # Normalize spacing
  pattern = r"[ \t]+"
  text = re.sub(pattern, " ", text)

  # Normalizes spacing before a punctuation mark
  pattern = r'\s+([.,;:!?])'
  text = re.sub(pattern, "", text)

  # verify(text)
  return text, books

def verify(text: str):
  pattern = rf"({book_pattern})\s(\d+)"
  chapter_counts = [28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22]

  chapter_counts_dict = { book: count for (book, count) in zip(books, chapter_counts)}

  chapters = re.findall(pattern, text)

  book_chapters = defaultdict(list)
  for book, chap in chapters:
    book_chapters[book].append(int(chap))

  for book, chaps in book_chapters.items():
    if chaps != sorted(chaps):
      print(f"Chapters out of order in {book}: {chaps}")
    else:
      if chapter_counts_dict[book] == len(chaps):
        print(f"{book} chapters ({len(chaps)}) in order ✓")
      else:
        print(f"{book} chapters ({len(chaps)} should be {chapter_counts_dict[book]}) NOT in order x: {chaps}")

  lines = text.splitlines()
  curr_count = 0
  curr_book = ""
  verse_nums = {}

  for line in lines:
    line = line.strip()
    if not line:
      continue
    parts = line.split(maxsplit=1)

    if parts[0] in books and parts[0] != curr_book:
      verse_nums[curr_book] = curr_count
      curr_count = 0
      curr_book = parts[0]

    if parts[0].isdigit():
      curr_count += 1

  verse_nums[curr_book] = curr_count
  print("Verse counts:", verse_nums)