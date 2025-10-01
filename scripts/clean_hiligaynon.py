import re
from collections import defaultdict

def clean_hiligaynon(text):
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
    
    pattern = r"(\d{1,3})(?=[A-Z][a-z])"
    text = re.sub(pattern, r"\n\1 ", text)
    
    pattern = r"^\d,(.*?)(?=\n)"
    text = re.sub(pattern, "", text, flags=re.MULTILINE)
    
    pattern = r"\n\s*\n"
    text = re.sub(pattern, "\n", text)

    return text