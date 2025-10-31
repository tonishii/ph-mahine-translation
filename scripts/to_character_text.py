import re, os, textwrap

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

def to_char(text, name):
  text = text.lower().strip()
  text = " ". join(text.split())
  char_text = " ".join(list(text))
  wrapped_lines = textwrap.wrap(char_text, width=1000)

  os.makedirs("data/char_text", exist_ok=True)
  file_path = os.path.join("data/char_text", f"{codes.get(name)}.txt")
  with open(file_path, "w", encoding="utf-8") as f:
    f.write(char_text)