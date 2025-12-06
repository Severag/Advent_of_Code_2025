def read_file(filename):
    num_parse = lambda line: list(map(int, line))
    
    with open(filename, 'r') as f:
        file_data = f.read().split('\n')

    # Part 1
    row_nums = []
    for raw_line in file_data:
        line = raw_line.strip().split()
        
        if line[0].isdigit():
            row_nums.append(num_parse(line))
        else:
            ops = line
    
    # Part 2
    new_row = []
    alternate = [new_row]
    
    # create numbers by columns
    for col in zip(*file_data[:-1]):
        string = ''.join(col).strip()
        
        if string.isdigit():
            new_row.append(int(string))
        else:  # reached break point
            new_row = []
            alternate.append(new_row)
    
    return row_nums, ops, alternate



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    rows, operations, _ = data
    total = 0
    
    for *numbers,op in zip(*rows, operations):
        total += sum(numbers) if op == '+' else list_prod(numbers)
    
    return total



def list_prod(this_list):
    total = 1
    
    for num in this_list:
        total *= num
    
    return total



def part2(data):
    _, operations, rows = data
    total = 0
    
    for numbers, op in zip(rows, operations):
        total += sum(numbers) if op == '+' else list_prod(numbers)
    
    return total



if __name__ == '__main__':
    puzzles = [['test_case.txt', 4_277_556, 3_263_827],
               ['puzzle_input.txt', ]]
    
    try:
        import AoC_testing
        AoC_testing.run(puzzles, read_file, solve)
    except ModuleNotFoundError:
        for filename, *_ in puzzles:
            print(solve(read_file(filename)))