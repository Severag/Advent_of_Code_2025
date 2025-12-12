import itertools, re, scipy
import numpy as np


def read_file(filename):
    regex = r"\[(.+)\] \((.+)\) \{(.+)\}"
    num_parse = lambda string: tuple(map(int, string.split(','))) 
    
    def parse(line):
        lights, buttons, joltages = re.findall(regex, line)[0]
        output = []
        output.append(tuple(char == '#' for char in lights))
        output.append([num_parse(string) for string in buttons.split(') (')])
        output.append(num_parse(joltages))
        
        return output
    
    with open( filename, 'r') as f:
        data = list(map(parse, f))
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    total = 0
    
    for lights, buttons, _ in data:
        total += bfs(lights, buttons)
    
    return total



def bfs(goal, options):
    open_list = [(0, (False,) * len(goal))]
    closed_set = set()
    
    while open_list:
        steps, state = open_list.pop(0)
        
        if state in closed_set:
            continue
        else:
            closed_set.add(state)
        
        if state == goal:  # end condition
            return steps
        
        for opt in options:
            cand = list(state)
            
            for idx in opt:
                cand[idx] = not cand[idx]
            
            cand = tuple(cand)
            if cand not in closed_set:
                open_list.append((steps + 1, cand))
    
    raise ValueError



def part2(data):
    total = 0
    
    for line in data:
        _, buttons, jolts = line
        
        # Find the linear combination of <buttons> that sums to <jolts>
        matrix = np.zeros((len(jolts), len(buttons)), dtype=np.int16)
        for idx, indices in enumerate(buttons):
            matrix[indices, idx] = 1
        
        jarr = np.array([jolts]).T  # joltage array, but jarr is funnier (pirate accent mandatory)
        
        total += solve_system(matrix, jarr)
    
    return total



def solve_system(matrix, jarr):  # system of equations, that is
    num_joltages, num_buttons = matrix.shape
    
    # start with Gaussian elimination
    gauss = np.hstack([matrix, jarr])
    
    upper = scipy.linalg.lu(gauss, permute_l=True)[1]
    upper[np.abs(upper) < 1e-10] = 0
    upper = back_substitution(upper)
    
    # that should reduce the problem space, so we'll try brute forcing the rest of the way there
    # i.e. the above should've narrowed it down to a handful of unconstrained variables
    # once we set the value of those, the rest will fall into place
    undefined = []
    for c_idx, col in enumerate(upper.T[:-1]):  # for every button's column
        # if this column has a single 1 with everything else as only 0s, then its button presses
        # are either solved or dependent on an undefined value
        # columns that don't match that criteria are undefined
        if np.count_nonzero(col) == 1 and col.sum() == 1:
            pass  # good to move on
        else:
            undefined.append(c_idx)
    
    # <template> expands <upper> (if needed) so that we can try to make a full-rank matrix
    template = upper.copy()
    for r_idx in undefined:
        # add row of zeros to correpsond to this button's column
        # provided there isn't one there already
        if r_idx >= len(template) or template[r_idx].any():
            template = np.insert(template, r_idx, 0, axis=0)
    
    # figure out how many different combinations we need to try
    param_space = []
    for idx in undefined:
        vector = matrix[:, idx:idx+1]
        mask = vector > 0
        
        limit = int(np.min(jarr[mask] / vector[mask]))
        
        param_space.append(range(limit + 1))
    
    # try all those options out
    best_score = np.inf
    for new_vals in itertools.product(*param_space):
        new_matrix = template.copy()
        
        for d_idx, new in zip(undefined, new_vals):
            new_matrix[d_idx, d_idx] = 1
            new_matrix[d_idx,    -1] = new
        
        new_matrix = back_substitution(new_matrix)
        
        # assert we reduced it correctly
        assert(np.all(new_matrix[:num_buttons, :num_buttons] == np.eye(num_buttons)))
        
        # round() b/c we can only accept integer number presses
        x_cand = np.round(new_matrix[:num_buttons, -1:], 0)
        
        if np.all(x_cand >= 0) and np.all(matrix @ x_cand == jarr):
            best_score = min(best_score, x_cand.sum())
    
    return int(best_score)



def back_substitution(upper):
    # Warning: modifies upper
    # upper is clear of the lower left triangle, so now we work from bottom to top
    # simplifying the upper right triangle
    for r_idx in reversed(range(len(upper))):
        curr_row = upper[r_idx]
        
        # get index of first nonzero value in row (minus last column, which is the "answer" column)
        nonzeros = np.where(curr_row[:-1] != 0)[0]
        if nonzeros.size > 0:
            c_idx = nonzeros[0]
        else:
            continue  # skip degenerate cases
        
        val = curr_row[c_idx]
        
        curr_row /= val  # normalize row leading number is 1
        curr_row[np.abs(curr_row) < 1e-10] = 0  # mop up nearly-0 numbers
        
        for r2_idx, val in enumerate(upper[:, c_idx]):
            if r2_idx != r_idx:
                upper[r2_idx] -= curr_row * val
    
    # rearrange rows which might not be in order after all this
    # specifically, we may have some rows with leading ones behind
    # the leading ones of subsequent rows
    rows, cols = np.where(upper == 1)
    _, indices = np.unique(rows, return_index=True)
    rows_with_ones = rows[indices]
    cols_with_ones = cols[indices]
    new_order = np.argsort(cols_with_ones)
    # move rows with leading ones in more left-columns higher
    upper[(rows_with_ones,)] = upper[(rows_with_ones[new_order],)]
    
    return upper



if __name__ == '__main__':
    puzzles = [['test_case.txt', 7, 33],
               ['puzzle_input.txt', ]]
    
    try:
        import AoC_testing
        AoC_testing.run(puzzles, read_file, solve)
    except ModuleNotFoundError:
        for filename, *_ in puzzles:
            print(solve(read_file(filename)))