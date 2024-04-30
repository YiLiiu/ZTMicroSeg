import networkx as nx
import matplotlib.pyplot as plt
import itertools
import random

class GenindNetwork:

    def __init__(self, N1, Type1, U2, N2, U3, N3, plot=True):
        self.node_labels = {}
        self.n3 = []
        self.graph = self.MULTI_GRAPHGENERATOR_AND_DRAW(N1, Type1, U2, N2, U3, N3, plot=plot)


    def NetworkZone_graphGenerator(self, N, Type):
        if Type == "Random Geometric":
            radius = 1.0
            G = nx.random_geometric_graph(N, radius)
        elif Type == "Waxman":
            alpha = 1.0
            beta = 1.0
            G = nx.waxman_graph(N, alpha, beta)
        else:
            raise ValueError("Invalid topology type specified.")
        return G

    def ControlZone_graphGenerator(self, N, topology_types=["mesh", "star", "ring", "bus"]):
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

    def adjust_node_ids(self, G, offset):
        """将图G中的所有节点ID增加一个偏移量"""
        mapping = {node: node + offset for node in G.nodes}
        return nx.relabel_nodes(G, mapping)

    def MULTI_GRAPHGENERATOR_AND_DRAW(self, N1, Type1, U2, N2, U3, N3, plot=True):
        G1 = self.NetworkZone_graphGenerator(N1, Type1)
        G2_list = [self.ControlZone_graphGenerator(N2) for _ in range(U2)]
        G3_list = [self.ControlZone_graphGenerator(N3) for _ in range(U3)]
        
        big_graph = G1.copy()
        node_colors = {node: 'red' for node in G1.nodes}  # 为G1节点分配颜色
        node_labels = {node: 0 for node in G1.nodes}  # 为G1节点分配标签
        offset = max(G1.nodes) + 1  # 初始化偏移量

        # 按顺序连接并调整G2图的节点ID后添加到大图
        for i, G2 in enumerate(G2_list):
            G2_adjusted = self.adjust_node_ids(G2, offset)
            controller_node = list(G1.nodes)[i % len(G1.nodes)]

            big_graph = nx.compose(big_graph, G2_adjusted)
            big_graph.add_edge(controller_node, min(G2_adjusted.nodes))
            for node in G2_adjusted.nodes:
                node_colors[node] = 'green'
                node_labels[node] = i + 1
            offset += len(G2_adjusted.nodes)

        # 创建一个循环迭代器以便循环访问G2图
        G2_cycle = itertools.cycle([self.adjust_node_ids(G2, i * len(G2.nodes) + N1) for i, G2 in enumerate(G2_list)])

        # 按顺序连接并调整G3图的节点ID后添加到大图
        for G3 in G3_list:
            G2 = next(G2_cycle)
            G3_adjusted = self.adjust_node_ids(G3, offset)
            controller_node_G2 = random.choice(list(G2.nodes()))
            big_graph = nx.compose(big_graph, G3_adjusted)
            big_graph.add_edge(controller_node_G2, min(G3_adjusted.nodes))
            for node in G3_adjusted.nodes:
                self.n3.append(node)
                node_colors[node] = 'blue'
                node_labels[node] = node_labels[controller_node_G2]
            offset += len(G3_adjusted.nodes)

        if plot:
            print(f"Node Labels: {node_labels}")
            # 使用spring布局
            pos = nx.spring_layout(big_graph)

            # 绘制网络图
            plt.figure(figsize=(12, 8))
            nx.draw(big_graph, pos, node_color=[node_colors[node] for node in big_graph.nodes()], with_labels=True, node_size=700)

        self.node_labels = node_labels

        return big_graph
    
    def node_to_node_path(self, node1, node2):
        return nx.shortest_path(self.graph, node1, node2)
    
    def node_to_node_permission(self, node1, node2):
        path = self.node_to_node_path(node1, node2)
        permissions = set()
        for node in path:
            permissions.add(self.node_labels[node])

        return len(permissions)

    def cal_avg_path_time(self, num = 10000):
        # Randomly select num pairs of nodes and calculate the average path length
        # between them, based on the path length, calculate the average time by random

        total_time = 0
        for _ in range(num):
            node1 = random.choice(self.n3)
            node2 = random.choice(self.n3)
            path = self.node_to_node_path(node1, node2)
            total_time += (len(path) - 1) * random.uniform(0.1, 1)

        return total_time / num


# Parameters
N1, Type1, U2, N2, U3, N3 = 3, "Random Geometric", 3, 3, 3, 3

# net = GenindNetwork(N1, Type1, U2, N2, U3, N3)

# Plotting setup
fig, axs = plt.subplots(3, 1, figsize=(12, 9))

# Plot for varying N1
x1 = []
y1 = []
for k in range(N1, 5 * N1):
    gein_network = GenindNetwork(k, Type1, U2, N2, U3, N3, False)
    x1.append(k)
    y1.append(gein_network.cal_avg_path_time())
axs[0].plot(x1, y1, label=f"U2={U2}, N2={N2}, U3={U3}, N3={N3}")
axs[0].set_xlabel("Number of N1 nodes")
axs[0].set_ylabel("Average path time")
axs[0].legend()

# Plot for varying N2
x2 = []
y2 = []
for k in range(N2, 5 * N2):
    gein_network = GenindNetwork(N1, Type1, U2, k, U3, N3, False)
    x2.append(k)
    y2.append(gein_network.cal_avg_path_time())
axs[1].plot(x2, y2, label=f"N1={N1}, U2={U2}, U3={U3}, N3={N3}")
axs[1].set_xlabel("Number of N2 nodes")
axs[1].set_ylabel("Average path time")
axs[1].legend()

# Plot for varying N3
x3 = []
y3 = []
for k in range(N3, 5 * N3):
    gein_network = GenindNetwork(N1, Type1, U2, N2, U3, k, False)
    x3.append(k)
    y3.append(gein_network.cal_avg_path_time())
axs[2].plot(x3, y3, label=f"N1={N1}, U2={U2}, N2={N2}")
axs[2].set_xlabel("Number of N3 nodes")
axs[2].set_ylabel("Average path time")
axs[2].legend()


# x4 = []
# y4 = []
# for k in range(U2, 3 * U2):
#     gein_network = GenindNetwork(N1, Type1, k, N2, U3, N3, False)
#     x4.append(k*N2)
#     y4.append(gein_network.cal_avg_path_time())
# axs[3].plot(x4, y4, label=f"N1={N1}, N2={N2}, N3={N3}")
# axs[3].set_xlabel("Number of U2 * N2 nodes")
# axs[3].set_ylabel("Average path time")
# axs[3].legend()


# x5 = []
# y5 = []
# for k in range(U3, 3 * U3):
#     gein_network = GenindNetwork(N1, Type1, U2, N2, k, N3, False)
#     x5.append(k*N3)
#     y5.append(gein_network.cal_avg_path_time())
# axs[4].plot(x5, y5, label=f"N1={N1}, N2={N2}, N3={N3}")
# axs[4].set_xlabel("Number of U3 * N3 nodes")
# axs[4].set_ylabel("Average path time")
# axs[4].legend()


plt.tight_layout()
plt.show()
