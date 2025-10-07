import sys, os, pandas as pd

pairs = [
  ("PAG", "TAO"),
  ("HIL", "WAR"),
  ("CBK", "SPA"),
  ("TGL", "PAM"),
  ("BCL", "KAK"),
  ("CEB", "ENG"),
]

def process_corpora(lang1, lang2):
  dir_path = "data/by_verse/"

  lang1 = os.path.join(dir_path, lang1)
  lang2 = os.path.join(dir_path, lang2)

  lang1_df = pd.read_excel(lang1 + ".xlsx")
  lang2_df = pd.read_excel(lang2 + ".xlsx")

  print(lang1_df.head())
  print(lang2_df.head())

def main():
  if not sys.argv[1:]:
    for (lang1, lang2) in pairs:
      process_corpora(lang1, lang2)

  else:
    lang1, lang2 = sys.argv[1:3]
    process_corpora(lang1, lang2)

if __name__ == "__main__":
  main()