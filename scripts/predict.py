import os
import subprocess
import re

train_dir = "data/training"


for dataset_folder in os.listdir(train_dir):
    dataset_path = os.path.join(train_dir, dataset_folder)
    
    model_path = os.path.join(dataset_path, "model")
    
    src_lang = dataset_folder.split("_")[0].lower()
    tgt_lang = dataset_folder.split("_")[1].lower()
    src_file = os.path.join(dataset_path, f"test.{src_lang}")
    if not os.path.exists(model_path) or not os.path.exists(src_file):
        continue
    print(src_file)
    
    pred_folder = os.path.join(dataset_path, "predictions")
    os.makedirs(pred_folder, exist_ok=True)
    
    step_dirs = [d for d in os.listdir(model_path) if re.match(r"step_\d+", d)]
    print(step_dirs)
    
    for step_dir in step_dirs:
        step_number = re.findall(r"\d+", step_dir)[0]
        
        full_model_path = os.path.join(model_path, step_dir)
        output_file = os.path.join(pred_folder, f"pred_{step_number}.{tgt_lang}")
        
        cmd = [
            "eole", "predict",
            "-model_path", full_model_path,
            "-src", src_file,
            "-output", output_file,
            "--gpu_ranks", "0"
        ]
        
        print(f"Running prediction for dataset {dataset_folder}, step {step_number}, target lang {tgt_lang}")
        subprocess.run(cmd)
        print(f"Prediction saved to {output_file}\n") 