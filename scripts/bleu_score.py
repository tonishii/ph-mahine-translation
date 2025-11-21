import os
import subprocess
import re

train_dir = "data/training"

for dataset_folder in os.listdir(train_dir):
    dataset_path = os.path.join(train_dir, dataset_folder)
    
    pred_folder = os.path.join(dataset_path, "predictions")
    if not os.path.isdir(pred_folder):
        continue  
    
    tgt_lang = dataset_folder.split("_")[1].lower()
    
    test_file = os.path.join(dataset_path, f"test.{tgt_lang}")
    if not os.path.exists(test_file):
        continue

    bleu_folder = os.path.join(dataset_path, "bleu_scores")
    os.makedirs(bleu_folder, exist_ok=True)

    pred_files = [f for f in os.listdir(pred_folder) if f.startswith("pred_") and f.endswith(f".{tgt_lang}")]
    pred_files.sort(key=lambda x: int(re.findall(r"\d+", x)[0]))  
    for pred_file in pred_files:
        step_number = re.findall(r"\d+", pred_file)[0]
        pred_file_path = os.path.join(pred_folder, pred_file)
        bleu_output_file = os.path.join(bleu_folder, f"score_{step_number}.json")

        cmd = f"sacrebleu {test_file} -i {pred_file_path} -m bleu --tokenize none -w 4 > {bleu_output_file}"
        subprocess.run(cmd, shell=True)

