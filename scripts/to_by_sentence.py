import re, os

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

def to_sentence(text, books, name):
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