import pandas as pd
import glob
import os
import re
from sklearn.model_selection import train_test_split

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

rev_codes = {v.lower(): k for k, v in codes.items()}

search = os.path.join('data/parallels', '*.csv')
files = glob.glob(search)

for file in files:
    df = pd.read_csv(file)
    df.drop(columns=['Book', 'Chapter', 'Verse'], inplace=True)
    

    columns = df.columns.to_list()
    
    base_name = os.path.splitext(os.path.basename(file))[0]
    base_dir = os.path.join("data", "training", base_name)
    os.makedirs(base_dir, exist_ok=True)
    
    for column in df.columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.lower()
            .apply(lambda x: re.sub(r'[^\w\s\'\-]', '', x))        
            .apply(lambda x: re.sub(r'\s+', ' ', x).strip())   
        )
        
    df = df[~df.apply(lambda row: row.astype(str).str.fullmatch(r'no verse\s*\d*', flags=re.IGNORECASE)).any(axis=1)]
    
    train_val, test = train_test_split(df, test_size=0.05, random_state=42)
    train, val = train_test_split(train_val, test_size=0.15, random_state=42)
    
    for column in df.columns:
        ext = rev_codes[column.lower()].lower()

        train[column].to_csv(os.path.join(base_dir, f"train.{ext}"), index=False, header=False, encoding="utf-8")
        val[column].to_csv(os.path.join(base_dir, f"valid.{ext}"), index=False, header=False, encoding="utf-8")
        test[column].to_csv(os.path.join(base_dir, f"test.{ext}"), index=False, header=False, encoding="utf-8")

        
        
        