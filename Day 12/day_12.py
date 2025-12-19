import re


def read_file(filename):
    num_parse = lambda numlist: list(map(int, numlist))
    regex = r"(\d+)"
    regex_parse = lambda line: num_parse(re.findall(regex, line))
    
    all_shapes = []
    square_counts = []
    
    with open( filename, 'r') as f:
        *shape_defs, area_defs = f.read().split('\n\n')
        
    for definition in shape_defs:
        shape = []
        count = 0
        for line in definition.split()[1:]:  # skipping label
            row = [char == '#' for char in line.strip()]
            shape.append(row)
            count += row.count(True)
        
        all_shapes.append(shape)
        square_counts.append(count)
    
    spaces = list(map(regex_parse, area_defs.split('\n')))
    
    return all_shapes, square_counts, spaces



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    all_shapes, square_counts, spaces = data
    total = 0
    
    for length, width, *shape_counts in spaces:
        avail_area = length * width
        
        needed_area = 0
        for footprint, count in zip(square_counts, shape_counts):
            needed_area += footprint * count
        
        if needed_area <= avail_area:
            total += 1
    
    return total



def part2(data):
    return



if __name__ == '__main__':
    puzzles = [['test_case.txt', 2, None],
               ['puzzle_input.txt', ]]  # 592 too low
    
    try:
        import AoC_testing
        AoC_testing.run(puzzles, read_file, solve)
    except ModuleNotFoundError:
        for filename, *_ in puzzles:
            print(solve(read_file(filename)))