import re


def read_file(filename):
    regex = r"(\d+)"
    regex_parse = lambda line: list(map(int, re.findall(regex, line)))
    
    with open( filename, 'r') as f:
        data = list(map(regex_parse, f))
    
    return data



def solve(data, do_1=True, do_2=True):
    distances = []
    
    for idx1, point1 in enumerate(data):
        for idx2, point2 in enumerate(data[:idx1]):
            d = dist(point1, point2)
            distances.append([d, idx1, idx2])
    
    distances.sort()
    
    p1 = part1(distances) if do_1 else None
    p2 = part2(data, distances) if do_2 else None
    
    return p1, p2



def dist(p1, p2):
    direcs = [(a - b)**2 for a,b in zip(p1, p2)]
    
    return sum(direcs)**0.5



def part1(distances):
    num_connections = 10 if len(distances) < 1_000 else 1_000
    circuits = []
    
    for _, idx1, idx2 in distances[:num_connections]:
        connection = {idx1, idx2}
        others = []
        for circ in circuits:
            if not circ.isdisjoint(connection):
                connection |= circ
            else:
                others.append(circ)
        
        circuits = others + [connection, ]
    
    circuits.sort(key=len, reverse=True)
    
    total = 1
    for circ in circuits[:3]:
        total *= len(circ)
    
    return total



def part2(data, distances):
    circuits = []
    
    for _, idx1, idx2 in distances:
        connection = {idx1, idx2}
        others = []
        for circ in circuits:
            if not circ.isdisjoint(connection):
                connection |= circ
            else:
                others.append(circ)
        
        circuits = others + [connection, ]
        
        if len(connection) == len(data):  # all nodes are in one circuit
            break
    
    return data[idx1][0] * data[idx2][0]



if __name__ == '__main__':
    puzzles = [['test_case.txt', 40, 25_272],
               ['puzzle_input.txt', ]]
    
    try:
        import AoC_testing
        AoC_testing.run(puzzles, read_file, solve)
    except ModuleNotFoundError:
        for filename, *_ in puzzles:
            print(solve(read_file(filename)))