#!/usr/bin/env bash
cd /home/ubuntu/working/mert-work
/home/ubuntu/mosesdecoder/bin/extractor --sctype BLEU --scconfig case:true  --scfile run11.scores.dat --ffile run11.features.dat -r /home/ubuntu/training/TAO_TGL/valid.tgl -n run11.best100.out.gz
