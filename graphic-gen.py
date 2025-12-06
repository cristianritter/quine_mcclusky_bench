import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Data from benchmark (Total, Phase1, Phase2)
data = {
    'N Vars (n)':   [4,   5,   6,    7,     8,      9,       10,        11,         12,          13],
    'Minterms':     [3,   7,   15,   31,    63,    127,      255,       511,       1023,        2047],
    "Don't Cares": [0,   1,    3,    6,    12,     25,       51,       102,        204,         409],
    'Total (ms)': [
        0.5484,
        0.6587,
        1.2268,
        9.6860,
        31.1872,
        151.7604,
        588.3319,
        3736.6930,
        25393.6366,
        182674.3696,
    ],
    'Phase1 (ms)': [
        0.0299,
        0.0792,
        0.1599,
        0.3255,
        0.6982,
        1.1976,
        2.8606,
        8.1850,
        18.1695,
        46.8680,
    ],
    'Phase2 (ms)': [
        0.4748,
        0.5586,
        1.0187,
        9.2128,
        30.3482,
        150.3037,
        584.9426,
        3725.4182,
        25373.1878,
        182623.1151,
    ],
}

df = pd.DataFrame(data)

# 2. Generating the Scalability Plot (Log Scale) with three lines
plt.figure(figsize=(9, 5))

plt.plot(df['N Vars (n)'], df['Total (ms)'], marker='o', linestyle='-', color='blue', label='Total')
plt.plot(df['N Vars (n)'], df['Phase1 (ms)'], marker='s', linestyle='--', color='green', label='Phase 1')
plt.plot(df['N Vars (n)'], df['Phase2 (ms)'], marker='^', linestyle='-.', color='red', label='Phase 2')

# The Y-axis must be logarithmic to clearly visualize exponential growth
plt.yscale('log')

plt.title('Quine-McCluskey Algorithm Performance: Runtime vs. Variables (n)', fontsize=14)
plt.xlabel('Number of Variables (n)', fontsize=12)
plt.ylabel('Time (ms) - Logarithmic Scale', fontsize=12)
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.legend()

# Adding time labels (optional)
for i, row in df.iterrows():
    # Position the label above each point
    plt.text(row['N Vars (n)'], row['Total (ms)'], f"{row['Total (ms)']:.1f}", 
             ha='left', va='bottom', fontsize=9)

# Save the plot as PDF (best quality for IEEE template)
plt.savefig('runtime_scalability_qmc.pdf', bbox_inches='tight')
print("Plot 'runtime_scalability_qmc.pdf' generated successfully!")

# 3. Displaying the Table (Optional)
print("\n--- Results Table ---")
# Adjust column names for printing the table
df.columns = ['N Vars (n)', 'Minterms', 'Don\'t Cares', 'Avg Time (ms)']
print(df.to_string(index=False))