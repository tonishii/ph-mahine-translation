# NLP1000-PROJECT

```
NLP1000-PROJECT/
├── data/
│   ├── processed/    <- Preprocessed material
│   ├── raw/          <- Source material
│   ├── by_verse/     <- Set of files segmented by verse
│   ├── by_sentence/  <- Set of files segmented by sentences
│   ├── parallels/    <- Set of files for the parallel corpus
├── scripts/          <- Preprocessing documentation
├── notebooks/        <- For future experimenting
├── requirements.txt  <- For tracking dependencies
```

## Dependencies
To run some of the scripts you may need to install the dependencies. Run the ff. commands:

```
pip install -r requirements.txt
```

## File Executables
| File | Description |
|------|--------------|
| `clean.py` | Text cleaner using regexes outputs to data/processed/{ISO}.txt |
| `extract_chavacano.py` | Web scraper for Chavacano text data. |
| `extract-pdf-to-txt.py` | Converts PDF documents into raw text files outputs to data/raw/{LANG}/*. |
| `parallel_corpus.py` | Builds the parallel corpora (e.g., English–Chavacano (ENG-CBK) pairs). Outputs to outputs to data/parallels/{ISO1}_{ISO2}.xlsx. Also produces a CSV version for better readability. |
| `to_by_sentence.py` | Segments text by sentence outputs to data/by_sentence/{ISO}.txt |
| `to_by_verse.py` | Splits text by verse outputs to data/by_verse/{ISO}.xlsx. |
---