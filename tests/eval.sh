#!/bin/bash


# Allow optional prompt file input from command line
prompt_file="${1}"

# Display which file is being used
echo "Using prompt file: $prompt_file"

# Ensure the prompt file exists
if [ ! -f "$prompt_file" ]; then
    echo "Error: $prompt_file file not found!"
    exit 1
fi

# Display contents (for verification/debugging)
ls -l "$prompt_file"
# cat "$prompt_file"

# Create the results directory if it doesn't exist
mkdir -p results

# Find the next available eval directory number
n=1
while [ -d "results/eval_$n" ]; do
    ((n++))
done

# Create the new eval directory
eval_dir="eval_$n"
mkdir "results/$eval_dir"

echo "Created new evaluation directory: results/$eval_dir"

# Create a results file in the new eval directory
touch results.txt
results_file="$eval_dir/results.txt"
echo "Starting evaluation..." > "$results_file"

# Create a master results file
results_file="results.txt"
echo "Starting evaluation..." > "$results_file"

# Track the iterations for the sake of labeling files
prompt_number=1

# Loop through each prompt in prompts.txt
while IFS= read -r prompt
do
    echo "Processing prompt: $prompt"
    
    # Generate two maps with the same prompt
    map_file1="map1_prompt_${prompt_number}.txt"
    map_file2="map2_prompt_${prompt_number}.txt"
    
    # Run the world generator twice with the prompt and save to two different map files
    python3 ../main.py --prompt "$prompt" --text "$map_file1" --quiet
    python3 ../main.py --prompt "$prompt" --text "$map_file2" --quiet
    
    # Print the prompt and the contents of the two map files into the results file
    echo "\nITERATION $prompt_number" >> "$results_file"
    echo "Prompt: $prompt" >> "$results_file"
    echo "Map 1 (saved to $map_file1):" >> "$results_file"
    cat "$map_file1" >> "$results_file"
    echo -e "\nMap 2 (saved to $map_file2):" >> "$results_file"
    cat "$map_file2" >> "$results_file"
    
    # Run the evaluation script with both map files and save the results
    evaluation_results=$(python3 test_methods.py --all "$map_file1" "$map_file2")
    echo -e "\nEvaluation results:" >> "$results_file"
    echo "$evaluation_results" >> "$results_file"
    
    # Separate iterations with a line in the results file
    echo -e "\n" >> "$results_file"

    # Increment the prompt number for the next iteration
    ((prompt_number++))
    
    echo "Processing for prompt \"$prompt\" completed."
done < prompts.txt

echo "All prompts processed. Results saved to $results_file."
