import networkx as nx
import matplotlib.pyplot as plt
import itertools
import random

class GenindNetwork:

    def __init__(self, N1, Type1, U2, N2, Type2, U3, N3, Type3):
        self.node_labels = {}
        self.graph = self.MULTI_GRAPHGENERATOR_AND_DRAW(N1, Type1, U2, N2, Type2, U3, N3, Type3)



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

    def ControlZone_graphGenerator(self, N, U, topology_types=["mesh", "star", "ring", "bus"]):
        if U <= N:
            controller_nodes = list(range(U))
        else:
            controller_nodes = random.sample(range(N), U)
        G = nx.Graph()
        G.add_nodes_from(range(N))
        for node in controller_nodes:
            topology_type = random.choice(topology_types)
            if topology_type == "mesh":
                for n in range(N):
                    if n != node:
                        G.add_edge(node, n)
            elif topology_type == "star":
                if controller_nodes:
                    center_node = controller_nodes[0]  # Assume the first controller node is the center for star topology
                    if node != center_node:
                        G.add_edge(center_node, node)
            elif topology_type == "ring":
                nodes = [n for n in range(N) if n != node]
                for i in range(len(nodes)):
                    G.add_edge(nodes[i], nodes[(i + 1) % len(nodes)])
            elif topology_type == "bus":
                if controller_nodes:
                    bus_node = controller_nodes[0]  # Assume the first controller node acts as a bus
                    for n in range(N):
                        if n != bus_node:
                            G.add_edge(bus_node, n)
        return G

    def adjust_node_ids(self, G, offset):
        """将图G中的所有节点ID增加一个偏移量"""
        mapping = {node: node + offset for node in G.nodes}
        return nx.relabel_nodes(G, mapping)

    def MULTI_GRAPHGENERATOR_AND_DRAW(self, N1, Type1, U2, N2, Type2, U3, N3, Type3):
        G1 = self.NetworkZone_graphGenerator(N1, Type1)
        G2_list = [self.ControlZone_graphGenerator(N2, 1, [Type2]) for _ in range(U2)]
        G3_list = [self.ControlZone_graphGenerator(N3, 1, [Type3]) for _ in range(U3)]
        
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
            controller_node_G2 = min(G2.nodes())
            big_graph = nx.compose(big_graph, G3_adjusted)
            big_graph.add_edge(controller_node_G2, min(G3_adjusted.nodes))
            for node in G3_adjusted.nodes:
                node_colors[node] = 'blue'
                node_labels[node] = node_labels[controller_node_G2]
            offset += len(G3_adjusted.nodes)

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


# 调用函数的参数设置
N1 = 3
Type1 = "Random Geometric"
U2 = 3
N2 = 3
Type2 = "bus"
U3 = 9
N3 = 3
Type3 = "bus"

# # 调用函数来生成和显示图像
gein_network = GenindNetwork(N1, Type1, U2, N2, Type2, U3, N3, Type3)



print(gein_network.node_to_node_path(1, 10))
print(gein_network.node_to_node_permission(1, 10))

plt.show()
