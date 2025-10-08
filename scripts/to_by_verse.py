import re, os, sys, pandas as pd

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

def to_excel(text, name):
  lines: list[str] = [line.strip() for line in text.splitlines() if line.strip()]
  verses = []
  current_book, current_chapter = "N/A", "N/A"

  for line in lines:
    match = re.match(r"^(.{3,25})\s(\d+)$", line)
    if match:
      current_book, current_chapter = match.groups()
    else:
      try:
        p1, p2 = line.split(None, 1)
      except:
        print(f"Error in processing {name}:", line)
        return

      verses.append({
        "Book": current_book.strip(),
        "Chapter": int(current_chapter),
        "Verse": str(p1.strip()),
        "Text": p2.strip()
      })

  if verses:
    df = pd.DataFrame(verses)
    excel_path = os.path.join("data/by_verse", f"{codes.get(name)}.xlsx")
    df.to_excel(excel_path, index=False)
    print(f"{excel_path} ✓")

  else:
    print("Error: No excel.")

def main():
  dir_path = "data/raw"

  if not sys.argv[1:]:
    for dir_name in os.listdir(dir_path):
      if dir_name.startswith("."): continue

      if not os.path.exists(f"data/processed/{codes.get(dir_name)}.txt"):
        filename = f"{codes.get(dir_name)}.txt"
        # print(f"File not found: {os.path.join("data/processed/",filename)}")
        continue

      with open(f"data/processed/{codes.get(dir_name)}.txt", "r", encoding="utf-8") as f:
        text = f.read()

        to_excel(text, dir_name)

  else:
    for argv in sys.argv[1:]:
      if not os.path.exists(f"data/processed/{codes.get(argv)}.txt"):
        filename = f"{codes.get(argv)}.txt"
        # print(f"File not found: {os.path.join("data/processed/",filename)}")
        continue

      with open(f"data/processed/{codes.get(argv)}.txt", "r", encoding="utf-8") as f:
        text = f.read()

        to_excel(text, argv)

if __name__ == "__main__":
  main()