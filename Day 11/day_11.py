import collections
import numpy as np


def read_file(filename):
    def parse(line):
        key, remainder = line.strip().split(': ')
        
        return key, remainder.split()
    
    with open( filename, 'r') as f:
        data = dict(map(parse, f))
    
    data['out'] = []
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    start = 'you'
    end = 'out'
    
    open_list = [[start]]
    completed_count = 0
    
    while open_list:
        path = open_list.pop()
        curr = path[-1]
        
        if curr == end:
            completed_count += 1
        elif curr in data:
            for cand in data[curr]:
                open_list.append(path + [cand])
    
    return completed_count



def part2(data):
    total = 0
    topo_order = topo_sort(data, 'svr')
    rev_graph = reverse_graph(data)
    
    all_routes = ['svr fft dac out'.split(),
                  'svr dac fft out'.split()]
    
    for route in all_routes:
        num_paths = 1
        for start,end in zip(route[:-1], route[1:]):
            if end == 'fft':
                avoid = 'dac'
            elif end == 'dac':
                avoid = 'fft'
            else:
                avoid = None
            num_paths *= count_paths(rev_graph, topo_order, start, end, avoid)
        
        total += num_paths
    
    return total



def reverse_graph(graph):
    rev = collections.defaultdict(list)
    
    for key, items in graph.items():
        for val in items:
            rev[val].append(key)
    
    return rev



def topo_sort(data, start):
    # modified from https://stackoverflow.com/questions/47192626/deceptively-simple-implementation-of-topological-sorting-in-python
    open_list = [start]
    stack = []
    order = []
    visited = set()
    
    while open_list:
        curr = open_list.pop()
        
        if curr in visited:
            continue
        visited.add(curr)
        open_list.extend(data[curr])
        
        # traverse back through unexplored branches
        while stack and curr not in data[stack[-1]]:
            order.append(stack.pop())
        
        stack.append(curr)
    
    return stack + order[::-1]



def count_paths(rev_graph, topo, start, end, avoid):
    path_counts = collections.defaultdict(int)
    path_counts[start] = 1
    
    begin = topo.index(start) + 1
    
    for node in topo[begin:]:
        if node == avoid:
            continue
        num_paths = 0
        for parent in rev_graph[node]:
            num_paths += path_counts[parent]
        
        path_counts[node] = num_paths
        
        if node == end:
            break
    
    return path_counts[end]



if __name__ == '__main__':
    puzzles = [['test_case.txt', 5, None],
               ['test_case_2.txt', None, 2],
               ['puzzle_input.txt', ]]
    
    try:
        import AoC_testing
        AoC_testing.run(puzzles, read_file, solve)
    except ModuleNotFoundError:
        for filename, *_ in puzzles:
            print(solve(read_file(filename)))