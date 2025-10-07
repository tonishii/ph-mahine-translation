import re
from collections import defaultdict

books = [
    "Genesis", "Exodo", "Levitico", "Mga Bilang", "Deuteronomio", "Josue", "Hukom", "Ruth",
    "1 Samuel", "2 Samuel", "1 Mga Hade", "2 Mga Hade", "1 mga Cronica", "2 Mga Cronica", "Esdras",
    "Nehemias", "Esther", "Job", "Salmo", "Mga Talinhaga", "Ecclesiastes o an Parahulit",
    "An Awit Nin Mga Awit", "Isaias", "Jeremias", "Mga Panambitan", "Ezekiel", "Daniel", "Oseas",
    "Joel", "Amos", "Obadias", "Jonas", "Mikas", "Nahum", "Habakkuk", "Sofonias", "Hageo",
    "Zacarias", "Malakias", "Mateo", "Markos", "Lukas", "Juan", "Gibo", "Roma", "1 Corinto",
    "2 Corinto", "Galacia", "Efeso", "Filipos", "Colosas", "1 Taga Tesalonica", "2 Taga Tesalonica",
    "Taga Tesalonica", "1 Timoteo", "2 Timoteo", "Tito", "Filemon", "Hebreyo", "Santiago",
    "1 Pedro", "2 Pedro", "1 Juan", "2 Juan", "3 Juan", "Judas", "Kapahayagan"
]

def clean_bicolano(text):
    
    # Remove footer 
    pattern = r"\b\d+\s+Marahay na Bareta Biblia Central Bikol New Testament © 1981, Bible © 1992, Philippine Bible Society\.\s*"
    text = re.sub(pattern, "", text)

    # Remove brackets but keep contents
    pattern = r"\[(.*?)\]"
    text = re.sub(pattern, r"\1", text)

    # Separate by book + chapter
    book_pattern = "|".join(books)
    pattern = rf"(?:\b({book_pattern}))\s+(?:\1\s+)?(\d+)\b(?![\"“]?[A-Za-z])"
    text = re.sub(pattern, r"\n\n\1 \2", text)

    # Add space after verse ranges (e.g. 1-2text → 1-2 text)
    pattern = r"\b(\d+)-(\d+)([\"“]?[A-Za-z]+)\b"
    text = re.sub(pattern, r"\n\1-\2 \3", text)

    # Add space after single verse numbers (e.g. 3text → 3 text)
    pattern = r"\b(\d+)([\"“]?[A-Za-z]+)\b"
    text = re.sub(pattern, r"\n\1 \2", text)

    # Normalize spacing for . & ,
    pattern = r"\s+([.,])"
    text = re.sub(pattern, r"\1", text)

    # Remove everything after book + chapter 
    pattern = rf"({book_pattern})\s+(\d+).*"
    text = re.sub(pattern, r"\1 \2", text)

    # Remove parentheses but keep contents
    pattern = r"[()]+"
    text = re.sub(pattern, "", text)

    # Remove the last section
    pattern = r"Esclarecimento(.|\n)*"
    text = re.sub(pattern, "", text)
    
    # Remove double new lines
    pattern = r'\n\n+'
    text = re.sub(pattern, "\n", text)
    
    # Remove the very first newline
    text = re.sub(r'^\s*\n+', '', text)
    
    return text
