# Quine–McCluskey Runtime Scalability Study

This repository contains the code used in a **Masters degree course on Electronic Design Automation (EDA)** to study the **runtime scalability of the QuineMcCluskey (QMC) Boolean minimization algorithm**.

The project is composed of:

- **A benchmark script** that runs the QuineMcCluskey algorithm for randomly generated Boolean functions with different numbers of variables.
- **A plotting script** that generates a **log-scale runtime vs. number-of-variables plot** and prints the data table used in the report.

The generated plot is saved as `runtime_scalability_qmc.pdf`, suitable for inclusion in an academic report or paper.

---

## 1. Project Structure

- `quine-bench.py`
  - Generates random Boolean functions for `n` variables.
  - Runs the QuineMcCluskey algorithm (via a timing wrapper) multiple times for each `n`.
  - Measures and prints the **average runtime**, split into **Total**, **Phase 1** (Prime Implicant generation) and **Phase 2** (Minimal Covering) for each number of variables.
  - This script is used to obtain the timing data that can be manually transferred to the plotting script or to a report.

- `graphic-gen.py`
  - Contains the **experimental data** in a Python dictionary (number of variables, number of minterms, number of don't cares, and measured runtimes in milliseconds).
  - Builds a **Pandas DataFrame** from those values.
  - Generates a **log-scale runtime vs. variables plot** using Matplotlib with three curves: **Total**, **Phase 1**, and **Phase 2**.
  - Saves the plot as `runtime_scalability_qmc.pdf` and prints a formatted results table.

- `runtime_scalability_qmc.pdf`
  - Example of the generated scalability plot for the QMC algorithm (already in the repository).

- `venv/`
  - Optional local virtual environment directory (not required for understanding the code, but useful for isolating dependencies).

---

## 2. Dependencies

The project is written in **Python 3** and depends on:

- `quine-mccluskey` (Python implementation of the QuineMcCluskey algorithm)
- `pandas`
- `matplotlib`
- `numpy`

### Installation

It is recommended to create and activate a virtual environment, then install the dependencies:

```bash
pip install quine-mccluskey pandas matplotlib numpy
```

If you prefer, you can also create a `requirements.txt` with these packages.

---

## 3. Benchmark Script: `quine-bench.py`

This script measures the **average runtime** of the QuineMcCluskey algorithm as the number of variables increases, decomposed into total time and the times of Phase 1 (Prime Implicant Generation) and Phase 2 (Minimal Covering).

### Configuration

The following constants are defined at the top of `quine-bench.py` (all comments are in Portuguese, matching the course context):

- `NUM_EXECUCOES_POR_TESTE`
  - Number of repetitions of the simplification for each configuration to obtain a more stable average time for total, Phase 1 and Phase 2.
  - Default in the script is set for **quick tests**. For final experiments, you can increase this to smooth out measurement noise.

- `VAR_MIN`, `VAR_MAX`
  - Minimum and maximum number of variables to test (inclusive).

- `DENSIDADE_MINTERMS`
  - Approximate fraction of possible minterms that will be included as **ones** in the random function (e.g. `0.25` = 25%).
  - Ensures a non-trivial number of prime implicants.

### How it works

1. For each `n` in `VAR_MIN` to `VAR_MAX`:
   - The function `generate_random_function(n, density)`:
     - Computes the maximum number of minterms: `2**n - 1`.
     - Selects a random subset of minterms according to the given density (without repetition).
     - Selects about **5%** of the full space as "don't care" conditions, from the remaining minterms.
   - The function `run_performance_test(...)`:
     - Instantiates a timing wrapper around `QuineMcCluskey`.
     - Calls `qm.simplify(minterms, dont_cares)` in a loop `NUM_EXECUCOES_POR_TESTE` times.
     - Uses `time.perf_counter()` and internal timers to measure the **average total time**, **average Phase 1 time**, and **average Phase 2 time** per call.
   - The script prints a formatted table row with:
     - Number of variables,
     - Number of minterms,
     - Number of don't cares,
     - Average total runtime in milliseconds,
     - Average Phase 1 runtime in milliseconds,
     - Average Phase 2 runtime in milliseconds.

2. At the end, a summary line is printed indicating that the test is finished and that the data can be used to generate the scalability plot for the report.

> Note: The list `results_data` is populated but not written to a file in this version. Data is currently read from visual inspection of the console output or manually transferred to `graphic-gen.py`.

### Running the benchmark

From the project root:

```bash
python quine-bench.py
```

You will see an output table similar to:

```text
Starting QMC Scalability Test (4 to 13 variables)
-----------------------------------------------------------------------------------------------
| N Vars | Minterms | Don't Cares | Total (ms) | Phase1 (ms) | Phase2 (ms) |
-----------------------------------------------------------------------------------------------
|   4    |    3     |      0      |   0.5484   |   0.0299    |   0.4748    |
|  ...   |   ...    |    ...      |    ...     |    ...      |    ...      |
-----------------------------------------------------------------------------------------------
Test completed.
```

Adjust the configuration constants at the top of the file to match the desired experimental setup for your report.

---

## 4. Plot Script: `graphic-gen.py`

This script produces the **final figure** for the report.

### Data definition

At the top of the file, a Python dictionary named `data` is defined with columns:

- `N Vars (n)`
- `Minterms`
- `Don't Cares`
- `Total (ms)`
- `Phase1 (ms)`
- `Phase2 (ms)`

These values correspond to the chosen experimental configuration and to the average timing results (total and by phase) obtained from `quine-bench.py`.

### Plot generation

Steps executed by `graphic-gen.py`:

1. Creates a `pandas.DataFrame` from `data`.
2. Uses `matplotlib` to plot **Total (ms)**, **Phase1 (ms)** and **Phase2 (ms)** vs. **Number of Variables (n)**.
3. Sets the **Y-axis to logarithmic scale** (`plt.yscale('log')`) to highlight the exponential growth of runtime.
4. Adds labels, grid, and optional value labels above each point.
5. Saves the figure as `runtime_scalability_qmc.pdf` with tight bounding boxes for high-quality inclusion in LaTeX / IEEE templates.
6. Prints a formatted table version of the same data for reference.

### Running the plot script

From the project root:

```bash
python graphic-gen.py
```

If everything is correctly installed, you will see a message like:

```text
Plot 'runtime_scalability_qmc.pdf' generated successfully!

--- Results Table ---
 N Vars (n)  Minterms  Don't Cares  Avg Time (ms)
          4         3            0         0.1178
          5         7            1         0.5150
          ...     ...          ...            ...
```

The file `runtime_scalability_qmc.pdf` will be created/overwritten in the project root.

---

## 5. Academic Context (EDA / Masters Course)

This code base is designed as part of a **graduate-level EDA (Electronic Design Automation) subject** to:

- Illustrate how **exact Boolean minimization** (QuineMcCluskey) behaves in terms of runtime for increasing number of variables.
- Show how to conduct a controlled **performance experiment**:
  - Define parameters (number of variables, density of minterms, number of executions).
  - Collect and aggregate runtime data.
  - Visualize results on a log scale.
- Provide material for **discussion on scalability limits** of exact methods versus heuristic approaches used in real-world EDA tools.

You can easily adapt the configuration or the plotting script to explore different densities, numbers of executions, or to compare other algorithms.

---

## 6. How to Reproduce the Results

1. **Install dependencies** (inside a virtual environment is recommended):

   ```bash
   pip install quine-mccluskey pandas matplotlib numpy
   ```

2. **Run the benchmark** to obtain runtime measurements for the desired range of variables:

   ```bash
   python quine-bench.py
   ```

   Optionally adjust `NUM_EXECUCOES_POR_TESTE`, `VAR_MIN`, `VAR_MAX`, and `DENSIDADE_MINTERMS` in the script.

3. **Update the data** in `graphic-gen.py` with the new experimental values (if different from the current ones).

4. **Generate the figure** for your report:

   ```bash
   python graphic-gen.py
   ```

5. Include `runtime_scalability_qmc.pdf` in your LaTeX or Word document as the figure illustrating the scalability of the QuineMcCluskey algorithm.

---

## 7. License / Usage

This code is intended for **academic and educational use** in the context of a Masters level EDA course. If you plan to redistribute or publish this repository, you may want to explicitly choose a license (e.g., MIT, Apache-2.0, or a custom academic license) and update this section accordingly.
