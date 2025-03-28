import math
import random as rand
import numpy as np
from tqdm import tqdm

# パラメータの設定
num = 1000000  # 乱数の生成数
N = 21         # 標本平均の個数
t_dist = 2.086  # t分布の値
trust_N = 100   # 信頼区間の数
mu = 40         # 母平均
X = [10, 25, 50, 75, 100]  # 評価する信頼区間の数

# 乱数の標本平均を計算する関数
def exp_ave():
    exp_dist = []
    for _ in range(num):
        u = rand.random()
        f_inv = -40 * math.log(1 - u)
        exp_dist.append(f_inv)
    return np.mean(exp_dist)

# 信頼区間を計算する関数
def calc_trust_sec():
    sample_means = [exp_ave() for _ in range(N)]
    E = np.mean(sample_means)               # 標本平均
    s2 = np.var(sample_means, ddof=1)       # 不偏分散
    margin_of_error = t_dist * math.sqrt(s2 / N)  # 信頼区間の誤差
    up = E + margin_of_error
    down = E - margin_of_error
    return E, up, down

# 信頼区間を100個計算し、母平均が区間に含まれるか判定
Y = 0  # 母平均が信頼区間に含まれる回数
result = []

print("信頼区間を計算中...\n")

for i in tqdm(range(1, trust_N + 1), desc="進捗"):
    E, up, down = calc_trust_sec()
    if down <= mu <= up:
        Y += 1
    if i in X:
        result.append(Y / i)
        print(f"進捗 X = {i}: 信頼区間に母平均を含む割合 Y/X = {Y / i:.3f}")
    if i == 50:  # 任意の進捗点で詳細を表示
        print(f"E = {E:.2f}, 信頼区間: [{down:.2f}, {up:.2f}]")

print("\n計算が完了しました。\n")

# 結果の表示
print("Xにおける母平均が信頼区間に含まれる割合 (Y/X):")
for x_val, yx_val in zip(X, result):
    print(f"X = {x_val}: Y/X = {yx_val:.3f}")
