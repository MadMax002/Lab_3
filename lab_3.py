import heapq

class Node:
    def __init__(self, path, cost, bound):
        self.path = path
        self.cost = cost
        self.bound = bound

    def __lt__(self, other):
        return self.bound < other.bound

class Heap:
    def __init__(self):
        self.nodes = []
        self.count = 0

    def push(self, node):
        heapq.heappush(self.nodes, node)
        self.count += 1

    def pop(self):
        self.count -= 1
        return heapq.heappop(self.nodes)

def tsp_branch_and_bound(distances):
    n = len(distances)
    best_path = None
    best_cost = float('inf')
    initial_node = Node([0], 0, bound(distances, [0]))
    heap = Heap()
    heap.push(initial_node)

    while heap.count > 0:
        node = heap.pop()

        if node.bound >= best_cost:
            continue

        if len(node.path) == n:
            node.path.append(0)
            cost = cost_of_path(distances, node.path)
            if cost < best_cost:
                best_cost = cost
                best_path = node.path[:-1]
        else:
            last = node.path[-1]
            for i in range(n):
                if i not in node.path:
                    path = node.path + [i]
                    cost = node.cost + distances[last][i]
                    bound_value = bound(distances, path)
                    child_node = Node(path, cost, bound_value)
                    if child_node.bound < best_cost:
                        heap.push(child_node)

    return best_path, best_cost

def cost_of_path(distances, path):
    cost = 0
    for i in range(len(path) - 1):
        cost += distances[path[i]][path[i+1]]
    return cost

def bound(distances, path):
    current = path[-1]
    unvisited = [i for i in range(len(distances)) if i not in path]
    bound = 0
    for i in range(len(path)-1):
        bound += distances[path[i]][path[i+1]]
    if len(unvisited) > 0:
        bound += min([distances[current][j] for j in unvisited])
        bound += min([distances[j][path[0]] for j in unvisited])
    return bound

# Зчитування даних з файлу
with open('data.txt', 'r') as f:
    lines = f.readlines()
    distances = []
    for line in lines:
        row = [int(x) for x in line.strip().split()]
        distances.append(row)

# Виклик функції та вивід результатів
best_path, best_cost = tsp_branch_and_bound(distances)
print('Best solution:', best_path)
print('Best distance:', best_cost)
