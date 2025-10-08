import sys, os, re, pandas as pd

pairs = [
  ("PAG", "TAO"),
  ("HIL", "WAR"),
  ("CBK", "SPA"),
  ("TGL", "PAM"),
  ("BCL", "KAK"),
  ("CEB", "ENG"),
]

codes = {
  "ENG": "english",
  "SPA": "espanol",
  "TAO": "yami",
  "TGL": "tagalog",
  "CEB": "cebuano",
  "ILO": "ilocano",
  "PAM": "kapampangan",
  "HIL": "hiligaynon",
  "WAR": "waray",
  "PAG": "pangasinense",
  "BCL": "bicolano",
  "TSG": "tausug",
  "KAK": "kalanguya",
  "CBK": "chavacano",
  "IFK": "tuwali",
}

old_testament_books = [
  "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
  "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
  "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
  "Ezra", "Nehemiah", "Esther", "Job", "Psalms",
  "Proverbs", "Ecclesiastes", "Song of Songs", "Isaiah",
  "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea",
  "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum",
  "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"
]

new_testament_books = [
  "Matthews", "Mark", "Luke", "John", "The Acts",
  "Romans", "1 Corinthians", "2 Corinthians",
  "Galatians", "Ephesians", "Philippians", "Colossians",
  "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy",
  "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter",
  "1 John", "2 John", "3 John", "Jude", "Revelation"
]

def process_corpora(lang1, lang2):
  dir_path = "data/by_verse/"

  # Read both languages with all string columns
  lang1_df = pd.read_excel(os.path.join(dir_path, lang1) + ".xlsx", dtype=str)
  lang2_df = pd.read_excel(os.path.join(dir_path, lang2) + ".xlsx", dtype=str)


  books1, books2 = list(lang1_df["Book"].unique()), list(lang2_df["Book"].unique())

  lang1_to_eng_book, eng_book = {}, []
  if lang1 in ["TAO", "PAG", "CBK", "TSG"]:
    eng_book = new_testament_books
    lang1_to_eng_book = {local: eng for local, eng in zip(books1, eng_book)} # New Testament only
  else:
    eng_book = old_testament_books + new_testament_books
    lang1_to_eng_book = {local: eng for local, eng in zip(books1, eng_book)}

  if lang2 in ["TAO", "PAG", "CBK", "TSG"]:
    eng_book = new_testament_books
    lang2_to_eng_book = {local: eng for local, eng in zip(books2, eng_book)} # New Testament only
  else:
    eng_book = old_testament_books + new_testament_books
    lang2_to_eng_book = {local: eng for local, eng in zip(books2, eng_book)}

  lang1_df["Book"] = lang1_df["Book"].map(lang1_to_eng_book).fillna(lang1_df["Book"])
  lang2_df["Book"] = lang2_df["Book"].map(lang2_to_eng_book).fillna(lang2_df["Book"])

  merged = pd.merge(
    lang1_df,
    lang2_df,
    on=["Book", "Chapter", "Verse"],
    how="outer",
    suffixes=(f"_{lang1}", f"_{lang2}")
  )

  merged = merged.rename(columns={
    f"Text_{lang1}": codes.get(lang1),
    f"Text_{lang2}": codes.get(lang2),
  })

  for lang in (lang1, lang2):
    col = codes.get(lang)
    merged[codes.get(lang)] = merged.apply(
      lambda r: (
        r.get(col)
        if pd.notna(r.get(col))
        else f"<no verse{r['Verse']}>"
      ),
      axis=1
    )

  merged = merged.sort_values(
    by=["Book", "Chapter", "Verse"],
    key=lambda col: col.map(
      lambda v: eng_book.index(v) # Use book ind to sort
      if col.name == "Book"
      else int(re.match(r"\d+", str(v)) # Finds the first number for verses and chapters to sort
               .group()) if re.match(r"\d+", str(v)) else 9999 # type: ignore
    )
  ).reset_index(drop=True)

  output_path = os.path.join("data/parallels", f"{lang1}_{lang2}.xlsx")
  merged.to_excel(output_path, index=False)
  print(f"{output_path} ✓")

def main():
  if not sys.argv[1:]:
    for (lang1, lang2) in pairs:
      process_corpora(lang1, lang2)

  else:
    lang1, lang2 = sys.argv[1:3]
    process_corpora(lang1, lang2)

if __name__ == "__main__":
  main()