import sys, os, re, pandas as pd

pairs = [
  ("TAO", "HIL"),
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

# Only appends if value is valid
def safe_append(arr, val):
  if pd.notna(val) and str(val).lower() != "nan":
    arr.append(str(val))

def process_corpora(lang1, lang2):
  dir_path = "data/by_verse/"

  # Read both languages with all string columns
  lang1_df = pd.read_excel(os.path.join(dir_path, lang1) + ".xlsx", dtype=str)
  lang2_df = pd.read_excel(os.path.join(dir_path, lang2) + ".xlsx", dtype=str)

  # List of unique books for each lang
  books1, books2 = list(lang1_df["Book"].unique()), list(lang2_df["Book"].unique())

  # Build the lang1 to english book translation map and a list of english books
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

  # Slice the bigger dataframe based on book set size
  if len(books1) > len(books2):
    lang1_df = lang1_df[lang1_df["Book"].isin(books1[-len(books2):])]

  elif len(books1) < len(books2):
    lang2_df = lang2_df[lang2_df["Book"].isin(books2[-len(books1):])]

  # Translate the books to english
  lang1_df["Book"] = lang1_df["Book"].map(lang1_to_eng_book).fillna(lang1_df["Book"])
  lang2_df["Book"] = lang2_df["Book"].map(lang2_to_eng_book).fillna(lang2_df["Book"])

  merged = pd.merge(
    lang1_df,
    lang2_df,
    on=["Book", "Chapter", "Verse"],
    how="outer",
    suffixes=(f"_{lang1}", f"_{lang2}")
  )

  col_lang1_name = codes.get(lang1,"None").capitalize()
  col_lang2_name = codes.get(lang2,"None").capitalize()

  # Rename to specified column
  merged = merged.rename(columns={
    f"Text_{lang1}": col_lang1_name,
    f"Text_{lang2}": col_lang2_name,
  })

  merged = merged.sort_values(
    by=["Book", "Chapter", "Verse"],
    key=lambda col: col.map(
      lambda v: eng_book.index(v) # Use book ind to sort
      if col.name == "Book"
      else int(re.match(r"\d+", str(v)) # Finds the first number for verses and chapters to sort
               .group()) if re.match(r"\d+", str(v)) else 9999 # type: ignore
    )
  ).reset_index(drop=True)

  range_verse_iter = merged[merged["Verse"].str.contains(r"^\d+-\d+$")].iterrows()
  pattern = re.compile(r"(\d+)-(\d+)")
  to_drop = []

  while True:
    try:
      curr_range_idx, curr_range_tuple = next(range_verse_iter)
      curr_range_idx = int(curr_range_idx) # type: ignore
    except:
      break # Exhaust

    range_match = re.match(pattern, curr_range_tuple.Verse)
    # print(curr_range_verse)

    if not range_match: continue # Literally impossible

    low, high = range_match.groups()
    low, high, curr_verse_num = int(low), int(high), int(low)
    text_lang1, text_lang2, drop_indices = [], [], []

    while curr_verse_num < high + 1:
      range_verse = merged.loc[
        (merged["Book"] == curr_range_tuple.Book) &
        (merged["Chapter"] == curr_range_tuple.Chapter) &
        (merged["Verse"] == str(curr_verse_num))
      ]

      if not range_verse.empty: # Safe to append to resulting text
        safe_append(text_lang1, range_verse[col_lang1_name].iloc[0])
        safe_append(text_lang2, range_verse[col_lang2_name].iloc[0])
        drop_indices.extend(range_verse.index.to_list())

        curr_verse_num += 1
        continue

      # This case is for overlapping ranges
      overlap = merged.loc[
        (merged["Book"] == curr_range_tuple.Book) &
        (merged["Chapter"] == curr_range_tuple.Chapter) &
        (merged["Verse"].astype(str).str.match(rf"^{curr_verse_num}+-\d+$", na=False))
      ]                                            # ^ Ofc start with the verse number were searching for

      if overlap.empty:
        curr_verse_num += 1
        continue

      if pd.notna(overlap.iloc[0][col_lang1_name]) and pd.notna(overlap.iloc[0][col_lang2_name]):
        curr_verse_num += 1
        continue

      # Leaves only overlapping ranges
      overlap_range = re.match(pattern, overlap.iloc[0].Verse)
      _, new_high = overlap_range.groups() # type: ignore
      high = max(high, int(new_high)) # Adjust the range
      # print(overlap_range)

      safe_append(text_lang1, overlap[col_lang1_name].iloc[0])
      safe_append(text_lang2, overlap[col_lang2_name].iloc[0])
      # print(text_lang1, text_lang2)

      drop_indices.extend(overlap.index.to_list())
      curr_verse_num += 1 # Better to search even with a new high

    if text_lang1 or text_lang2:
      safe_append(text_lang1, curr_range_tuple[codes.get(lang1, "None").capitalize()])
      safe_append(text_lang2, curr_range_tuple[codes.get(lang2, "None").capitalize()])

      merged.at[curr_range_idx, codes.get(lang1, "None").capitalize()] = " ".join(text_lang1)
      merged.at[curr_range_idx, codes.get(lang2, "None").capitalize()] = " ".join(text_lang2)

      merged.at[curr_range_idx, "Verse"] = str(low)+"-"+str(high)

      # print(drop_indices)
    to_drop.extend(drop_indices)

  # Drop the marked rows
  merged.drop(index=to_drop, inplace=True)
  merged.reset_index(drop=True, inplace=True)

  # Fills the empty rows
  for lang in (lang1, lang2):
    col = codes.get(lang,"None").capitalize()
    merged[codes.get(lang,"None").capitalize()] = merged.apply(
      lambda r: (
        r.get(col)
        if pd.notna(r.get(col))
        else f"<no verse{r['Verse']}>"
      ),
      axis=1
    )

  merged.to_excel("data/parallels/" + f"{lang1}_{lang2}.xlsx", index=False)
  merged.to_csv("data/parallels/" + f"{lang1}_{lang2}.csv", index=False)
  print(f"data/parallels/{lang1}_{lang2}.xlsx ✓")

def main():
  if not sys.argv[1:]:
    for (lang1, lang2) in pairs:
      process_corpora(lang1, lang2)

  else:
    lang1, lang2 = sys.argv[1:3]
    process_corpora(lang1, lang2)

if __name__ == "__main__":
  main()