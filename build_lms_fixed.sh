#!/bin/bash
mkdir -p models

for f in data/no_punctuation/*.txt; do
    lang=$(basename "$f" .txt)
    echo "Building model for $lang..."
    ngram-count -text "$f" \
                -order 3 \
                -lm "models/${lang}.lm" \
                -unk
done

echo "All models built successfully!"
