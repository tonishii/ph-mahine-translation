import re, os

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
      # Remove anything with a parentheses, brackets, or braces and its contents
      pattern = r"\(.*?\)|\[.*?\]|\{.*?\}"
      text = re.sub(pattern, "", text)

      # Remove the footer and page number
      pattern = r"\d+ Ing Mayap a Balita Biblia New Testament © 1981, Bible © 1994, Philippine Bible Society.\s"
      text = re.sub(pattern, "", text)

      # Separates by book
      pattern = r"(?=(1\s+Juan|2\s+Juan|3\s+Juan|Juan|Nahum|Genesis|Habakuk|Exodo|Zepania|Levitico|Hageo|Ding Bilang|Zacarias|Deuteronomio|Malakias|Josue|Ukum|Mateo|Ruth|Marcos|1 Samuel|Lucas|2 Samuel|1 Ari|Ding Dapat|2 Ari|Roma|1 Cronica|1 Corinto|2 Cronica|2 Corinto|Ezra|Galacia|Nehemias|Efeso|Ester|Filipos|Job|Colosas|Ding Dalit|1 Tesalonica|Ding Kasebian|2 Tesalonica|Ecclesiastes|1 Timoteo|Ing Malagung Diling Kanta|2 Timoteo|Isaias|Tito|Jeremias|Filemon|Ding Tagulele|Hebreo|Ezekiel|Santiago|Daniel|1 Pedro|Hosea|2 Pedro|Joel|Amos|Obadias|Jonas|Judas|Mikeas|Kapahayagan)\s+\d+\s)"
      text = re.sub(pattern, "\n", text)

      # Normalizes Juan books
      pattern = r"(?<=\d\s)\n(?=Juan)"
      text = re.sub(pattern, "", text)

      # Remove the special cases
      pattern = r"\n(?=(Job 10 Kaybat|Job 1 Kanita|Exodo 1 Inyang|Jeremias 1 King|Jeremias 1 Migsalita|Jeremias 1 Gewa))"
      text = re.sub(pattern, "", text)

      # Remove the titles
      pattern = r"\s+(Nahum|Genesis|Habakuk|Exodo|Zepania|Levitico|Hageo|Ding Bilang|Zacarias|Deuteronomio|Malakias|Josue|Ukum|Mateo|Ruth|Marcos|1 Samuel|Lucas|2 Samuel|Juan|1 Ari|Ding Dapat|2 Ari|Roma|1 Cronica|1 Corinto|2 Cronica|2 Corinto|Ezra|Galacia|Nehemias|Efeso|Ester|Filipos|Job|Colosas|Ding Dalit|1 Tesalonica|Ding Kasebian|2 Tesalonica|Ecclesiastes|1 Timoteo|Ing Malagung Diling Kanta|2 Timoteo|Isaias|Tito|Jeremias|Filemon|Ding Tagulele|Hebreo|Ezekiel|Santiago|Daniel|1 Pedro|Hosea|2 Pedro|Joel|1 Juan|Amos|2 Juan|Obadias|3 Juan|Jonas|Judas|Mikeas|Kapahayagan)\s\n"
      text = re.sub(pattern, "\n", text)

      pattern = r"[ \t]+"
      text = re.sub(pattern, " ", text)

      pattern = r"(1\sJuan|2\sJuan|3\sJuan|Juan|Nahum|Genesis|Habakuk|Exodo|Zepania|Levitico|Hageo|Ding Bilang|Zacarias|Deuteronomio|Malakias|Josue|Ukum|Mateo|Ruth|Marcos|1 Samuel|Lucas|2 Samuel|1 Ari|Ding Dapat|2 Ari|Roma|1 Cronica|1 Corinto|2 Cronica|2 Corinto|Ezra|Galacia|Nehemias|Efeso|Ester|Filipos|Job|Colosas|Ding Dalit|1 Tesalonica|Ding Kasebian|2 Tesalonica|Ecclesiastes|1 Timoteo|Ing Malagung Diling Kanta|2 Timoteo|Isaias|Tito|Jeremias|Filemon|Ding Tagulele|Hebreo|Ezekiel|Santiago|Daniel|1 Pedro|Hosea|2 Pedro|Joel|Amos|Obadias|Jonas|Judas|Mikeas|Kapahayagan)\s(\d+)\s(.*?)(?=\d+\s*)"
      text = re.sub(pattern, r"\1 \2\n", text)

      # pattern = r"(?<=(1\sJuan|2\sJuan|3\sJuan|Juan|Nahum|Genesis|Habakuk|Exodo|Zepania|Levitico|Hageo|Ding Bilang|Zacarias|Deuteronomio|Malakias|Josue|Ukum|Mateo|Ruth|Marcos|1 Samuel|Lucas|2 Samuel|1 Ari|Ding Dapat|2 Ari|Roma|1 Cronica|1 Corinto|2 Cronica|2 Corinto|Ezra|Galacia|Nehemias|Efeso|Ester|Filipos|Job|Colosas|Ding Dalit|1 Tesalonica|Ding Kasebian|2 Tesalonica|Ecclesiastes|1 Timoteo|Ing Malagung Diling Kanta|2 Timoteo|Isaias|Tito|Jeremias|Filemon|Ding Tagulele|Hebreo|Ezekiel|Santiago|Daniel|1 Pedro|Hosea|2 Pedro|Joel|Amos|Obadias|Jonas|Judas|Mikeas|Kapahayagan)\s\d+\s).*(?=\d+\s*)"
      # text = re.sub(pattern, "", text)

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