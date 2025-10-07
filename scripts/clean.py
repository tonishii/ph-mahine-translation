import re, os, sys
from clean_utils.clean_kapampangan import clean_kapampangan
from clean_utils.clean_tagalog import clean_tagalog
from clean_utils.clean_hiligaynon import clean_hiligaynon
from clean_utils.clean_pangasinese import clean_pangasinese
from clean_utils.clean_waray import clean_waray
from clean_utils.clean_tuwali import clean_tuwali
from clean_utils.clean_bicolano import clean_bicolano
from clean_utils.clean_kalanguya import clean_kalanguya
from clean_utils.clean_tausug import clean_tausug
from clean_utils.clean_yami import clean_yami
from clean_utils.clean_ilocano import clean_ilocano
from clean_utils.clean_cebuano import clean_cebuano
from clean_utils.clean_espanol import clean_espanol
from clean_utils.clean_english import clean_english
from clean_utils.clean_chavacano import clean_chavacano
from to_by_sentence import to_sentence

codes = {
  "english": "ENG",
  "espanol": "SPA",
  "yami": "TAO",
  "tagalog": "TGL",
  "cebuano": "CEB",
  "ilocano": "ILO",
  "kapampangan": "PAM",
  "hiligaynon": "HIL",
  "waray": "WAR",
  "pangasinense": "PAG",
  "bicolano": "BCL",
  "tausug": "TSG",
  "kalanguya": "KAK",
  "chavacano": "CBK",
  "tuwali": "IFK",
}

def clean_file(path, dir_name):
  with open(path + "/bible.txt", "r", encoding="utf-8") as f:
    text = f.read()

    # Removes unnecessary newlines
    pattern = r"\n\s*\n"
    text = re.sub(pattern, "\n", text)

    pattern = r"-\d+-"
    text = re.sub(pattern, "", text)

    # Normalize spacing
    if dir_name not in ["cebuano", "ilocano", "espanol", "tagalog", "chavacano"]:
      pattern = r"\s+"
      text = re.sub(pattern, " ", text)

    # Removes everything until first chapter
    pattern = r"^(.*?)(?=Genesis\s+1\s)"
    text = re.sub(pattern, "", text)

    books = []

    if dir_name == "cebuano":
      text, books = clean_cebuano(text)

    if dir_name == "ilocano":
      text, books = clean_ilocano(text)

    if dir_name == "espanol":
      text, books = clean_espanol(text)

    if dir_name == "tagalog":
      text, books = clean_tagalog(text)

    if dir_name == "kapampangan":
      text, books = clean_kapampangan(text)

    if dir_name == "tausug":
      text, books = clean_tausug(text)

    if dir_name == "yami":
      text, books = clean_yami(text)

    if dir_name == "pangasinan":
      text, books = clean_pangasinese(text)

    if dir_name == "waray":
      text, books = clean_waray(text)

    if dir_name == "maranao":
      pattern = r"^(.*?)(?=Maksod\s+1\s)"
      text = re.sub(pattern, "", text)

    if dir_name == "chavacano":
      text, books = clean_chavacano(text)

    if dir_name == "hiligaynon":
      text, books = clean_hiligaynon(text)

    if dir_name == "bicolano":
      text, books = clean_bicolano(text)

    if dir_name == "kalanguya":
      text, books = clean_kalanguya(text)

    if dir_name == "english":
      text, books = clean_english(text)

    if dir_name == "tuwali":
      text = clean_tuwali(text)

    with open(f"data/processed/{codes.get(dir_name)}.txt", "w", encoding="utf-8") as f:
      f.write(text)

    print(f"data/processed/{codes.get(dir_name)}.txt: {dir_name} ✓")
    to_sentence(text, books, dir_name)
    print(f"data/by_sentence/{codes.get(dir_name)}.txt: {dir_name} ✓")


def main():
  dir_path = "data/raw/"

  if not sys.argv[1:]:
    for dir_name in os.listdir(dir_path):
      if dir_name.startswith("."): continue

      full_path = os.path.join(dir_path, dir_name)

      if not os.path.exists(full_path + "/bible.txt"):
        print(f"File not found: {os.path.join(full_path, 'bible.txt')}")
        continue

      clean_file(full_path, dir_name)
  else:
    for argv in sys.argv[1:]:
      full_path = os.path.join(dir_path, argv)

      if not os.path.exists(full_path + "/bible.txt"):
        print(f"File not found: {os.path.join(full_path, 'bible.txt')}")
        continue

      clean_file(full_path, argv)

if __name__ == "__main__":
  main()