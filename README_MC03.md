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
    -output data/training/TGL_HIL/pred.hgl \
    --gpu_ranks 0
```

## Stop Container
```bash
docker compose down
```

## Moses Commands (TENTATIVE)
``` bash
# setup ubuntu server 24.04 LTS instance type c7i-flex.large on aws

ssh -i "key.pem" ubuntu@<your-public-dns>
sudo apt-get update
sudo apt-get upgrade -y
sudo add-apt-repository universe
sudo apt-get update
sudo apt-get g++ git subversion automake libtool zlib1g-dev libicu-dev libboost-all-dev libbz2-dev liblzma-dev python3-dev graphviz imagemagick make cmake libgoogle-perftools-dev autoconf doxygen tmux
git clone https://github.com/moses-smt/mosesdecoder.git
cd mosesdecoder
tmux new -s build
./bjam -j4

mkdir ~/lm
cd ~/lm
~/mosesdecoder/bin/lmplz -o 3 < ~/training/CBK_SPA/train.spa > model.arpa.spa

~/mosesdecoder/bin/build_binary \
  model.arpa.spa \
  model.blm.spa

mkdir ~/working
cd ~/working
~/mosesdecoder/scripts/training/train-model.perl \
  -root-dir train \
  -corpus ~/training/CBK_SPA/train \
  -f cbk -e spa \
  -alignment grow-diag-final-and \
  -reordering msd-bidirectional-fe \
  -lm 0:3:$HOME/lm/model.blm.spa:8 \
  -external-bin-dir ~/mosesdecoder/tools

~/mosesdecoder/scripts/training/mert-moses.pl \
  ~/training/CBK_SPA/valid.cbk ~/training/CBK_SPA/valid.spa \
  ~/mosesdecoder/bin/moses train/model/moses.ini --mertdir ~/mosesdecoder/bin/ \
  --decoder-flags="-threads 2"

mkdir binarised-model
~/mosesdecoder/bin/processPhraseTableMin \
  -in train/model/phrase-table.gz -nscores 4 \
  -out binarised-model/phrase-table
~/mosesdecoder/bin/processLexicalTableMin \
  -in train/model/reordering-table.wbe-msd-bidirectional-fe.gz \
  -out binarised-model/reordering-table

~/mosesdecoder/scripts/training/filter-model-given-input.pl             \
  filtered-test-model mert-work/moses.ini ~/training/CBK_SPA/test.cbk  \
  -Binarizer ~/mosesdecoder/bin/processPhraseTableMin

~/mosesdecoder/bin/moses \
  -f filtered-test-model/moses.ini \
  < ~/training/CBK_SPA/test.cbk \
  > test.translated.spa

sacrebleu  ~/training/CBK_SPA/test.spa -i test.translated.spa -m bleu --tok intl > bleu.json

sacrebleu  ~/training/CBK_SPA/test.spa -i test.translated.spa -m chrf --tok intl > chrf.json
```