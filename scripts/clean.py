import re, os, sys
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

def clean_file(path, dir_name):
  with open(path + "/bible.txt", "r", encoding="utf-8") as f:
    text = f.read()

    # Removes unnecessary newlines
    pattern = r"\n\s*\n"
    text = re.sub(pattern, "\n", text)

    # Removes everything until first chapter
    pattern = r"^(.*?)(?=Genesis\s+1\s)"
    text = re.sub(pattern, "", text)

    # Normalize spacing
    if dir_name not in ["cebuano", "ilocano", "espanol"]:
      pattern = r"\s+"
      text = re.sub(pattern, " ", text)

    if dir_name == "cebuano":
      # Removes everything until first chapter
      text = re.sub(r"(?s)^.*?\bGenesis\s*1\b", "Genesis 1", text, count=1)
      text = clean_cebuano(text)

    if dir_name == "ilocano":
      text = re.sub(r"(?s)^.*?\bGenesis\s*1\b", "Genesis 1", text, count=1)
      text = clean_ilocano(text)

    if dir_name == "espanol":
      text = clean_espanol(text)

    if dir_name == "tagalog":
      text = clean_tagalog(text)

    if dir_name == "kapampangan":
      text = clean_kapampangan(text)

    if dir_name == "tausug":
      pattern = r"^(.*?)(?=Matiyu\s+1\s)"
      text = re.sub(pattern, "", text)

    if dir_name == "yami":
      text = clean_yami(text)

    if dir_name == "pangasinan":
      text = clean_pangasinese(text)

    if dir_name == "waray":
      text = clean_waray(text)

    if dir_name == "maranao":
      pattern = r"^(.*?)(?=Maksod\s+1\s)"
      text = re.sub(pattern, "", text)

    if dir_name == "chavacano":
      pattern = r"^(.*?)(?=Mateo 1:1 1 Mateo 2:1)"
      text = re.sub(pattern, "", text)

    if dir_name == "hiligaynon":
      text = clean_hiligaynon(text)
    
    if dir_name == "bicolano":
      text = clean_bicolano(text)
      
    if dir_name == "kalanguya":
      text = clean_kalanguya(text)
    
    if dir_name == "english":
      text = clean_english(text)

    if dir_name == "tausug":
      text = clean_tausug(text)

    out_dir = f"data/processed/{dir_name}"
    os.makedirs(out_dir, exist_ok=True)
    with open(out_dir + "/bible_clean.txt", "w", encoding="utf-8") as f:
      f.write(text)

    print(out_dir + "/bible_clean.txt ✓")

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