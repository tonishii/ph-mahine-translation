import re, os
from collections import Counter

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

def char_ngrams(text, name, n=3):
  text = re.sub(r"\s+", "", text.lower())

  os.makedirs("counts/lexical", exist_ok=True)
  file_path = os.path.join("counts/lexical", f"{codes.get(name)}.txt")
  with open(file_path, "w", encoding="utf-8") as f:
    for n in range(n, 0, -1):
        ngrams = Counter([text[i:i+n] for i in range(len(text)-n+1)])
        for ng, freq in ngrams.most_common():
            f.write(f"{ng}\t{freq}\n")
        f.write("\n")

  print(f"counts/char_text/{codes.get(name)}.txt: {name} ✓")