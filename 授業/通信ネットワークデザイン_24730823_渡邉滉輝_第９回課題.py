import math
import random as rand
import numpy as np
import matplotlib.pyplot as plt

num = 1000000
max = 50
min = 30
uni_dist = []
exp_dist = []
dist_range = range(min, max)

for i in range(num):
    u = rand.random()
    f_inv = (max - min) * u + min
    uni_dist.append(math.floor(f_inv))
    f_inv = - 40 * math.log(1 - u)
    exp_dist.append(math.floor(f_inv))

plt.figure(figsize=(12, 6))

plt.hist(uni_dist, bins=100, color='skyblue', edgecolor='black')
plt.title("Uniform Distribution")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.xticks([i for i in range(min, max)])
plt.tight_layout()
plt.show()

plt.hist(exp_dist, bins=100, color='salmon', edgecolor='black')
plt.title("Exponential Distribution")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()




