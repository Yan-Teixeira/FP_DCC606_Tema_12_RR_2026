import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np

def repair_individual(individual, edges_indices, degrees):
    """
    Operador Heurístico para resolver a Inviabilidade Espacial.
    Garante que toda aresta tenha pelo menos um vértice no cover.
    """
    repaired = list(individual)
    for u, v in edges_indices:
        if repaired[u] == 0 and repaired[v] == 0:
            # Eficiência fiscal: prioriza o cruzamento com maior grau (mais vias)
            if degrees[u] > degrees[v]:
                repaired[u] = 1
            else:
                repaired[v] = 1
    return repaired

def calculate_fitness(individual):
    # O fitness é o número de ativos alocados. O objetivo é minimizar.
    return sum(individual)

def tournament_selection(pop, fitnesses, k=3):
    selected = random.sample(range(len(pop)), k)
    best_idx = min(selected, key=lambda i: fitnesses[i])
    return pop[best_idx]

def genetic_algorithm_mvc(graph, pop_size=100, generations=100, mutation_rate=0.05):
    nodes = list(graph.nodes())
    edges_indices = [(nodes.index(u), nodes.index(v)) for u, v in graph.edges()]
    degrees = [graph.degree(n) for n in nodes]
    num_vertices = len(nodes)
    
    # População inicial gerada e imediatamente reparada
    population = [[random.choice([0, 1]) for _ in range(num_vertices)] for _ in range(pop_size)]
    population = [repair_individual(ind, edges_indices, degrees) for ind in population]
    
    best_history, avg_history = [], []
    global_best = None
    global_best_fitness = float('inf')
    
    for gen in range(generations):
        fitnesses = [calculate_fitness(ind) for ind in population]
        best_gen_fitness = min(fitnesses)
        avg_gen_fitness = np.mean(fitnesses)
        
        best_history.append(best_gen_fitness)
        avg_history.append(avg_gen_fitness)
        
        # Elitismo: preserva o melhor indivíduo
        best_idx = fitnesses.index(best_gen_fitness)
        if best_gen_fitness < global_best_fitness:
            global_best_fitness = best_gen_fitness
            global_best = population[best_idx]
            
        new_pop = [population[best_idx]]
        
        while len(new_pop) < pop_size:
            p1 = tournament_selection(population, fitnesses)
            p2 = tournament_selection(population, fitnesses)
            
            # Crossover de 1 ponto
            pt = random.randint(1, num_vertices - 1)
            c1, c2 = p1[:pt] + p2[pt:], p2[:pt] + p1[pt:]
            
            # Mutação
            for i in range(num_vertices):
                if random.random() < mutation_rate: c1[i] = 1 - c1[i]
                if random.random() < mutation_rate: c2[i] = 1 - c2[i]
            
            # Reparo Heurístico Pós-Mutação
            c1 = repair_individual(c1, edges_indices, degrees)
            c2 = repair_individual(c2, edges_indices, degrees)
            
            new_pop.extend([c1, c2])
            
        population = new_pop[:pop_size]
        
    return global_best, global_best_fitness, best_history, avg_history

# --- Cenário Realista: Rede de Monitoramento Urbano ---
# Simulação de interseções contendo no mínimo 50 vértices com conexões densas e esparsas
urb_graph = nx.barabasi_albert_graph(50, 3) 
best_cover, best_fit, best_hist, avg_hist = genetic_algorithm_mvc(urb_graph, pop_size=50, generations=150)

print("--- Malha Urbana Teste ---")
print(f"Vértices: {urb_graph.number_of_nodes()} | Arestas: {urb_graph.number_of_edges()}")
print(f"Melhor Cobertura (Ativos Posicionados): {best_fit}")

# --- Módulo de Visualização Gráfica ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Tela 1: Topologia e Solução
pos = nx.spring_layout(urb_graph)
colors = ['red' if best_cover[i] == 1 else 'lightblue' for i in range(len(urb_graph.nodes))]
nx.draw(urb_graph, pos, node_color=colors, with_labels=True, node_size=300, ax=ax1, font_size=8)
ax1.set_title("Cenário Realista: Ativos de Segurança (Vermelho)")

# Tela 2: Gráfico de Convergência
ax2.plot(best_hist, label="Melhor Fitness (Menor Cobertura)", color="blue", linewidth=2)
ax2.plot(avg_hist, label="Fitness Médio da População", color="orange", linestyle="--")
ax2.set_title("Comportamento da Evolução")
ax2.set_xlabel("Geração")
ax2.set_ylabel("Tamanho da Cobertura")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()

# Nota: Para os testes de estresse DIMACS, basta carregar o arquivo .col lendo 
# as linhas iniciadas em 'e' e usar urb_graph.add_edge(u, v).