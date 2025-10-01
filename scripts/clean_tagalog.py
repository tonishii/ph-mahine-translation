import re
from collections import defaultdict

books = [
  "Genesis", "Exodus", "Leviticus", "Bilang", "Deuteronomio", "Josue", "Hukom", "Ruth",
  "1 Samuel", "2 Samuel", "1 Hari", "2 Hari", "1 Cronica", "2 Cronica", "Ezra", "Nehemias",
  "Ester", "Job", "Salmo", "Kawikaan", "Mangangaral", "Awit", "Isaias", "Jeremias",
  "Panaghoy", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadias", "Jonas", "Micas",
  "Nahum", "Habakuk", "Zefanias", "Hageo", "Zacarias", "Malakias", "Mateo", "Marcos",
  "Lucas", "Juan", "Gawa", "Roma", "1 Corinto", "2 Corinto", "Galacia", "Efeso", "Filipos",
  "Colosas", "1 Tesalonica", "2 Tesalonica", "1 Timoteo", "2 Timoteo", "Tito", "Filemon",
  "Hebreo", "Santiago", "1 Pedro", "2 Pedro", "1 Juan", "2 Juan", "3 Juan", "Judas", "Pahayag"
]

def clean_tagalog(text):

  # Remove anything with a parentheses or braces and its contents
  pattern = r"\(.*?\)"
  text = re.sub(pattern, "", text)

  # Remove brackets but keep the contents
  pattern = r"\[(.*?)\]"
  text = re.sub(pattern, r"\1", text)

  # Remove the last section of the Bible
  pattern = r"Esclarecimento(.|\n)*"
  text = re.sub(pattern, "", text)

  # Remove the footer and page number
  pattern = r"\d*\s*(Ang Salita ng Dios\s+\(Tagalog Contemporary Bible\) © 2009, 2011, 2014, 2015 by Biblica, Inc. ®.|Ang Salita ng Dios\s+© 2009, 2011, 2014, 2015 by Biblica, Inc. ®.|© 2009, 2011, 2014, 2015 by Biblica, Inc. ®.)\s"
  text = re.sub(pattern, "", text)

  # Separate by book
  pattern = rf"(?=({"|".join(books)})\s+\d+\s)"
  text = re.sub(pattern, "\n", text)

  # Normalizes Juan books
  pattern = r"(?<=\d\s)\n(?=Juan)"
  text = re.sub(pattern, "", text)

  # Remove the special cases
  pattern = r"\n(Ezra 1 Sinabi|Habakuk 2 Sinabi|Habakuk 5 Sumagot|Habakuk 12 Sinabi|Jeremias 23 PANGINOON|Jeremias 1 PANGINOON|Roma 22\s)"
  text = re.sub(pattern, "", text)

  # Removes special cases
  pattern = r"Filipino.*All Bible\s*"
  text = re.sub(pattern, "", text)

  # Remove the titles
  pattern = rf"\s+({"|".join(books)})\s\n"
  text = re.sub(pattern, "\n", text)

  # Normalize spacing
  pattern = r"[ \t]+"
  text = re.sub(pattern, " ", text)

  # Remove everything from the book title to the first verse number
  pattern = rf"({"|".join(books)})\s(\d+)\s(.*?)(?=\d+\s*)"
  text = re.sub(pattern, r"\1 \2\n", text)

  # Separates by verse
  pattern = r"\s(?=\d+)"
  text = re.sub(pattern, "\n", text)

  # Removes the first newline
  pattern = r"^\n"
  text = re.sub(pattern, "", text)

  # Normalizes spacing before a punctuation mark
  pattern = r'\s+([.,;:!?])'
  text = re.sub(pattern, "", text)

  # Normalizes spacing after a number
  pattern = r"(?<=\d)(?=[a-zA-Z])"
  text = re.sub(pattern, " ", text)

  # Normalizes chapter number so its beside the book
  pattern = r"([a-zA-Z]+)\n(\d+)\n"
  text = re.sub(pattern, r"\1 \2\n", text)

  verify(text)
  return text

def verify(text):
  pattern = rf"({"|".join(books)})\s(\d+)\n"
  chapter_counts = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66, 52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4]

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
