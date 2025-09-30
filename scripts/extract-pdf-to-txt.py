import os
from pypdf import PdfReader

dir_path = "data/raw/"

for dir_name in os.listdir(dir_path):
  if dir_name.startswith("."): continue

  full_path = os.path.join(dir_path, dir_name)

  reader = PdfReader(full_path + "/bible.pdf")
  text = "\n".join(page.extract_text() for page in reader.pages)
  with open(full_path + "/bible.txt", "w", encoding="utf-8") as f:
    f.write(text)

  print(full_path + ": " + str(len(reader.pages)))