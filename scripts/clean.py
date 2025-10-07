import re, os, sys
import pandas as pd
from clean_kapampangan import clean_kapampangan
from clean_tagalog import clean_tagalog
from clean_hiligaynon import clean_hiligaynon
from clean_pangasinese import clean_pangasinese
from clean_waray import clean_waray
from clean_bicolano import clean_bicolano
from clean_kalanguya import clean_kalanguya
from clean_tausug import clean_tausug
from clean_yami import clean_yami
from clean_ilocano import clean_ilocano
from clean_cebuano import clean_cebuano
from clean_espanol import clean_espanol
from clean_english import clean_english

codes = {
  "english": "ENG",
  "spanish": "SPA",
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
}

def to_excel(text, books, out_dir):
    name = out_dir[len("data/processed/"):]
    
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    verses = []
    current_book, current_chapter = None, None

    book_pattern = "|".join(re.escape(book) for book in books)
    book_regex = re.compile(rf"^({book_pattern})\s+(\d+)$")

    for line in lines:
        match = book_regex.match(line)
        if match:
            current_book, current_chapter = match.groups()
            continue

        match = re.match(r"^(\d+(?:-\d+)?)\s+(.*)", line)
        if match and current_book and current_chapter:
            verse, verse_text = match.groups()
            verses.append({
                "Book": current_book.strip(),
                "Chapter": int(current_chapter),
                "Verse #": verse.strip(),
                "Text": verse_text.strip()
            })

    if verses:
        df = pd.DataFrame(verses)
        excel_path = os.path.join("data/by_verse", f"{codes.get(name)}.xlsx")
        df.to_excel(excel_path, index=False)
        print(f"{excel_path}")
    else:
        print("Error no excel")  

def to_sentence(text, books, out_dir):
    name = out_dir[len("data/processed/"):]
    book_pattern = "|".join(re.escape(book) for book in books)
    text = re.sub(rf"\b(?:{book_pattern})\s+\d+\b", "", text)
    
    text = re.sub(r"^\s*\d+(?:-\d+)?\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text).strip()
    
    text = re.sub(r'(?<=[.!?]["”])\s+(?=[A-Z])', "\n", text)
    text = re.sub(r'(?<=[.!?])\s+(?=[A-Z])', "\n", text)
    
    os.makedirs("data/by_sentence", exist_ok=True)
    file_path = os.path.join("data/by_sentence", f"{codes.get(name)}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
      f.write(text)

def clean_file(path, dir_name):
  with open(path + "/bible.txt", "r", encoding="utf-8") as f:
    text = f.read()

    # Removes unnecessary newlines
    pattern = r"\n\s*\n"
    text = re.sub(pattern, "\n", text)
    
    # Normalize spacing
    if dir_name not in ["cebuano", "ilocano", "espanol"]:
      pattern = r"\s+"
      text = re.sub(pattern, " ", text)

    # Removes everything until first chapter
    pattern = r"^(.*?)(?=Genesis\s+1\s)"
    text = re.sub(pattern, "", text)

    books = []
    
    if dir_name == "cebuano":
      # Removes everything until first chapter
      text = re.sub(r"(?s)^.*?\bGenesis\s*1\b", "Genesis 1", text, count=1)
      text, books = clean_cebuano(text)

    if dir_name == "ilocano":
      text = re.sub(r"(?s)^.*?\bGenesis\s*1\b", "Genesis 1", text, count=1)
      text, books = clean_ilocano(text)

    if dir_name == "espanol":
      text, books = clean_espanol(text)

    if dir_name == "tagalog":
      text, books = clean_tagalog(text)

    if dir_name == "kapampangan":
      text, books = clean_kapampangan(text)

    if dir_name == "tausug":
      pattern = r"^(.*?)(?=Matiyu\s+1\s)"
      text = re.sub(pattern, "", text)
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
      pattern = r"^(.*?)(?=Mateo 1:1 1 Mateo 2:1)"
      text = re.sub(pattern, "", text)

    if dir_name == "hiligaynon":
      text, books = clean_hiligaynon(text)
    
    if dir_name == "bicolano":
      text, books = clean_bicolano(text)
      
    if dir_name == "kalanguya":
      text, books = clean_kalanguya(text)
    
    if dir_name == "english":
      text, books = clean_english(text)

    out_dir = f"data/processed/{dir_name}"
    os.makedirs(out_dir, exist_ok=True)
    with open(out_dir + "/bible_clean.txt", "w", encoding="utf-8") as f:
      f.write(text)

    print(out_dir + "/bible_clean.txt ✓")
    to_excel(text, books, out_dir)
    to_sentence(text, books, out_dir)

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