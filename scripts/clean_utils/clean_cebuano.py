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
  text = re.sub(r"(?s)^.*?\bGenesis\s*1\b", "Genesis 1", text, count=1)

  book_pattern = "|".join(books)

  pattern = r"\s*(?=\n)"
  text = re.sub(pattern, "", text)

  # Removes the first newline
  pattern = r"^\n"
  text = re.sub(pattern, "", text)

  # Remove anything with a parentheses and its contents
  pattern = r"\(.*?\)"
  text = re.sub(pattern, "", text, flags=re.S)

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
  pattern = r"(Cebuano.*All Bible\s*|(20[1-9]|2[1-9]\d|[3-9]\d{2,})|(?<=\n)139\n|(?<=\n)138\n)"
  text = re.sub(pattern, "", text)

  # Puts everything that doesnt start with a number in the previous line
  pattern = r"\n(?!\d+)"
  text = re.sub(pattern, " ", text)

  # Normalize spacing behind book
  pattern = rf"\s+(?=({book_pattern})\s+\d+)"
  text = re.sub(pattern, "\n", text)

  # Remove the titles
  pattern = rf"\s+({book_pattern})\n"
  text = re.sub(pattern, "\n", text)

  # Normalize spacing
  pattern = r"[ \t]+"
  text = re.sub(pattern, " ", text)

  pattern = r"\d+([.,;:!?])\d*"
  text = re.sub(pattern, r"\1", text)

  # Normalizes spacing before a punctuation mark
  pattern = r"\s+([.,;:!?])"
  text = re.sub(pattern, "", text)

  # Normalizes spacing after a verse number (Sometimes verses are in ranges e.g. 4-5)
  pattern = r"(?<=\d)\s*(?=[^0-9-])"
  text = re.sub(pattern, " ", text)

  pattern = r"\s*(?=\n)"
  text = re.sub(pattern, "", text)

  # Remove unnecessary titles
  pattern = rf"({book_pattern})(?=\n)"
  text = re.sub(pattern, "", text)

  # Remove everything from the book title to the first verse number
  pattern = rf"({book_pattern})\s(\d+)(.*?)(?=\n\d+\s*)"
  text = re.sub(pattern, r"\1 \2\n", text)

  pattern = r"\s*(?=\n)"
  text = re.sub(pattern, "", text)

  pattern = r"\n\d\n"
  text = re.sub(pattern, "\n", text)

  pattern = r"[^.]\n(?=100)"
  text = re.sub(pattern, " ", text)

  pattern = r"\s\n(?=50\ska)"
  text = re.sub(pattern, " ", text)

  pattern = r"(?<=as)\n(?=50\s)"
  text = re.sub(pattern, " ", text)

  # verify(text)
  text = fix_verse(text)
  # verify(text)
  return text, books

def fix_verse(text):
  book_pattern = "|".join(books)
  lines = text.splitlines()
  curr_book = ""
  curr_chapter = None
  last_verse = 0
  book_chapters = defaultdict(list)

  for line in lines:
    line = line.strip()
    if not line:
      continue

    match = re.match(rf"({book_pattern})\s(\d+)", line)

    if match:
      curr_book, chap_str = match.groups()
      curr_chapter = int(chap_str)
      last_verse = 0
      book_chapters[curr_book].append(curr_chapter)
      continue

    if re.match(r"^\d+(-(\d+))*\s", line):
      verse_num = int(re.match(r"^(\d+)", line).group(1)) # type: ignore
      match = re.match(r"^(\d+)-(\d+)", line)
      if match:
        verse_num, _= match.groups()
        verse_num = int(verse_num)
      #future_verse = int (re.match)
      if verse_num < last_verse:
        pattern = rf"\n({last_verse}\s(.*))\n({verse_num}(.*))"
        text = re.sub(pattern, r" \1 \n\3", text)
      last_verse = verse_num

  return text

def verify(text: str):
  book_pattern = "|".join(books)
  chapter_counts = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66, 52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4, 28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22]

  chapter_counts_dict = { book: count for (book, count) in zip(books, chapter_counts)}
  lines = text.splitlines()
  curr_book = ""
  curr_chapter = None
  last_verse = 0
  book_chapters = defaultdict(list)

  issues = []

  for line in lines:
      line = line.strip()
      if not line:
          continue

      match = re.match(rf"({book_pattern})\s+(\d+)", line)

      if match:
          curr_book, chap_str = match.groups()
          curr_chapter = int(chap_str)
          last_verse = 0
          book_chapters[curr_book].append(curr_chapter)
          continue

      if re.match(r"^\d+\s", line):
          verse_num = int(re.match(r"^(\d+)", line).group(1)) # type: ignore
          if verse_num < last_verse:
              issues.append(f"Verse out of order in {curr_book} {curr_chapter}: {last_verse} → {verse_num}")
          elif verse_num == last_verse:
              issues.append(f"Duplicate verse in {curr_book} {curr_chapter}: {verse_num}")
          last_verse = verse_num

  for book, chaps in book_chapters.items():
      expected = chapter_counts_dict.get(book, None)
      if expected and len(set(chaps)) == expected:
          print(f"{book} chapters ({len(chaps)}) in order ✓")
      else:
          print(f"{book} chapters ({len(set(chaps))} should be {expected}) NOT in order x")

  if issues:
      print("\n--- Chronology Issues ---")
      for i in issues:
          print(i)
  else:
      print("\nAll verses are in chronological order ✓")
