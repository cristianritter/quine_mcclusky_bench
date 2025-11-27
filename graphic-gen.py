import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Data from Image
data = {
    'N Vars (n)': [4, 5, 6, 7, 8, 9, 10, 11, 12],
    'Minterms': [3, 7, 15, 31, 63, 127, 255, 511, 1023],
    'Don\'t Cares': [0, 1, 3, 6, 12, 25, 51, 102, 204],
    'Average Time (ms)': [0.1178, 0.5150, 1.9954, 7.6465, 25.8294, 160.2858, 662.9968, 3678.6571, 24206.6752]
}

df = pd.DataFrame(data)

# 2. Generating the Scalability Plot (Log Scale)
plt.figure(figsize=(9, 5))
# Use 'Average Time (ms)' column for plotting
plt.plot(df['N Vars (n)'], df['Average Time (ms)'], marker='o', linestyle='-', color='blue')

# The Y-axis must be logarithmic to clearly visualize exponential growth
plt.yscale('log') 

plt.title('Quine-McCluskey Algorithm Performance: Runtime vs. Variables (n)', fontsize=14)
plt.xlabel('Number of Variables (n)', fontsize=12)
plt.ylabel('Average Time (ms) - Logarithmic Scale', fontsize=12)
plt.grid(True, which="both", ls="--", linewidth=0.5)

# Adding time labels (optional)
for i, row in df.iterrows():
    # Position the label above each point
    plt.text(row['N Vars (n)'], row['Average Time (ms)'], f"{row['Average Time (ms)']:.1f}", 
             ha='left', va='bottom', fontsize=9)

# Save the plot as PDF (best quality for IEEE template)
plt.savefig('runtime_scalability_qmc.pdf', bbox_inches='tight')
print("Plot 'runtime_scalability_qmc.pdf' generated successfully!")

# 3. Displaying the Table (Optional)
print("\n--- Results Table ---")
# Adjust column names for printing the table
df.columns = ['N Vars (n)', 'Minterms', 'Don\'t Cares', 'Avg Time (ms)']
print(df.to_string(index=False))