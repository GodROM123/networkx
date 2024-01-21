import networkx as nx

# 创建一个包含1000个节点的无标度网络
N = 1000
network = nx.barabasi_albert_graph(N, 3)

# 计算度中心性
degree_centrality = nx.degree_centrality(network)

# 选择度中心性前5%的节点并添加二度连接
top_5_percent = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:int(0.05 * N)]
network_reset = network.copy()  # 重置网络到初始状态
for node in top_5_percent:
    neighbors = list(network_reset.neighbors(node))
    added_edges = 0
    for i in range(len(neighbors)):
        for j in range(i + 1, len(neighbors)):
            if added_edges >= 2:
                break
            network_reset.add_edge(neighbors[i], neighbors[j])
            added_edges += 1
        if added_edges >= 2:
            break

# 定义攻击的不同比例
attack_percentages = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

# 存储结果的字典
results_original = {}
results_enhanced = {}

# 对每个比例进行攻击并计算鲁棒性
for attack_percentage in attack_percentages:
    # 选择攻击的节点
    nodes_to_attack = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:int(N * attack_percentage)]

    # ... [省略前面的代码]

    # 对每个比例进行攻击并计算鲁棒性
    for attack_percentage in attack_percentages:
        # 选择攻击的节点
        nodes_to_attack = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[
                          :int(N * attack_percentage)]

        # 攻击原始网络
        network_attacked = network.copy()
        network_attacked.remove_nodes_from(nodes_to_attack)
        if len(network_attacked) > 0:
            largest_cc = max(nx.connected_components(network_attacked), key=len)
            largest_cc_size = len(largest_cc)
            efficiency = nx.global_efficiency(network_attacked)
        else:
            largest_cc_size = 0
            efficiency = 0
        results_original[attack_percentage] = (largest_cc_size, efficiency)

        # 攻击增强后的网络
        network_enhanced = network_reset.copy()  # 使用增强后的网络副本
        network_enhanced.remove_nodes_from(nodes_to_attack)
        if len(network_enhanced) > 0:  # 注意这里是网络增强后的网络长度
            largest_cc_enhanced = max(nx.connected_components(network_enhanced), key=len)
            largest_cc_size_enhanced = len(largest_cc_enhanced)
            efficiency_enhanced = nx.global_efficiency(network_enhanced)
        else:
            largest_cc_size_enhanced = 0
            efficiency_enhanced = 0
        results_enhanced[attack_percentage] = (largest_cc_size_enhanced, efficiency_enhanced)

# 输出结果
print("原始网络结果:", results_original)
print("增强后的网络结果:", results_enhanced)
