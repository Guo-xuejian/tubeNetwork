from tqdm import tqdm
from datetime import datetime
import networkx as nx

start = datetime.now()

G = {}

for i in range(1, 1000 + 1):
    if i == 1:
        G[1] = (2, 3)
        continue
    elif i == 999:
        G[999] = (997, 1000)
        continue
    if i % 2 == 1:
        G[i] = (i - 2, i + 1, i + 2)
    else:
        G[i] = (i - 1, 1002 - i)
H = nx.DiGraph(G)
with open('data1.txt', 'w') as f:
    for one in tqdm(nx.simple_cycles(H)):
        count += 1
        f.write(" ".join(list(map(str, one))) + "\n")
    f.close()


end = datetime.now()

print(f"time cost: {(end-start).seconds}")

