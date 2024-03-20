import networkx as nx
import matplotlib.pyplot as plt
from queue import PriorityQueue
from collections import namedtuple

def astar(graph, heuristic, start, goal):
    g_score = {}
    f_score = {}
    h_score = heuristic

    g_score[start] = 0
    f_score[start] = g_score[start] + h_score[start]

    queue = PriorityQueue()
    Item = namedtuple("Item", ["f_score", "h_score", "city"])
    queue.put(Item(f_score[start], h_score[start], start))

    explored = {}

    while not queue.empty():
        current = queue.get().city

        if current == goal:
            break

        for neighbor, distance in graph[current].items():
            new_g_score = g_score[current] + distance

            if neighbor not in g_score or new_g_score < g_score[neighbor]:
                g_score[neighbor] = new_g_score
                f_score[neighbor] = g_score[neighbor] + h_score[neighbor]

                item = Item(f_score[neighbor], h_score[neighbor], neighbor)
                queue.put(item)

                explored[neighbor] = current

    # Reversão do caminho
    path = []
    current = goal
    while current != start:
        if current not in explored:
            raise ValueError("Não há caminho de {} para {}".format(start, goal))
        path.append(current)
        current = explored[current]
    path.append(start)
    path.reverse()

    return path, g_score, f_score

# Definindo o grafo original
graph = {
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Zerind": {"Oradea": 71, "Arad": 75},
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Sibiu": {"Oradea": 151, "Arad": 140, "Fagaras": 99, "Rimnicu Vilcea": 80},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Craiova": {"Drobeta": 120, "Rimnicu Vilcea": 146, "Pitesti": 138},
    "Rimnicu Vilcea": {"Craiova": 146, "Pitesti": 97, "Sibiu": 80},
    "Fagaras": {"Sibiu": 99, "Bucareste": 211},
    "Pitesti": {"Craiova": 138, "Rimnicu Vilcea": 97, "Bucareste": 101},
    "Bucareste": {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90, "Urziceni": 85},
    "Giurgiu": {"Bucareste": 90},
    "Urziceni": {"Bucareste": 85, "Hirsova": 98, "Vaslui": 142},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Eforie": {"Hirsova": 86},
    "Vaslui": {"Urziceni": 142, "Iasi": 92},
    "Iasi": {"Vaslui": 92, "Neamt": 87},
    "Neamt": {"Iasi": 87}
}

# Definindo a heurística
heuristic = {
    "Arad": 366,
    "Bucareste": 0,
    "Craiova": 160,
    "Drobeta": 242,
    "Eforie": 161,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Hirsova": 151,
    "Iasi": 226,
    "Lugoj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374
}

# Definindo o nó de início e o nó de destino
start = "Arad"
goal = "Bucareste"

# Calculando o caminho usando A*
path, g_score, f_score = astar(graph, heuristic, start, goal)

cost = 0
for i in range(len(path) - 1):
    cost += graph[path[i]][path[i+1]]

print("Shortest path: ", path)
print("Total cost:", cost)
print("G Score: ", g_score)
print("F Score: ", f_score)

# Criando um grafo sem direção para visualização
G = nx.Graph()
for node, neighbors in graph.items():
    G.add_node(node)
    for neighbor, weight in neighbors.items():
        G.add_edge(node, neighbor, weight=weight)

# Criando a posição dos nós para visualização
pos = nx.spring_layout(G)

# Desenhando o grafo completo
nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=12, font_weight="bold")

# Destacando o caminho ótimo
path_edges = list(zip(path, path[1:]))
nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="orange", node_size=700)
nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2, alpha=0.5, edge_color="red")

# Adicionando rótulos de peso nas arestas
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Exibindo a plotagem
plt.title("Caminho encontrado por A*")
plt.axis("off")
plt.show()
