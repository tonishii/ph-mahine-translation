import sys, os, re, pandas as pd

pairs = [
  ("PAG", "TAO"),
  ("HIL", "WAR"),
  ("CBK", "SPA"),
  ("TGL", "PAM"),
  ("BCL", "KAK"),
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

  lang1_df = pd.read_excel(os.path.join(dir_path, lang1) + ".xlsx", dtype=str)
  lang2_df = pd.read_excel(os.path.join(dir_path, lang2) + ".xlsx", dtype=str)

  books1, books2 = lang1_df["Book"].unique(), lang2_df["Book"].unique()
  book_map = {book1: book2 for book1, book2 in zip(books1, books2)}
  book_map_lang1_to_eng = {local: eng for local, eng in zip(books1, new_testament_books)}
  book_map_lang2_to_eng = {local: eng for local, eng in zip(books2, new_testament_books)}

  lang1_iter, lang2_iter = lang1_df.itertuples(), lang2_df.itertuples()
  parallel_rows = []

  try:
    while True:
      next_lang1, next_lang2 = next(lang1_iter), next(lang2_iter)

      # print(next_lang1, next_lang2)
      if book_map.get(next_lang1.Book) == next_lang2.Book and next_lang1.Chapter == next_lang2.Chapter and next_lang1._3 == next_lang2._3:
        parallel_rows.append([
          book_map_lang1_to_eng.get(next_lang1.Book),
          next_lang1.Chapter,
          next_lang1._3,
          next_lang1.Text,
          next_lang2.Text
        ])

      elif next_lang1._3 != next_lang2._3:
        match = re.match(r"(\d+)-(\d+)", str(next_lang1._3))
        if match:
          low, high = match.groups()
          text = []
          next_tuple = None
          for _ in range(int(high) - int(low) + 1):
            next_tuple = next(lang1_iter)
            text.append(next_tuple.Text)

          if not next_tuple:
            return []

          parallel_rows.append([
            book_map_lang1_to_eng.get(next_lang1.Book),
            next_lang1.Chapter,
            low+"-"+high,
            " ".join(text),
            next_lang2.Text
          ])

        else:
          match = re.match(r"(\d+)-(\d+)", str(next_lang2._3))
          if match:
            low, high = match.groups()
            text = []
            next_tuple = None
            for _ in range(int(high) - int(low) + 1):
              next_tuple = next(lang1_iter)
              text.append(next_tuple.Text)

            if not next_tuple:
              return []

            parallel_rows.append([
              book_map_lang1_to_eng.get(next_lang1.Book),
              next_lang1.Chapter,
              low+"-"+high,
              " ".join(text),
              next_lang2.Text
            ])
          else:
            lang1_verse_no, lang2_verse_no = int(next_lang1._3), int(next_lang2._3) # type: ignore
            while lang1_verse_no > lang2_verse_no:
              parallel_rows.append([
                book_map_lang1_to_eng.get(next_lang1.Book),
                next_lang1.Chapter,
                lang2_verse_no,
                f"<no verse{lang2_verse_no}>",
                next_lang2.Text
              ])

              next_lang1, next_lang2 = next(lang1_iter), next(lang2_iter)
              print(next_lang1, next_lang2)
              lang1_verse_no, lang2_verse_no = int(next_lang1._3), int(next_lang2._3) # type: ignore

            while lang2_verse_no > lang1_verse_no:
              parallel_rows.append([
                book_map_lang1_to_eng.get(next_lang1.Book),
                next_lang1.Chapter,
                f"<no verse{lang1_verse_no}>",
                lang1_verse_no,
                next_lang1.Text
              ])

              next_lang1, next_lang2 = next(lang1_iter), next(lang2_iter)
              print(next_lang1, next_lang2)
              lang1_verse_no, lang2_verse_no = int(next_lang1._3), int(next_lang2._3) # type: ignore

            # print(next_lang1, next_lang2)
  except StopIteration:
    print("Error")

  parallel_df = pd.DataFrame(parallel_rows, columns=[
    "Book", "Chapter", "Verse", codes.get(lang1).capitalize(), codes.get(lang2).capitalize() # type: ignore
  ])

  output_path = os.path.join("data/parallels", f"{lang1}_{lang2}_parallel.xlsx")
  parallel_df.to_excel(output_path, index=False)
  print(f"Parallel corpus saved to: {output_path}")

def main():
  if not sys.argv[1:]:
    for (lang1, lang2) in pairs:
      process_corpora(lang1, lang2)

  else:
    lang1, lang2 = sys.argv[1:3]
    process_corpora(lang1, lang2)

if __name__ == "__main__":
  main()