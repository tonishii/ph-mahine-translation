#!/usr/bin/env bash
cd /home/ubuntu/working/mert-work
/home/ubuntu/mosesdecoder/bin/extractor --sctype BLEU --scconfig case:true  --scfile run5.scores.dat --ffile run5.features.dat -r /home/ubuntu/training/TGL_HIL/valid.hil -n run5.best100.out.gz
