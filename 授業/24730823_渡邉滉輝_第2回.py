import numpy as np

# 指数分布乱数生成 (逆関数法)
def generate_exponential_random(mean):
    u = np.random.uniform(0, 1)
    return -mean * np.log(1 - u)

# シミュレーションパラメータ
A = 10  # 1つ目のノードのバッファサイズ
B = 10  # 2つ目のノードのバッファサイズ
lambda_arrival = 0.5  # 平均到着率 (到着間隔の平均 = 1/lambda)
mean_service_time = 1.0  # サービス時間の平均
propagation_delay = 0.5  # 伝播遅延時間
num_packets = 1000000  # シミュレーション終了条件
num_simulations = 21  # シミュレーションの繰り返し回数

# 性能評価結果を格納
results = {
    "reject_rate": [],
    "avg_system_packets": [],
    "avg_system_delay": [],
    "avg_queue_delay": [],
}

# シミュレーション実行
for sim in range(num_simulations):
    time = 0
    node1_buffer = []
    node2_buffer = []
    node1_rejected = 0
    node2_rejected = 0
    total_packets = 0
    system_time = []  # パケットのシステム内遅延を記録
    queue_time = []  # パケットの待ち行列遅延を記録

    while total_packets < num_packets:
        # 次のパケット到着時間
        interarrival_time = generate_exponential_random(1 / lambda_arrival)
        time += interarrival_time

        # ノード1のサービス処理
        if node1_buffer and time >= node1_buffer[0][1]:
            node2_arrival_time = time + propagation_delay
            if len(node2_buffer) < B:
                service_time = generate_exponential_random(mean_service_time)
                node2_buffer.append((node2_arrival_time, node2_arrival_time + service_time))
            else:
                node2_rejected += 1
            node1_buffer.pop(0)

        # ノード2のサービス処理
        if node2_buffer and time >= node2_buffer[0][1]:
            system_time.append(node2_buffer[0][1] - node2_buffer[0][0])
            queue_time.append(node2_buffer[0][0] - (time - propagation_delay))
            node2_buffer.pop(0)

        # ノード1へのパケット到着
        if len(node1_buffer) < A:
            service_time = generate_exponential_random(mean_service_time)
            node1_buffer.append((time, time + service_time))
        else:
            node1_rejected += 1

        total_packets += 1

    # 結果を保存
    total_rejected = node1_rejected + node2_rejected
    reject_rate = total_rejected / num_packets
    avg_system_packets = (len(node1_buffer) + len(node2_buffer)) / 2
    avg_system_delay = np.mean(system_time) if system_time else 0
    avg_queue_delay = np.mean(queue_time) if queue_time else 0

    results["reject_rate"].append(reject_rate)
    results["avg_system_packets"].append(avg_system_packets)
    results["avg_system_delay"].append(avg_system_delay)
    results["avg_queue_delay"].append(avg_queue_delay)

# 平均と信頼区間の計算
def calculate_statistics(data):
    mean = np.mean(data)
    ci = 2.086 * np.std(data) / np.sqrt(len(data))  # 95%信頼区間
    return mean, ci

for metric in results:
    mean, ci = calculate_statistics(results[metric])
    print(f"{metric}: Mean = {mean:.6f}, 95% CI = ±{ci:.6f}")
