import re, os
from char_ngrams import char_ngrams

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

def to_remove_punctuations(text, name):
  text = re.sub(r"[^A-Za-zÀ-ÿ\s'-]", "", text, flags=re.UNICODE)

  os.makedirs("data/no_punctuation", exist_ok=True)
  file_path = os.path.join("data/no_punctuation", f"{codes.get(name)}.txt")
  with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

  char_ngrams(text, name)
  print(f"counts/lexical/{codes.get(name)}.txt: {name} ✓")