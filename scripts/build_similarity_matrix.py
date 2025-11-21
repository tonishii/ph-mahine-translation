import re
from pathlib import Path
import pandas as pd

file_dir_lex = Path('counts') / 'lexical'
file_dir_tok = Path('counts') / 'token'
output_dir = Path('sim_matrix')
output_dir.mkdir(parents=True, exist_ok=True)

trigrams_l = {} # dictionary
bigrams_l = {}
unigrams_l = {}

trigrams_w = {} # dictionary
bigrams_w = {}
unigrams_w = {}

def dice(a, b):
    return 2 * len(a & b) / (len(a) + len(b))

def ngram_extract_lex(file_path, n):
    text = file_path.read_text(encoding='utf-8')
    text = re.sub(r'\t\d+\r?\n?', '\n', text)
    ngram = set(re.findall(rf"^[A-Za-z0-9'-]{{{n}}}$", text, flags=re.MULTILINE))
    return ngram

def ngram_extract_word(file_path, n, min_count=2):
    text = file_path.read_text(encoding='utf-8')
    text = re.sub(r'\t\d+\s*$', '', text)
    ngram = set()
    
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        count = int(parts[-1]) if parts[-1].isdigit() else 1
        words = parts[:-1] if parts[-1].isdigit() else parts

        if count < min_count:
            continue
        
        if len(words) == n:
            ngram.add(tuple(words))

    return ngram
    
for file_path in file_dir_lex.glob('*'):
    unigrams_l[file_path.stem] = ngram_extract_lex(file_path, 1)
    bigrams_l[file_path.stem] = ngram_extract_lex(file_path, 2)
    trigrams_l[file_path.stem] = ngram_extract_lex(file_path, 3)

for file_path in file_dir_tok.glob('*'):
    unigrams_w[file_path.stem] = ngram_extract_word(file_path, 1)
    bigrams_w[file_path.stem] = ngram_extract_word(file_path, 2)
    trigrams_w[file_path.stem] = ngram_extract_word(file_path, 3)

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

ul_matrix = sim_matrix(unigrams_l, 'unigram_lex')
bl_matrix = sim_matrix(bigrams_l, 'bigram_lex')
tl_matrix = sim_matrix(trigrams_l, 'trigram_lex')

uw_matrix = sim_matrix(unigrams_w, 'unigram_word')
bw_matrix = sim_matrix(bigrams_w, 'bigram_word')
tlwmatrix = sim_matrix(trigrams_w, 'trigram_word')