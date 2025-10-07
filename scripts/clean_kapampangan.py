import re
from collections import defaultdict

def clean_kapampangan(text):
  # Remove anything with a parentheses or braces and its contents
  pattern = r"\(.*?\)|\{.*?\}"
  text = re.sub(pattern, "", text)

  # Remove brackets but keep the contents
  pattern = r"\[(.*?)\]"
  text = re.sub(pattern, r"\1", text)

  # Remove the last section of the Bible
  pattern = r"Esclarecimento(.|\n)*"
  text = re.sub(pattern, "", text)

  # Remove the footer and page number
  pattern = r"\d+ Ing Mayap a Balita Biblia New Testament © 1981, Bible © 1994, Philippine Bible Society.\s"
  text = re.sub(pattern, "", text)

  # Separate by book
  pattern = r"(?=(1\s+Juan|2\s+Juan|3\s+Juan|Juan|Nahum|Genesis|Habakuk|Exodo|Zepania|Levitico|Hageo|Ding Bilang|Zacarias|Deuteronomio|Malakias|Josue|Ukum|Mateo|Ruth|Marcos|1 Samuel|Lucas|2 Samuel|1 Ari|Ding Dapat|2 Ari|Roma|1 Cronica|1 Corinto|2 Cronica|2 Corinto|Ezra|Galacia|Nehemias|Efeso|Ester|Filipos|Job|Colosas|Ding Dalit|1 Tesalonica|Ding Kasebian|2 Tesalonica|Ecclesiastes|1 Timoteo|Ing Malagung Diling Kanta|2 Timoteo|Isaias|Tito|Jeremias|Filemon|Ding Tagulele|Hebreo|Ezekiel|Santiago|Daniel|1 Pedro|Hosea|2 Pedro|Joel|Amos|Obadias|Jonas|Judas|Mikeas|Kapahayagan)\s+\d+\s)"
  text = re.sub(pattern, "\n", text)

  # Normalizes Juan books
  pattern = r"(?<=\d\s)\n(?=Juan)"
  text = re.sub(pattern, "", text)

  # Remove the special cases
  pattern = r"\n(Job 10 Kaybat|Job 1 Kanita|Exodo 1 Inyang|Jeremias 1 King|Jeremias 1 Migsalita|Jeremias 1 Gewa|Judas  3 Inyang|Roma 22 Inya|Isaias 1 Ikit)"
  text = re.sub(pattern, "", text)

  pattern = r"\sKapampangan.*"
  text = re.sub(pattern, "", text)

  # Remove the titles
  pattern = r"\s+(Nahum|Genesis|Habakuk|Exodo|Zepania|Levitico|Hageo|Ding Bilang|Zacarias|Deuteronomio|Malakias|Josue|Ukum|Mateo|Ruth|Marcos|1 Samuel|Lucas|2 Samuel|Juan|1 Ari|Ding Dapat|2 Ari|Roma|1 Cronica|1 Corinto|2 Cronica|2 Corinto|Ezra|Galacia|Nehemias|Efeso|Ester|Filipos|Job|Colosas|Ding Dalit|1 Tesalonica|Ding Kasebian|2 Tesalonica|Ecclesiastes|1 Timoteo|Ing Malagung Diling Kanta|2 Timoteo|Isaias|Tito|Jeremias|Filemon|Ding Tagulele|Hebreo|Ezekiel|Santiago|Daniel|1 Pedro|Hosea|2 Pedro|Joel|1 Juan|Amos|2 Juan|Obadias|3 Juan|Jonas|Judas|Mikeas|Kapahayagan)\s\n"
  text = re.sub(pattern, "\n", text)

  # Normalize spacing
  pattern = r"[ \t]+"
  text = re.sub(pattern, " ", text)

  # Remove everything from the book title to the first verse number
  pattern = r"(1\sJuan|2\sJuan|3\sJuan|Juan|Nahum|Genesis|Habakuk|Exodo|Zepania|Levitico|Hageo|Ding Bilang|Zacarias|Deuteronomio|Malakias|Josue|Ukum|Mateo|Ruth|Marcos|1 Samuel|Lucas|2 Samuel|1 Ari|Ding Dapat|2 Ari|Roma|1 Cronica|1 Corinto|2 Cronica|2 Corinto|Ezra|Galacia|Nehemias|Efeso|Ester|Filipos|Job|Colosas|Ding Dalit|1 Tesalonica|Ding Kasebian|2 Tesalonica|Ecclesiastes|1 Timoteo|Ing Malagung Diling Kanta|2 Timoteo|Isaias|Tito|Jeremias|Filemon|Ding Tagulele|Hebreo|Ezekiel|Santiago|Daniel|1 Pedro|Hosea|2 Pedro|Joel|Amos|Obadias|Jonas|Judas|Mikeas|Kapahayagan)\s(\d+)\s(.*?)(?=\d+\s*)"
  text = re.sub(pattern, r"\1 \2\n", text)

  pattern = r"\d+([.,;:!?])\d*"
  text = re.sub(pattern, r"\1", text)

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

  # CORRECTIONS:
  pattern = r"([eE]) n e"
  text = re.sub(pattern, r"\1 ne", text)

  # verify(text)
  return text

def verify(text):
  pattern = r"(Nahum|Genesis|Habakuk|Exodo|Zepania|Levitico|Hageo|Ding Bilang|Zacarias|Deuteronomio|Malakias|Josue|Ukum|Mateo|Ruth|Marcos|1 Samuel|Lucas|2 Samuel|Juan|1 Ari|Ding Dapat|2 Ari|Roma|1 Cronica|1 Corinto|2 Cronica|2 Corinto|Ezra|Galacia|Nehemias|Efeso|Ester|Filipos|Job|Colosas|Ding Dalit|1 Tesalonica|Ding Kasebian|2 Tesalonica|Ecclesiastes|1 Timoteo|Ing Malagung Diling Kanta|2 Timoteo|Isaias|Tito|Jeremias|Filemon|Ding Tagulele|Hebreo|Ezekiel|Santiago|Daniel|1 Pedro|Hosea|2 Pedro|Joel|1 Juan|Amos|2 Juan|Obadias|3 Juan|Jonas|Judas|Mikeas|Kapahayagan)\s(\d+)\n"
  chapter_counts = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66, 52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4, 28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22]

  chapters = re.findall(pattern, text)

  book_chapters = defaultdict(list)
  for book, chap in chapters:
    book_chapters[book].append(int(chap))

  for ((book, chaps), count) in zip(book_chapters.items(), chapter_counts):
    if count == len(chaps):
      print(f"{book} chapters ({len(chaps)}) in order ✓")
    else:
      print(f"{book} chapters ({len(chaps)} SHOULD BE {count}) NOT in order x")