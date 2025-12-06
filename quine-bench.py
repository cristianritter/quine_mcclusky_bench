import random
from time import perf_counter

from timed_qm import TimedQuineMcCluskey

# --- TEST CONFIGURATIONS ---
NUM_EXECUTIONS_PER_TEST = 1
VAR_MIN = 4
VAR_MAX = 13
# For each N variables, we'll use about 25% of possible minterms.
# This ensures a good number of prime implicants to challenge the algorithm.
DENSITY_MINTERMS = 0.25 
# ----------------------------

def generate_random_function(n, density):
    """Generates random minterms for n variables based on density."""
    max_minterm = 2**n - 1
    num_minterms = int(max_minterm * density)
    
    # Select random minterms (without repetition)
    minterms = random.sample(range(max_minterm + 1), num_minterms)
    
    # Optional: Add some don't cares (e.g., 5% of total)
    num_dont_cares = int(max_minterm * 0.05)
    
    # Generate don't cares from the remaining universe
    remaining_minterms = list(set(range(max_minterm + 1)) - set(minterms))
    dont_cares = random.sample(remaining_minterms, min(len(remaining_minterms), num_dont_cares))
    
    return minterms, dont_cares

def run_performance_test(n, minterms, dont_cares, num_executions):
    """Executes QMC and measures average time for total, phase1 and phase2."""
    if not minterms and not dont_cares:
        return 0.0, 0.0, 0.0

    total_time = 0.0
    total_phase1 = 0.0
    total_phase2 = 0.0

    # Measures time over multiple executions (without prints)
    for _ in range(num_executions):
        qm = TimedQuineMcCluskey()
        start = perf_counter()
        qm.simplify(minterms, dont_cares)
        end = perf_counter()

        total_time += end - start
        total_phase1 += getattr(qm, "time_phase1", 0.0)
        total_phase2 += getattr(qm, "time_phase2", 0.0)

    avg_time = total_time / num_executions
    avg_phase1 = total_phase1 / num_executions
    avg_phase2 = total_phase2 / num_executions

    return avg_time, avg_phase1, avg_phase2

# --- MAIN TEST LOOP ---

print(f"Starting QMC Scalability Test ({VAR_MIN} to {VAR_MAX} variables)")
print("-" * 95)
print(f"| N Vars | Minterms | Don't Cares | Total (ms) | Phase1 (ms) | Phase2 (ms) |")
print("-" * 95)

# List to store results (for plotting the graph in the report)
results_data = []

for n in range(VAR_MIN, VAR_MAX + 1):
    # 1. Generate random function for N variables
    minterms, dont_cares = generate_random_function(n, DENSITY_MINTERMS)

    # 2. Execute performance test
    avg_time_s, phase1_s, phase2_s = run_performance_test(
        n, minterms, dont_cares, NUM_EXECUTIONS_PER_TEST
    )
    avg_time_ms = avg_time_s * 1000
    phase1_ms = phase1_s * 1000
    phase2_ms = phase2_s * 1000

    # 3. Store and print the result
    results_data.append({
        'n_vars': n,
        'num_minterms': len(minterms),
        'time_ms_total': avg_time_ms,
        'time_ms_phase1': phase1_ms,
        'time_ms_phase2': phase2_ms,
    })

    print(
        f"| {n:^6} | {len(minterms):^8} | {len(dont_cares):^11} | "
        f"{avg_time_ms:^10.4f} | {phase1_ms:^11.4f} | {phase2_ms:^11.4f} |"
    )

print("-" * 95)
print("Test completed.")