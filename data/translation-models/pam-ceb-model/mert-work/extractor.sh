#!/usr/bin/env bash
cd /home/ubuntu/working2/mert-work
/home/ubuntu/mosesdecoder/bin/extractor --sctype BLEU --scconfig case:true  --scfile run11.scores.dat --ffile run11.features.dat -r /home/ubuntu/training/PAM_CEB/valid.ceb -n run11.best100.out.gz
