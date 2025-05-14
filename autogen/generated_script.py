# filename: generate_chart.py
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read data from the CSV file
data = pd.read_csv('data.csv')

# Step 2: Calculate the average of the 'score' column
average_score = data['score'].mean()

# Step 3: Generate a bar chart of the results
plt.figure(figsize=(10, 6))
plt.bar('Average Score', average_score)
plt.title('Average Score')
plt.ylabel('Score')
plt.savefig('results.png')

# Step 4: Save the chart as 'results.png'
plt.show()