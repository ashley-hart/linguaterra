#!/bin/bash

# Ensure correct usage, must have at least 2 args.
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <prompt_file> <output_file>"
    exit 1
fi

PROMPT_FILE=$1
OUTPUT_FILE=$2
EVAL1_FILE="bp1_hamming_results.txt"
EVAL2_FILE="bp2_js_results.txt"

# Check if prompt file exists
if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: Prompt file '$PROMPT_FILE' not found!"
    exit 1
fi

# Clear previous output files
> "$OUTPUT_FILE"
> "$EVAL1_FILE"
> "$EVAL2_FILE"

# Process each prompt in the file
while IFS= read -r PROMPT || [ -n "$PROMPT" ]; do
    echo "Processing prompt: $PROMPT"

    # Run the world generator and capture output
    WORLD_MAP=$(python main.py -t map_file.txt --prompt "$PROMPT")

    # Run evaluation functions
    EVAL1=$(python -c "import evaluation; print(evaluation.method1('''$WORLD_MAP'''))")
    EVAL2=$(python -c "import evaluation; print(evaluation.method2('''$WORLD_MAP'''))")

    # Append results to the main output file
    {
        echo "Prompt: $PROMPT"
        echo "Generated World Map:"
        echo "$WORLD_MAP"
        echo "Evaluation Method 1: $EVAL1"
        echo "Evaluation Method 2: $EVAL2"
        echo "----------------------------------"
    } >> "$OUTPUT_FILE"

    # Append numerical results to separate files
    echo "$EVAL1" >> "$EVAL1_FILE"
    echo "$EVAL2" >> "$EVAL2_FILE"

    echo "Completed processing for: $PROMPT"
done < "$PROMPT_FILE"

echo "Batch evaluation complete. Results saved to:"
echo " - $OUTPUT_FILE (full details)"
echo " - $EVAL1_FILE (numerical results for method 1)"
echo " - $EVAL2_FILE (numerical results for method 2)"
