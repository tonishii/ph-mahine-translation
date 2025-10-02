import re
from collections import defaultdict

def clean_waray(text):
    old_testament_books = [
        "Genesis", "Exodus", "Leviticus", "Numero", "Deuteronomio",
        "Josue", "Hukom", "Ruth", "1 Samuel", "2 Samuel",
        "1 Hari", "2 Hari", "1 Cronica", "2 Cronica", "Ezra", "Nehemias", "Ester",
        "Job", "Salmo", "Hulubaton", "Manugwali", "Kanta", "Isaias", "Jeremias",
        "Panalambiton", "Ezekiel", "Daniel", "Hoseas", "Joel", "Amos", "Obadias", "Jonas",
        "Micas", "Nahum", "Habakuk", "Zefanias", "Haggai", "Zacarias", "Malakias"
    ]
    
    new_testament_books = [
        "Mateo", "Marcos", "Lucas", "Juan", "Binuhatan",
        "Roma", "1 Corinto", "2 Corinto", "Galacia", "Efeso", "Filipos", "Colosas",
        "1 Tesalonica", "2 Tesalonica", "1 Timoteo", "2 Timoteo", "Tito", "Filemon",
        "Hebreo", "Santiago", "1 Pedro", "2 Pedro", "1 Juan", "2 Juan", "3 Juan", "Judas", "Pahayag"
    ]
    
    books = old_testament_books + new_testament_books
    
    pattern = r"\d+\s+Ang Pulong Sang Dios \(Hiligaynon Contemporary Bible\) © 1996, 2006, 2011 by Biblica, Inc\.®\.\s+"
    #pattern = r"\d+\n+Ang Pulong Sang Dios\n\(Hiligaynon Contemporary Bible\)\n© 1996, 2006, 2011 by Biblica, Inc\.®.\s+"
    text = re.sub(pattern, "", text)
    
    pattern = r"\s+Hiligaynon - All Bible \(Ang Pulong Sang Dios\)\s+"
    text = re.sub(pattern, " ", text)
    
    pattern = r"\((.*?)\)|\{(.*?)\}"
    text = re.sub(pattern, "", text)
    
    pattern = r'\s+([.,;:!?])'
    text = re.sub(pattern, "", text)
    
    pattern = r'\s+([-])'
    text = re.sub(pattern, "-", text)
    
    pattern = r'([-])\s+'
    text = re.sub(pattern, "-", text)
    
    books_pattern = "|".join(books)
    
    pattern = r"({})\s+(\d+)\s(.*?)(?=\d+\s*)".format(books_pattern)
    text = re.sub(pattern, r"\1 \2 ", text)

    pattern = r"(^|\s)({})\s+(\d+)".format(books_pattern)
    text = re.sub(pattern, r"\1\n\2 \3\n", text)
    
    pattern = r"^\s+"
    text = re.sub (pattern, "", text, flags=re.MULTILINE)
    
    pattern = r"\s\n(Juan\s+\d+)[ \t]*\n([A-Za-z])"
    text = re.sub(pattern, r" \1\2", text, flags=re.MULTILINE)
    
    pattern = r"((\d+-)*\d+)(?=[A-Za-z])"
    text = re.sub(pattern, r"\n\1 ", text)
    
    pattern = r"^\d,(.*?)(?=\n)"
    text = re.sub(pattern, "", text, flags=re.MULTILINE)
    
    pattern = r"\n\s*\n"
    text = re.sub(pattern, "\n", text)
    #verify(text)
    return text

def verify(text):
  pattern = r"(Nahum|Genesis|Habakuk|Exodo|Zepania|Levitico|Hageo|Ding Bilang|Zacarias|Deuteronomio|Malakias|Josue|Ukum|Mateo|Ruth|Marcos|1 Samuel|Lucas|2 Samuel|Juan|1 Ari|Ding Dapat|2 Ari|Roma|1 Cronica|1 Corinto|2 Cronica|2 Corinto|Ezra|Galacia|Nehemias|Efeso|Ester|Filipos|Job|Colosas|Ding Dalit|1 Tesalonica|Ding Kasebian|2 Tesalonica|Ecclesiastes|1 Timoteo|Ing Malagung Diling Kanta|2 Timoteo|Isaias|Tito|Jeremias|Filemon|Ding Tagulele|Hebreo|Ezekiel|Santiago|Daniel|1 Pedro|Hosea|2 Pedro|Joel|1 Juan|Amos|2 Juan|Obadias|3 Juan|Jonas|Judas|Mikeas|Kapahayagan)\s(\d+)\n"
  chapter_counts = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66, 52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4]

  chapters = re.findall(pattern, text)

  book_chapters = defaultdict(list)
  for book, chap in chapters:
    book_chapters[book].append(int(chap))

  for ((book, chaps), count) in zip(book_chapters.items(), chapter_counts):
    if count == len(chaps):
      print(f"{book} chapters ({len(chaps)}) in order ✓")
    else:
      print(f"{book} chapters ({len(chaps)} SHOULD BE {count}) NOT in order x")