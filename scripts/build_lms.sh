mkdir -p ../counts/token

for f in ../data/by_lower_sentence/*.txt; do
    lang=$(basename "$f" .txt)
    echo "Building 3-gram model for $lang..."

    ngram-count -text "$f" \
                -order 3 \
                -write "../counts/token/${lang}_3grams.txt" \
                -no-sos -no-eos
done

echo "All 3-gram models built successfully!"
