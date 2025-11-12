import re
from pathlib import Path
import pandas as pd

file_dir = Path('counts') / 'lexical'
output_dir = Path('similarity')
output_dir.mkdir(parents=True, exist_ok=True)

trigrams = {} # dictionary

def dice(a, b):
    return 2 * len(a & b) / (len(a) + len(b))

def trigram_extract(file_path):
    text = file_path.read_text(encoding='utf-8')
    text = re.sub(r'\t\d+\r?\n?', '\n', text)
    trigrams = set(re.findall(r"^[A-Za-z0-9'-]{3}$", text, flags=re.MULTILINE))
    return trigrams

for file_path in file_dir.glob('*'):
    trigrams[file_path.stem] = trigram_extract(file_path)

names = list(trigrams.keys())
matrix = pd.DataFrame(index=names, columns=names, dtype=float)

for a in names:
    for b in names:
        matrix.at[a, b] = dice(trigrams[a], trigrams[b])

matrix.to_excel(output_dir / 'matrix.xlsx')

print(matrix)