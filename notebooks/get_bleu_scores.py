import os
import pandas as pd
import json
import re

base_dir = os.path.join(os.path.dirname(__file__), '../data/training')
base_dir = os.path.abspath(base_dir)

def read_bleu_score():
    dfs = []

    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        
        if not os.path.isdir(folder_path):
            continue

        scores = []
        steps = []

        bleu_folder = os.path.join(folder_path, "bleu_scores")
        if not os.path.isdir(bleu_folder):
            continue

        for file in os.listdir(bleu_folder):
            if file.endswith(".json"):
                match = re.search(r'score_(\d+)\.json', file)
                if match:
                    step_num = int(match.group(1))
                    steps.append(step_num)

                    file_path = os.path.join(bleu_folder, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        score = data.get("score")
                        scores.append(score)

        if steps:  
            sorted_pairs = sorted(zip(steps, scores))
            steps_sorted, scores_sorted = zip(*sorted_pairs)

            df = pd.DataFrame({
                "step": steps_sorted,
                "score": scores_sorted
            })
            df.name = folder  
            dfs.append(df)

    return dfs

