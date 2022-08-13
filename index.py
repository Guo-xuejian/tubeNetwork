from datetime import datetime

G = {}

for i in range(1, 1000 + 1):
    if i == 1:
        G[1] = {2, 3}
        continue
    elif i == 999:
        G[999] = {997, 1000}
        continue
    if i % 2 == 1:
        G[i] = {i - 2, i + 1, i + 2}
    else:
        G[i] = {i - 1, 1002 - i}


file = open('graphCycles.txt', 'w')


def new_graph(num: int) -> dict:
    """
    new_graph return a graph with given number nodes base on the num parameter
    :rtype: dict
    :param num: The number of the nodes that you want to construct
    :return:
    """
    graph = {}
    for i in range(1, num + 1):
        if i == 1:
            graph[i] = {2, 3}
            continue
        elif i == num - 1:
            graph[i] = {num - 3, num}
            continue
        if i % 2 == 1:
            graph[i] = {i - 2, i + 1, i + 2}
        else:
            graph[i] = {i - 1, num + 2 - i}
    return graph


# G: graph G
# length: length of circles
# path: circles starts with nodes in path
def find_cir_starts_with(G, length, path):
    l, last = len(path), path[-1]
    cnt = 0
    if l == length - 1:  # choose the final node in the circle
        for i in G[last]:
            if (i > path[1]) and (i not in path) and (path[0] in G[i]):
                file.write(f"{path + [i]}\n")
                # print(path + [i])
                cnt += 1
    else:
        for i in G[last]:  # choose internal nodes in the circle
            if (i > path[0]) and (i not in path):
                cnt += find_cir_starts_with(G, length, path + [i])
    return cnt


# G: graph G
# n: number of nodes
# length: length of circles
def find_cir_of_length(G, n, length):
    cnt = 0
    for i in range(1, n - length + 2):  # find all circles starts with i
        cnt += find_cir_starts_with(G, length, [i])
    return cnt


# G: graph G
# n: number of nodes
def find_all_cycles(G, n):
    cnt = 0
    for i in range(48, n + 1):  # find all circles of length i
        cnt += find_cir_of_length(G, n, i)
    return cnt


start = datetime.now()

find_all_cycles(G, 1000)

end = datetime.now()

print(f"time cost: {(end-start).seconds}")
