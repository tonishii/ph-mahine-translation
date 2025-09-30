# NLP1000-PROJECT

```
NLP1000-PROJECT/
├── data/
│   ├── processed/    <- Preprocessed material
│   ├── raw/          <- Source material
├── scripts/          <- Preprocessing documentation
├── notebooks/        <- For future experimenting
├── dependencies.txt  <- For tracking dependencies
```

## Dependencies
To run some of the scripts you may need to install the dependencies. Run the ff. commands:

```
pip install -r dependencies.txt
```

# Bicolano Regex Replacements

| **Pattern** | **Replace With** |
|-------------|------------------|
| `\b\d+\s+Marahay na Bareta Biblia Central Bikol New Testament © 1981, Bible © 1992, Philippine Bible Society\.\s*` | `` |
| `(Genesis|Exodo|Levitico|Mga Bilang|Deuteronomio|Josue|Hukom|Ruth|1 Samuel|2 Samuel|1 Mga Hade|2 Mga Hade|1 mga Cronica|2 Mga Cronica|Esdras|Nehemias|Esther|Job|Salmo|Mga Talinhaga|Ecclesiastes o an Parahulit|An Awit Nin Mga Awit|Isaias|Jeremias|Mga Panambitan|Ezekiel|Daniel|Oseas|Joel|Amos|Obadias|Jonas|Mikas|Nahum|Habakkuk|Sofonias|Hageo|Zacarias|Malakias|Mateo|Markos|Lukas|Juan|Gibo|Roma|1 Corinto|2 Corinto|Galacia|Efeso|Filipos|Colosas|1 Taga Tesalonica|2 Taga Tesalonica|1 Timoteo|2 Timoteo|Tito|Filemon|Hebreyo|Santiago|1 Pedro|2 Pedro|1 Juan|2 Juan|3 Juan|Judas|Kapahayagan)(\s+\d+\s*)` | `\n\n\1\2` |
| `\b(\d+)(["“]?[A-Za-z]+)\b` | `\nVerse\1: \2` |
