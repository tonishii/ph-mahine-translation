import re, os

def clean_file(path, dir_name):
  with open(path + "/bible.txt", "r", encoding="utf-8") as f:
    text = f.read()

    pattern = r"\n\s*\n"
    text = re.sub(pattern, "\n", text)

    pattern = r"\s+"
    text = re.sub(pattern, " ", text)

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