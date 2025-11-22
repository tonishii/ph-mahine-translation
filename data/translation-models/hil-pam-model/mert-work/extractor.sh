#!/usr/bin/env bash
cd /home/ubuntu/working2/mert-work
/home/ubuntu/mosesdecoder/bin/extractor --sctype BLEU --scconfig case:true  --scfile run13.scores.dat --ffile run13.features.dat -r /home/ubuntu/training/HIL_PAM/valid.pam -n run13.best100.out.gz
