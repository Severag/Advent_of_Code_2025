import re


def read_file(filename):
    regex = r"(\d+)"
    regex_parse = lambda line: list(map(int, re.findall(regex, line)))
    
    with open( filename, 'r') as f:
        data = list(map(int, re.findall(regex, next(f))))
    
    ranges = [range(low, high+1) for low,high in zip(data[::2], data[1::2])]
    
    return ranges



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    total = 0
    
    for rng in data:
        for val in rng:
            string = str(val)
            
            idx = len(string) // 2
            
            if string[:idx] == string[idx:]:
                total += val
    
    return total



def part2(data):
    total = 0
    
    for rng in data:
        for val in rng:
            string = str(val)
            
            for seq_len in range(1, len(string) // 2 + 1):
                cand = string[:seq_len]
                # <string> consists entirely of multiple <cand>'s repeated
                if len(string.replace(cand, "")) == 0:
                    total += val
                    break
    
    return total



if __name__ == '__main__':
    puzzles = [['test_case.txt', 1_227_775_554, 4_174_379_265],
               ['puzzle_input.txt', ]]
    
    try:
        import AoC_testing
        AoC_testing.run(puzzles, read_file, solve)
    except ModuleNotFoundError:
        for filename, *_ in puzzles:
            print(solve(read_file(filename)))