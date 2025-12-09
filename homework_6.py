import networkx as nx
import matplotlib.pyplot as plt
import sys

# Налаштування виводу (UTF-8)
sys.stdout.reconfigure(encoding='utf-8')

# ====== ЗАВДАННЯ 1 ======
# Створення графа
print("====== ЗАВДАННЯ 1: Створення та аналіз графа ======")

# Створення графа (Транспортна мережа)
G = nx.Graph()

# Додавання міст
cities = ["Київ", "Львів", "Одеса", "Харків", "Дніпро", "Житомир"]
G.add_nodes_from(cities)

# Додавання доріг та відстаней
roads = [
    ("Київ", "Житомир", 140),
    ("Київ", "Харків", 480),
    ("Київ", "Одеса", 475),
    ("Київ", "Дніпро", 450),
    ("Житомир", "Львів", 400),
    ("Львів", "Одеса", 790),
    ("Харків", "Дніпро", 220),
    ("Дніпро", "Одеса", 450)
]
G.add_weighted_edges_from(roads)

# Візуалізація графа
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=12, font_weight='bold')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Транспортна мережа міст")
# plt.show()
plt.savefig("graph_visualization.png")
print("Граф збережено у 'graph_visualization.png'")

# Аналіз графа
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
degrees = dict(G.degree())

print(f"Кількість вершин (міст): {num_nodes}")
print(f"Кількість ребер (доріг): {num_edges}")
print("Ступінь вершин (кількість доріг з кожного міста):")
for city, degree in degrees.items():
    print(f"  {city}: {degree}")


# ====== ЗАВДАННЯ 2 ======


print("\n====== ЗАВДАННЯ 2: DFS та BFS ======")

start_node = "Київ"
print(f"Початкова вершина для обходу: {start_node}")

# DFS (Пошук у глибину)

dfs_path = list(nx.dfs_preorder_nodes(G, source=start_node))
print(f"Шлях DFS (глибина): {dfs_path}")

# BFS (Пошук у ширину)

bfs_path = list(nx.bfs_tree(G, source=start_node))
print(f"Шлях BFS (ширина): {bfs_path}")

# Порівняння та пояснення
print("\nПояснення різниці:")
print(f"DFS (Depth-First Search) йде 'вглиб' графа. З '{start_node}' він йде до першого сусіда (наприклад, '{dfs_path[1]}'), "
      f"потім до його сусіда і так далі, поки не дійде до тупика, після чого повертається назад.")
print(f"BFS (Breadth-First Search) йде 'вшир'. З '{start_node}' він спочатку відвідує всіх безпосередніх сусідів "
      f"({', '.join(bfs_path[1:1+degrees[start_node]])}), і тільки потім переходить до сусідів сусідів.")


# ====== ЗАВДАННЯ 3 ======


print("\n====== ЗАВДАННЯ 3: Алгоритм Дейкстри ======")

# Реалізація алгоритму Дейкстри
def dijkstra(graph, start):
    # Ініціалізація відстаней
    distances = {node: float('infinity') for node in graph.nodes}
    distances[start] = 0
    
    # Невідвідані вершини
    unvisited = list(graph.nodes)
    
    while unvisited:
        # Найближча вершина
        current_node = min(unvisited, key=lambda node: distances[node])
        
        # Перевірка досяжності
        if distances[current_node] == float('infinity'):
            break
            
        # Перевірка сусідів
        for neighbor, attributes in graph[current_node].items():
            weight = attributes.get('weight', 1)
            new_distance = distances[current_node] + weight
            
            # Оновлення відстані
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
        
        # Вершина оброблена
        unvisited.remove(current_node)
    
    return distances

# Пошук шляхів
start_city = "Київ"
shortest_paths = dijkstra(G, start_city)

# Виведення результатів
print(f"Найкоротші шляхи від міста {start_city}:")
print(f"{'Місто':<15} | {'Відстань (км)':<15}")
print("-" * 35)
for city, distance in shortest_paths.items():
    print(f"{city:<15} | {distance:<15}")

# Перевірка (NetworkX)
print("\nПеревірка (NetworkX built-in):")
nx_lengths = nx.single_source_dijkstra_path_length(G, start_city)
print(nx_lengths)
