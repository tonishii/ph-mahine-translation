import re
from collections import defaultdict

books = [
  "Genesis", "Exodo", "Levitico", "Numeros", "Deuteronomio", "Josue",
  "Mga Maghuhukom", "Ruth", "1 Samuel", "2 Samuel", "1 Mga Hari",
  "2 Mga Hari", "1 Cronicas", "2 Cronicas", "Esdras", "Nehemias",
  "Ester", "Job", "Mga Salmo", "Mga Panultihon", "Ecclesiastes",
  "Awit sa mga Awit", "Isaias", "Jeremias", "Mga Pagbangotan",
  "Ezequiel", "Daniel", "Oseas", "Joel", "Amos", "Abdias", "Jonas",
  "Miqueas", "Nahum", "Habacuc", "Sofonias", "Hageo", "Zacarias",
  "Malaquias", "Mateo", "Marcos", "Lucas", "Juan", "Mga Buhat",
  "Mga Taga-Roma", "1 Mga Taga-Corinto", "2 Mga Taga-Corinto",
  "Mga Taga-Galacia", "Mga Taga-Efeso", "Mga Taga-Filipos", "Mga Taga-Colosas",
  "1 Mga Taga-Tesalonica", "2 Mga Taga-Tesalonica", "1 Timoteo",
  "2 Timoteo", "Tito", "Filemon", "Mga Hebreo", "Santiago", "1 Pedro",
  "2 Pedro", "1 Juan", "2 Juan", "3 Juan", "Judas", "Gipadayag"
]

def clean_cebuano(text):
  pattern = r"\s*(?=\n)"
  text = re.sub(pattern, "", text)

  # Removes the first newline
  pattern = r"^\n"
  text = re.sub(pattern, "", text)

  # Remove anything with a parentheses and its contents
  pattern = r"\(.*?\)"
  text = re.sub(pattern, "", text)

  # Remove brackets but keep the contents
  pattern = r"\[(.*?)\]"
  text = re.sub(pattern, r"\1", text)

  # Remove the last section of the Bible
  pattern = r"Esclarecimento(.|\n)*"
  text = re.sub(pattern, "", text)

  # Remove the footer and page number
  pattern = r"\d*\nAng Bag-ong Maayong Balita Biblia\n© 1999, Philippine Bible Society.\n"
  text = re.sub(pattern, "", text)

  # Removes special cases
  pattern = r"(Cebuano.*All Bible\s*|(20[1-9]|2[1-9]\d|[3-9]\d{2,}))"
  text = re.sub(pattern, "", text)

  # Puts everything that doesnt start with a number in the previous line
  pattern = r"\n(?!\d+)"
  text = re.sub(pattern, " ", text)

  # Normalize spacing behind book
  pattern = rf"\s+(?=({"|".join(books)})\s+\d+)"
  text = re.sub(pattern, "\n", text)

  # Remove the titles
  pattern = rf"\s+({"|".join(books)})\n"
  text = re.sub(pattern, "\n", text)

  # Normalize spacing
  pattern = r"[ \t]+"
  text = re.sub(pattern, " ", text)

  pattern = r"\d+([.,;:!?])\d*"
  text = re.sub(pattern, r"\1", text)

  # Normalizes spacing before a punctuation mark
  pattern = r'\s+([.,;:!?])'
  text = re.sub(pattern, "", text)

  # Normalizes spacing after a verse number (Sometimes verses are in ranges e.g. 4-5)
  pattern = r"(?<=\d)\s*(?=[^0-9-])"
  text = re.sub(pattern, " ", text)

  pattern = r"\s*(?=\n)"
  text = re.sub(pattern, "", text)

  # Remove unnecessary titles
  pattern = rf"({"|".join(books)})(?=\n)"
  text = re.sub(pattern, "", text)

  # Remove everything from the book title to the first verse number
  pattern = rf"({"|".join(books)})\s(\d+)(.*?)(?=\n\d+\s*)"
  text = re.sub(pattern, r"\1 \2\n", text)

  pattern = r"\s*(?=\n)"
  text = re.sub(pattern, "", text)

  pattern = r"\n\d\n"
  text = re.sub(pattern, "\n", text)

  # verify(text)
  return text

def verify(text: str):
  pattern = rf"({"|".join(books)})\s(\d+)"
  chapter_counts = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66, 52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4, 28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22]

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