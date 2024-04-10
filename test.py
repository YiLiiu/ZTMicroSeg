import random
import networkx as nx
import matplotlib.pyplot as plt


def ControlZone_graphGenerator(N, topology_types=["mesh", "star", "ring", "bus"]):
    toplogy = random.choice(topology_types)
    if toplogy == "mesh":
        G = nx.complete_graph(N)
    elif toplogy == "star":
        G = nx.star_graph(N - 1)
    elif toplogy == "ring":
        G = nx.cycle_graph(N)
    elif toplogy == "bus":
        G = nx.path_graph(N)
    return G


N = 5  # 节点总数


G = ControlZone_graphGenerator(N, ["bus"])

# 画图
plt.figure(figsize=(8, 6))
nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray')
plt.title("Network Topology")
plt.show()