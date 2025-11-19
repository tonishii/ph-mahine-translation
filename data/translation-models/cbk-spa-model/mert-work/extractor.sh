#!/usr/bin/env bash
cd /home/ubuntu/working/mert-work
/home/ubuntu/mosesdecoder/bin/extractor --sctype BLEU --scconfig case:true  --scfile run6.scores.dat --ffile run6.features.dat -r /home/ubuntu/training/CBK_SPA/valid.spa -n run6.best100.out.gz
