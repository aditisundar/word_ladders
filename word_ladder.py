from timeit import default_timer
import heapq

class Node():
    def __init__(self, word):
        self.name = word
        self.g = 0
        self.h = 0
        self.f = self.g + self.h
        self.parent = None
    def __repr__(self):
        return self.name
    def __lt__(self, other):
        return self.f < other.f
        print("comparing")
    def __eq__(self, other):
        return self.name == other.name
        print("equals")
    def neighbors(self, goal, graph):
        n = []
        adjacencies = graph.get(self.name, [])
        for a in adjacencies:
            node = Node(a)
            node.parent = self
            node.g = self.g + 1
            node.h = heuristic(self.name, goal)
            node.f = node.g + node.h
            n.append(node)
        return n


def make_graph(wordFile):
    d = {}
    g = {}
    dict1 = open(wordFile,'r')
    for line in dict1:
        keyWord = line[:-1]
        g[keyWord] = []

    wfile = open(wordFile,'r')

    for line in wfile:
        word = line[:-1]
        for i in range(len(word)):
            bucket = word[:i] + '_' + word[i+1:]
            if bucket in d:
                d[bucket].append(word)
            else:
                d[bucket] = [word]

    for bucket in d.keys():
        for word1 in d[bucket]:
            for word2 in d[bucket]:
                if word1 != word2:
                    g[word1].append(word2)
    return g
def bfs(graph, start, end):
    count = 0
    queue = []
    queue.append([start])
    while queue:
        path = queue.pop(0)
        count += 1
        node = path[-1]
        if node == end:
            print("nodes popped: ", count)
            return path
        adjacencies = graph.get(node, [])
        for a in adjacencies:
            new_path = list(path)
            new_path.append(a)
            queue.append(new_path)
def heuristic(start, end):
    count = 0
    for a in start:
        for b in end:
            if a is not b:
                count += 1
    return count
def min_index(li):
    min_f = min(node.f for node in li)
    for i in range(len(li)):
        if li[i].f == min_f:
            return i
def bidirectional(graph, start, end):
        queue = []
        backqueue = []
        queue.append([start])
        backqueue.append([end])

        while queue:
            path = queue.pop(0)
            backpath = backqueue.pop(0)
            node = path[-1]
            backnode = backpath[-1]
            if node == backnode:
                return path[0:-1] + backpath[::-1]
            for adjacent in graph.get(node, []):
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)
            for adjacent in graph.get(backnode, []):
                new_backpath = list(backpath)
                new_backpath.append(adjacent)
                backqueue.append(new_backpath)

def astarq(graph, start, end):
    op = []
    s = Node(start)
    heapq.heappush(op, s)
    cl = []
    count = 0
    while op:
        heapq.heapify(op)
        q = heapq.heappop(op)
        count+=1
        #print(q)
        if q.name == end:
            path = []
            while q.parent:
                path.append(q.name)
                q = q.parent
            path.append(q.name)
            print("nodes popped: ", count)
            return path
        cl.append(q)
        for node in q.neighbors(end, graph):
            if node.name == end:
                path = []
                while(node.parent):
                    path.append(node.name)
                    node = node.parent
                path.append(node.name)
                print("nodes popped: ", count)
                return path[::-1]
            if node not in cl:
                g = q.g+1
                if(node.g > g):
                    node.g = g
                    node.parent = q
                heapq.heappush(op, node)


g = make_graph("words.txt")

print()

start = input("starting word: ")
end = input("target word: ")

print()

start2 = default_timer()
a_path = astarq(g,start,end)
duration = default_timer() - start2
if(a_path is None):
    print("a*: no path found.")
else:
    print("a*: ", a_path)
    print("time: ", duration, " steps: ", len(a_path))

print()

start1 = default_timer()
b_path = bfs(g, start, end)#bfs(g,start,end)
duration = default_timer() - start1
if(b_path is None):
    print("bfs: no path found.")
else:
    print("bfs: ", b_path)
    print("bfs time: ", duration, " steps: ", len(b_path))

print()