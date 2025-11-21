import re, os

dir_path = "data/no_punctuation"
new_path = "data/by_lower_sentence"

for file in os.listdir(dir_path):
    if file.endswith('.txt'):
        file_path = os.path.join(dir_path, file)

        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        text = text.lower()
        os.makedirs(new_path, exist_ok=True)
        file_path = os.path.join(new_path, file)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"data/by_lower_sentence/{file}.txt: {file} ✓")

    