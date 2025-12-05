def read_file(filename):
    ranges = []
    items = []
    in_items = False
    
    with open( filename, 'r') as f:
        for raw_line in f:
            line = raw_line.strip().split('-')
            if in_items:
                items.append(int(line[0]))
            elif len(line) < 2:
                in_items = True
            else:
                nums = list(map(int, line))
                ranges.append(range(nums[0], nums[1] + 1))
    
    return ranges, items




def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    ranges, items = data
    total = 0
    
    for ingred in items:
        fresh = False
        
        for rng in ranges:
            if ingred in rng:
                fresh = True
                break
        
        if fresh:
            total += 1
    
    return total



def part2(data):
    ranges, items = data
    
    merged_one = True
    
    while merged_one:
        merged_one = False
        
        for whole_list_index in range(len(ranges)):
            this = ranges.pop(0)
            
            for idx,other in enumerate(ranges):
                if this.stop in other or this.start in other:
                    new_start = min(this.start, other.start)
                    new_stop = max(this.stop, other.stop)
                    
                    ranges[idx] = range(new_start, new_stop)
                    
                    merged_one = True
                    break
            else:  # if no breaks were executed
                ranges.append(this)
    
    total = sum(len(rng) for rng in ranges)
    
    return total



if __name__ == '__main__':
    puzzles = [['test_case.txt', 3, 14],
               ['puzzle_input.txt', ]]
    
    try:
        import AoC_testing
        AoC_testing.run(puzzles, read_file, solve)
    except ModuleNotFoundError:
        for filename, *_ in puzzles:
            print(solve(read_file(filename)))