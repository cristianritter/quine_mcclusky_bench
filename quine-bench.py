import random
from quine_mccluskey.qm import QuineMcCluskey
from time import perf_counter

# --- CONFIGURAÇÕES DO TESTE ---
NUM_EXECUCOES_POR_TESTE = 10  # Reduzido para testes rápidos (Aumente para 100+ no teste final)
VAR_MIN = 4
VAR_MAX = 12
# Para cada N variáveis, usaremos cerca de 25% dos minterms possíveis.
# Isso garante um bom número de implicantes primos para desafiar o algoritmo.
DENSIDADE_MINTERMS = 0.25 
# -----------------------------

def generate_random_function(n, density):
    """Gera minterms aleatórios para n variáveis com base na densidade."""
    max_minterm = 2**n - 1
    num_minterms = int(max_minterm * density)
    
    # Seleciona minterms aleatórios (sem repetição)
    minterms = random.sample(range(max_minterm + 1), num_minterms)
    
    # Opcional: Adicionar alguns don't cares (ex: 5% do total)
    num_dont_cares = int(max_minterm * 0.05)
    
    # Gera don't cares a partir do que sobrou do universo
    remaining_minterms = list(set(range(max_minterm + 1)) - set(minterms))
    dont_cares = random.sample(remaining_minterms, min(len(remaining_minterms), num_dont_cares))
    
    return minterms, dont_cares

def run_performance_test(n, minterms, dont_cares, num_execucoes):
    """Executa o QMC e mede o tempo médio."""
    if not minterms and not dont_cares:
        return 0.0

    # Mede o tempo de várias execuções (sem prints)
    start = perf_counter()
    for _ in range(num_execucoes):
        qm = QuineMcCluskey(False)
        qm.simplify(minterms, dont_cares)
    end = perf_counter()

    return (end - start) / num_execucoes

# --- LOOP PRINCIPAL DE TESTE ---

print(f"Iniciando Teste de Escalabilidade QMC ({VAR_MIN} a {VAR_MAX} variáveis)")
print("-" * 50)
print(f"| N Vars | Minterms | Don't Cares | Tempo Médio (ms) |")
print("-" * 50)

# Lista para armazenar os resultados (para plotar o gráfico no relatório)
results_data = []

for n in range(VAR_MIN, VAR_MAX + 1):
    # 1. Gera função aleatória para N variáveis
    minterms, dont_cares = generate_random_function(n, DENSIDADE_MINTERMS)
    
    # 2. Executa o teste de performance
    tempo_medio_s = run_performance_test(n, minterms, dont_cares, NUM_EXECUCOES_POR_TESTE)
    tempo_medio_ms = tempo_medio_s * 1000

    # 3. Armazena e imprime o resultado
    results_data.append({
        'n_vars': n,
        'num_minterms': len(minterms),
        'time_ms': tempo_medio_ms
    })
    
    print(f"| {n:^6} | {len(minterms):^8} | {len(dont_cares):^11} | {tempo_medio_ms:^16.4f} |")

print("-" * 50)
print("Teste concluído. Use os dados acima para gerar o gráfico de escalabilidade (Seção III).")