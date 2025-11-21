## Prerequisites
```bash
python scripts/extract_training_set.py
```

## Start Container
```bash
docker compose up -d
```
### Status
```bash
docker ps -a
```

## Enter Container
```bash
docker exec -it eole_nlp bash
```
```bash
cd /workspace
```

## Build Vocabulary
```bash
eole build_vocab -config configs/<config_file>.yml -n_sample -1
```

## Train 
```bash
eole train -config configs/<config_file>.yml
```

## Predict/Translate
```bash
eole predict \
    -model_path data/training/TGL_HIL/model/step_5500 \
    -src data/training/TGL_HIL/test.tgl \
    -output data/training/TGL_HIL/pred.hil \
    --gpu_ranks 0
```

## Stop Container
```bash
docker compose down
```

## Bleu score
```bash
sacrebleu test.<code> -i pred.<code> -m bleu --tokenize none -w 4
```