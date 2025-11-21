import re
from pathlib import Path
import pandas as pd

file_dir = Path('counts') / 'lexical'
output_dir = Path('sim_matrix')
output_dir.mkdir(parents=True, exist_ok=True)

trigrams = {} # dictionary
bigrams = {}
unigrams = {}

def dice(a, b):
    return 2 * len(a & b) / (len(a) + len(b))

def ngram_extract(file_path, n):
    text = file_path.read_text(encoding='utf-8')
    text = re.sub(r'\t\d+\r?\n?', '\n', text)
    ngram = set(re.findall(rf"^[A-Za-z0-9'-]{{{n}}}$", text, flags=re.MULTILINE))
    return ngram

for file_path in file_dir.glob('*'):
    unigrams[file_path.stem] = ngram_extract(file_path, 1)
    bigrams[file_path.stem] = ngram_extract(file_path, 2)
    trigrams[file_path.stem] = ngram_extract(file_path, 3)

def sim_matrix (ngrams, name):
    names = list(ngrams.keys())
    matrix = pd.DataFrame(index=names, columns=names, dtype=float)

    for a in names:
        for b in names:
            matrix.at[a, b] = dice(ngrams[a], ngrams[b])
    
    matrix.index.name = "XX"
    
    matrix.to_excel(output_dir / f'{name}_matrix.xlsx')
    matrix.to_csv(output_dir / f'{name}_matrix.csv')
    return matrix

u_matrix = sim_matrix(unigrams, 'unigram')
b_matrix = sim_matrix(bigrams, 'bigram')
t_matrix = sim_matrix(trigrams, 'trigram')