import math
import random as rand
import numpy as np
from tqdm import tqdm

# パラメータの設定
num = 1000000  # 乱数の生成数
N = 21         # 標本平均の個数
t_dist = 2.086  # t分布の値

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

E, up, down = calc_trust_sec()
print(f"E = {E:.2f}, 信頼区間: [{down:.2f}, {up:.2f}]")
