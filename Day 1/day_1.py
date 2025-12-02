def read_file(filename):
    def line_parse(line_raw):
        line = line_raw.strip()
        if line[0] == 'R':
            coeff = 1
        elif line[0] == 'L':
            coeff = -1
        else:
            raise ValueError(f"Invalid letter for the line begining: {line[0]}")
        
        return coeff * int(line[1:])
    
    with open( filename, 'r') as f:
        data = list(map(line_parse, f))
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    dial = 50
    count_0 = 0
    
    for turn in data:
        dial = (dial + turn) % 100
        
        if dial == 0:
            count_0 += 1
    
    return count_0



def part2(data):
    dial = 50
    count_0 = 0
    
    for turn in data:
        quotient, new_dial = divmod(dial + turn, 100)
        
        delta_count = abs(quotient)
        
        if turn < 0:
            if dial == 0:         # the quotient increases by 1 if we started at 
                delta_count -= 1  # zero and went negative, but we already 
                                  # counted that zero in the previous step
            
            if new_dial == 0:     # quotient won't increase by 1 if we decreased
                delta_count += 1  # our way to zero, but the count should go up 
                                  # anyway
        
        dial = new_dial
        count_0 += delta_count
    
    return count_0



if __name__ == '__main__':
    puzzles = [['test_case.txt', 3, 6],
               ['puzzle_input.txt', ]]
    
    try:
        import AoC_testing
        AoC_testing.run(puzzles, read_file, solve)
    except ModuleNotFoundError:
        for filename, *_ in puzzles:
            print(solve(read_file(filename)))