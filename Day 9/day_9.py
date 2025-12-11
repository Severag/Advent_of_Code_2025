from itertools import combinations as combo


def read_file(filename):
    num_parse = lambda line: tuple(map(int, line.split(',')))
    
    with open(filename, 'r') as f:
        data = [num_parse(line.strip()) for line in f]
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    return max(get_easy_area(pair) for pair in combo(data, 2))



def get_easy_area(point_pair):
    sides = [abs(x1 - x2) + 1 for x1, x2 in zip(*point_pair)]
    
    return sides[0] * sides[1]



def part2(data):
    simple_areas = []
    
    for point1, point2 in combo(data, 2):
        area = get_easy_area([point1, point2])
        simple_areas.append((area, point1, point2))
    
    simple_areas.sort(reverse=True)
    
    # start with the largest area and continue till we find one that works
    for area, point1, point2 in simple_areas:
        point3 = (point1[0], point2[1])
        point4 = (point2[0], point1[1])
        
        # Verify the new corners are in the shape
        # and that the rectangle's perimeter line across never leaves it
        if are_valid_corners([point3, point4], [point1, point2], data):
            return area



def are_valid_corners(new, old, data):
    for new_corner in new:
        # if both new_corners are inside
        if new_corner in data or is_inside(new_corner, data):
            # if both lines from <new_corner> to the old corners remain
            # in the shape
            for old_corner in old:
                if have_line_crossings(new_corner, old_corner, data):
                    return False
        else:
            return False
    
    return True




def is_inside(point, data):
    winding = 0
    
    for vert_a, vert_b in zip(data, data[1:] + data[:1]):
        ascending = vert_a[1] <= vert_b[1]
        
        if ascending:
            is_relevant = vert_a[1] <= point[1] < vert_b[1]
        else:
            is_relevant = vert_b[1] <= point[1] < vert_a[1]
        
        if is_relevant:
            ab_x = vert_b[0] - vert_a[0]
            ab_y = vert_b[1] - vert_a[1]
            
            ap_x = point[0] - vert_a[0]
            ap_y = point[1] - vert_a[1]
            
            # the z-component of the cross vector 
            # (x & y components are 0, b/c factors' z's are 0)
            cross_product = (ab_x * ap_y) - (ab_y * ap_x)
            
            if ascending and cross_product > 0:
                winding += 1
            elif not ascending and cross_product < 0:
                winding -= 1
    
    return winding != 0



def have_line_crossings(start, stop, data):
    get_range = lambda a,b: range(min(a, b) + 1, max(a,b))
    is_horizontal = lambda point1, point2: point1[1] == point2[1] 
    
    h_mode = is_horizontal(start, stop)
    if h_mode:
        range_x = get_range(start[0], stop[0])
        const_y = start[1]
    else:
        const_x = start[0]
        range_y = get_range(start[1], stop[1])
    
    crossings = 0
    
    for vert_a, vert_b in zip(data, data[1:] + data[:1]):
        if h_mode:
            if not is_horizontal(vert_a, vert_b):
                # Our horizontal line is crossing this other vertical line
                other_x = vert_a[0]
                xs_overlap = other_x in range_x
                
                min_y, max_y = sorted((vert_a[1], vert_b[1]))
                ys_overlap = min_y <= const_y <= max_y
                
                if xs_overlap and ys_overlap:
                    crossings += 1
        else:
            if is_horizontal(vert_a, vert_b):
                # Our vertical line is crossing this other horizontal line
                min_x, max_x = sorted((vert_a[0], vert_b[0]))
                xs_overlap = min_x <= const_x <= max_x
                
                other_y = vert_a[1]
                ys_overlap = other_y in range_y
                
                if xs_overlap and ys_overlap:
                    crossings += 1
        
        if crossings > 1:
            return True
    
    return False



if __name__ == '__main__':
    puzzles = [['test_case.txt', 50, 24],
               ['puzzle_input.txt', ]]
    
    try:
        import AoC_testing
        AoC_testing.run(puzzles, read_file, solve)
    except ModuleNotFoundError:
        for filename, *_ in puzzles:
            print(solve(read_file(filename)))