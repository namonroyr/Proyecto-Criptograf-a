import numpy as np

def generate_permutation():
    return np.random.permutation([i for i in range(10)])

for i in range(5):
    print(generate_permutation())