import re, os
from clean_kapampangan import clean_kapampangan

def clean_file(path, dir_name):
  with open(path + "/bible.txt", "r", encoding="utf-8") as f:
    text = f.read()

    pattern = r"\n\s*\n" # Removes unnecessary newlines
    text = re.sub(pattern, "\n", text)

    pattern = r"\s+"
    text = re.sub(pattern, " ", text)

    # Removes everything until first chapter
    pattern = r"^(.*?)(?=Genesis\s+1\s)"
    text = re.sub(pattern, "", text)

    if dir_name == "kapampangan":
      text = clean_kapampangan(text)

    if dir_name == "tausug":
      pattern = r"^(.*?)(?=Matiyu\s+1\s)"
      text = re.sub(pattern, "", text)

    if dir_name == "yami":
      pattern = r"^(.*?)(?=Matay\s+1\s)"
      text = re.sub(pattern, "", text)

    if dir_name == "pangasinan":
      pattern = r"^(.*?)(?=Mateo\s+1\s)"
      text = re.sub(pattern, "", text)

    if dir_name == "maranao":
      pattern = r"^(.*?)(?=Maksod\s+1\s)"
      text = re.sub(pattern, "", text)

    if dir_name == "chavacano":
      pattern = r"^(.*?)(?=Mateo 1:1 1 Mateo 2:1)"
      text = re.sub(pattern, "", text)

    if dir_name == "english":
      pattern = r"¶\s+"
      text = re.sub(pattern, "", text)
      pattern = r"\s+[;]"
      text = re.sub(pattern, ";", text)
      pattern = r"\s+[:]"
      text = re.sub(pattern, "", text)
      pattern = r"(\b\d+\b(\s+\d+\b)+)"
      text = re.sub(pattern, "", text)
      pattern = r"\s+([?.!,;:])"
      text = re.sub(pattern, r'\1', text)

    out_dir = f"data/processed/{dir_name}"
    os.makedirs(out_dir, exist_ok=True)
    with open(out_dir + "/bible_clean.txt", "w", encoding="utf-8") as f:
      f.write(text)
    print(out_dir + "/bible_clean.txt ✓")

def main():
  dir_path = "data/raw/"
  for dir_name in os.listdir(dir_path):
    if dir_name.startswith("."): continue

    full_path = os.path.join(dir_path, dir_name)

    clean_file(full_path, dir_name)

if __name__ == "__main__":
  main()