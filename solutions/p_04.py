#https://adventofcode.com/2025/day/4
INPUT_FILENAME = "inputs/input_04.txt"

import numpy as np

def count_and_mark_forklift_accessible_rolls(data):
    max_for_accessibility = 4
    grid_depth = len(data)
    grid_width = len(data[0])

    adj_count_mat = np.zeros((grid_depth, grid_width))
    is_roll_mat = np.zeros((grid_depth, grid_width))

    for i in range(grid_depth):
        for j in range(grid_width):

            cur_char = data[i][j]
            if cur_char == ".":
                continue
            elif cur_char == "@":
                is_roll_mat[i,j] = 1
                adj_i_lowerbound = max(0,i-1)
                adj_i_upperbound = min(grid_depth-1, i+1)
                adj_j_lowerbound = max(0,j-1)
                adj_j_upperbound = min(grid_width-1, j+1)
                adj_count_mat[adj_i_lowerbound:adj_i_upperbound+1,adj_j_lowerbound:adj_j_upperbound+1] += 1
                adj_count_mat[i,j] -= 1
            else:
                raise Exception("Unknown Character {}".format(cur_char))

    removable = np.where(adj_count_mat < 4, is_roll_mat, 0)
    return int(np.sum(removable)), removable

def count_iteratively_removed_rolls(data):
    grid_depth = len(data)
    grid_width = len(data[0])

    res = 0
    while True:
        last_count, last_removables = count_and_mark_forklift_accessible_rolls(data)
        res += last_count
        if last_count == 0:
            break
        for i in range(grid_depth):
            for j in range(grid_width):
                if last_removables[i,j]:
                    data[i] = data[i][:j] + '.' + data[i][j+1:] 
    
    return res

def get_data():
    with open(INPUT_FILENAME) as f:
        data = f.readlines()
        data = [s.strip() for s in data]
    return data


def main():
    data = get_data()
    p1_sol, _ = count_and_mark_forklift_accessible_rolls(data)
    p2_sol = count_iteratively_removed_rolls(data)
    print('num accessible roles by forklift: {}'.format(p1_sol))
    print('num accessible rolls by iterative removing: {}'.format(p2_sol))

    


if __name__ == "__main__":
    main()