import numpy as np
import matplotlib.pyplot as plt

# 定数設定
arrival_rate = 0.54  # 到着率 λ
service_rate = 1.0  # サービス率 μ
target_rejection_rate = 0.001  # 目標棄却率
K_min, K_max = 1, 20  # システム容量 K の範囲

# 性能指標を計算する関数
def compute_mm1k_metrics(arrival_rate, service_rate, K):
    rho = arrival_rate / service_rate  # 利用率
    p0 = (1 - rho) / (1 - rho ** (K + 1))  # 空状態の確率
    pk = p0 * rho ** K  # 棄却率
    L = rho * (1 - (K + 1) * rho ** K + K * rho ** (K + 1)) * p0 / (1 - rho) ** 2  # 平均システム内客数
    Lq = L - rho * (1 - pk) # 平均待ち行列内客数
    utilization = rho  # サーバ利用率
    print(K, ': pk=', pk)
    return pk, L, Lq, utilization

# システム容量ごとの性能指標を計算
K_values = np.arange(K_min, K_max + 1)
rejection_rates = []
avg_customers_in_system = []
avg_customers_in_queue = []
utilization_rates = []

for K in K_values:
    pk, L, Lq, utilization = compute_mm1k_metrics(arrival_rate, service_rate, K)
    rejection_rates.append(pk)
    avg_customers_in_system.append(L)
    avg_customers_in_queue.append(Lq)
    utilization_rates.append(utilization)

# グラフの作成と保存

# 棄却率
plt.figure()
plt.plot(K_values, rejection_rates, marker='o', label="Rejection Rate")
plt.axhline(target_rejection_rate, color='red', linestyle='--', label="Target Rejection Rate")
plt.xlabel("System Capacity (K)")
plt.ylabel("Rejection Rate")
plt.title("Rejection Rate vs System Capacity")
plt.legend()
plt.grid()
plt.savefig("rejection_rate_vs_capacity.png")

# 平均システム内客数
plt.figure()
plt.plot(K_values, avg_customers_in_system, marker='o', label="Avg Customers in System")
plt.xlabel("System Capacity (K)")
plt.ylabel("Avg Customers in System")
plt.title("Avg Customers in System vs System Capacity")
plt.legend()
plt.grid()
plt.savefig("avg_customers_in_system_vs_capacity.png")

# 平均待ち行列内客数
plt.figure()
plt.plot(K_values, avg_customers_in_queue, marker='o', label="Avg Customers in Queue")
plt.xlabel("System Capacity (K)")
plt.ylabel("Avg Customers in Queue")
plt.title("Avg Customers in Queue vs System Capacity")
plt.legend()
plt.grid()
plt.savefig("avg_customers_in_queue_vs_capacity.png")

# サーバ利用率
plt.figure()
plt.plot(K_values, utilization_rates, marker='o', label="Utilization Rate")
plt.xlabel("System Capacity (K)")
plt.ylabel("Utilization Rate")
plt.title("Utilization Rate vs System Capacity")
plt.legend()
plt.grid()
plt.savefig("utilization_rate_vs_capacity.png")

plt.show()
