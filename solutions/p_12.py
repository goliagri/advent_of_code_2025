#https://adventofcode.com/2025/day/12
INPUT_FILENAME = "inputs/input_12.txt"
import numpy as np

def can_fit_under_tree(shapes, shape_counts, grid_shape) -> bool:
    '''
    shapes: dict int -> shape mat
    shape_counts: list of ints, shape_count[i] = # of shapes[i] under tree
    grid_shape = (x,y) specifying rows and cols in tree grid
    return: True iff shapes can be fit under tree grid
    '''
    print('--- Solving Tree')
    if not basic_feasability(shapes, shape_counts, grid_shape):
        print('Trivially Infeasible')
        return False
    if greedy_packing(shapes, shape_counts, grid_shape):
        print('solved by greedy packing')
        return True
    else:
        print('unsolved by greedy packing')
        return False

def can_fit(shape: np.ndarray , grid_seg :np.ndarray) -> bool:
    return not np.sum(shape[grid_seg != 0])

def get_all_orientations(shape: np.ndarray) -> list[np.ndarray]:
    res = []
    is_included = set() #used to make sure elements of res are unique

    for s in [shape, np.flip(shape.copy(), axis=0)]:
        for _ in range(4):
            tup_s = tuple(s.flatten()) #hashable representation of matrix
            if not tup_s in is_included:
                is_included.add(tup_s)
                res.append(s.copy())
            s = s.T
            s = np.flip(s, axis=0)

    return res

def basic_feasability(shapes: list[np.ndarray], shape_counts: list[int], grid_shape: list[int]):
    #quickly checks cheap cases where is unsolvable
    s_val_list = [shapes[i] for i in range(len(shapes))]
    shape_sizes = [sum(i>0 for i in list(s.flatten())) for s in s_val_list]
    total_size = sum(count*size for count,size in zip(shape_counts, shape_sizes))
    total_possible_size = grid_shape[0] * grid_shape[1]
    return total_size <= total_possible_size
    
#----------------------------------------------------------------
#                      Packing Algorithms!
#----------------------------------------------------------------
def greedy_packing(shapes, shape_counts, grid_shape):
    #we iterate from top left through grid, and whenever we can place a shape we do so, tiebreaking based on count left
    #seems like greedy packing is sufficient to solve every actual tree.
    grid = np.zeros(grid_shape)
    for i in range(grid_shape[0] - 2):
        for j in range(grid_shape[1] - 2):
            subgrid = grid[i:i+3, j:j+3]
            shape_check_order = list(np.argsort(shape_counts))
            #print('!')
            #print(shape_counts)
            #print(shape_check_order)
            shape_check_order.reverse()
            shape_check_order = shape_check_order[:sum(i>0 for i in shape_counts)] #make sure we aren't placing used up shapes
            if not shape_check_order: #stop early if done
                break 
            #print(shape_check_order)
            found_fit = False
            for shape_id in shape_check_order:
                shape = shapes[shape_id] * (shape_id+1) #number to keep track of what tiles are actually being used for vis and debugging
                shape_rots = get_all_orientations(shape)
                shape_rots = shape_rots 
                for shape_rot in shape_rots:
                    if can_fit(shape_rot, subgrid):
                        #place shape in grid
                        shape_counts[shape_id] -= 1
                        grid[i:i+3, j:j+3] += shape_rot
                        found_fit = True
                        break
                if found_fit:
                    break
    print(shape_counts)
    return sum(i>0 for i in shape_counts) == 0


def get_data():
    with open(INPUT_FILENAME) as f:
        lines = [a.strip() for a in f.readlines()]
    segments = []
    cur_seg = []
    for line in lines:
        if line == '':
            segments.append(cur_seg)
            cur_seg  = []
        else:
            cur_seg.append(line)
    segments.append(cur_seg)
    tree_specs = []
    shapes = {}
    for segment in segments:
        if len(segment) > 1 and segment[1][0] == '.' or segment[1][0] == '#': #is a shape definition
            id = int(segment[0][:-1]) #first line of shape should be <id>:
            shape_diagram = segment[1:]
            shape_mat = np.zeros((len(shape_diagram), len(shape_diagram[0])))
            #print(shape_diagram)
            for i in range(len(shape_diagram)):
                for j in range(len(shape_diagram[0])):
                    if shape_diagram[i][j] == '#':
                        shape_mat[i,j] = 1
            shapes[id] = shape_mat

        else: # is tree specs
            for tree_data in segment:
                grid_shape, shape_counts = tree_data.split(': ')
                grid_shape = [int(a) for a in grid_shape.split('x')]
                shape_counts = [int(a) for a in shape_counts.split(' ')]
                assert len(grid_shape) == 2
                tree_specs.append((grid_shape, shape_counts))
    return shapes, tree_specs


def count_num_trees_fitting_presents(shapes, tree_specs) -> int: 
    res = 0
    for grid_shape, shape_counts in tree_specs:
        if can_fit_under_tree(shapes, shape_counts, grid_shape):
            res += 1
    
    return res


def main():
    shapes, tree_specs = get_data()
    p1_sol = count_num_trees_fitting_presents(shapes, tree_specs)

    print('number of trees which can fit presents {}'.format(p1_sol))



if __name__ == '__main__':
    main()