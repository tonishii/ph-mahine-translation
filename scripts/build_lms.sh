#!/bin/bash
mkdir -p counts

for f in data/char_text/*.txt; do
    lang=$(basename "$f" .txt)
    echo "Building model for $lang..."
    ngram-count -text "$f" \
                -order 4 \
                -write "counts/${lang}_4grams.txt" \
                -no-sos -no-eos
done

echo "All models built successfully!"
