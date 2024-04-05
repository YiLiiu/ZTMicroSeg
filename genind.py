import networkx as nx
import matplotlib.pyplot as plt
import itertools
import random

def NetworkZone_graphGenerator(N, Type):
    if Type == "Random Geometric":
        radius = 0.5
        G = nx.random_geometric_graph(N, radius)
    elif Type == "Waxman":
        alpha = 0.8
        beta = 0.1
        G = nx.waxman_graph(N, alpha, beta)
    else:
        raise ValueError("Invalid topology type specified.")
    return G

def ControlZone_graphGenerator(N, U, topology_types=["mesh", "star", "ring", "bus"]):
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

def adjust_node_ids(G, offset):
    """将图G中的所有节点ID增加一个偏移量"""
    mapping = {node: node + offset for node in G.nodes}
    return nx.relabel_nodes(G, mapping)

def MULTI_GRAPHGENERATOR_AND_DRAW(N1, Type1, U2, N2, Type2, U3, N3, Type3):
    G1 = NetworkZone_graphGenerator(N1, Type1)
    G2_list = [ControlZone_graphGenerator(N2, 1, [Type2]) for _ in range(U2)]
    G3_list = [ControlZone_graphGenerator(N3, 1, [Type3]) for _ in range(U3)]
    
    big_graph = G1.copy()
    node_colors = {node: 'red' for node in G1.nodes}  # 为G1节点分配颜色
    offset = max(G1.nodes) + 1  # 初始化偏移量

    # 按顺序连接并调整G2图的节点ID后添加到大图
    for i, G2 in enumerate(G2_list):
        G2_adjusted = adjust_node_ids(G2, offset)
        controller_node = list(G1.nodes)[i % len(G1.nodes)]
        big_graph = nx.compose(big_graph, G2_adjusted)
        big_graph.add_edge(controller_node, min(G2_adjusted.nodes))
        for node in G2_adjusted.nodes:
            node_colors[node] = 'green'
        offset += len(G2_adjusted.nodes)

    # 创建一个循环迭代器以便循环访问G2图
    G2_cycle = itertools.cycle([adjust_node_ids(G2, i * len(G2.nodes) + N1) for i, G2 in enumerate(G2_list)])

    # 按顺序连接并调整G3图的节点ID后添加到大图
    for G3 in G3_list:
        G2 = next(G2_cycle)
        G3_adjusted = adjust_node_ids(G3, offset)
        controller_node_G2 = min(G2.nodes())
        big_graph = nx.compose(big_graph, G3_adjusted)
        big_graph.add_edge(controller_node_G2, min(G3_adjusted.nodes))
        for node in G3_adjusted.nodes:
            node_colors[node] = 'blue'
        offset += len(G3_adjusted.nodes)

    # 使用spring布局
    pos = nx.spring_layout(big_graph)

    # 绘制网络图
    plt.figure(figsize=(12, 8))
    nx.draw(big_graph, pos, node_color=[node_colors[node] for node in big_graph.nodes()], with_labels=True, node_size=700)
    plt.show()

# 调用函数的参数设置
N1 = 3
Type1 = "Random Geometric"
U2 = 3
N2 = 3
Type2 = "bus"
U3 = 9
N3 = 3
Type3 = "bus"

# 调用函数来生成和显示图像
MULTI_GRAPHGENERATOR_AND_DRAW(N1, Type1, U2, N2, Type2, U3, N3, Type3)
