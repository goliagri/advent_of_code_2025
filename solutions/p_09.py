#https://adventofcode.com/2025/day/9
INPUT_FILENAME = "inputs/input_09.txt"


def largest_rectangle_area(data):
    max_area = 0
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            cur_area = (abs(data[i][0]-data[j][0])+1) *((abs(data[i][1]-data[j][1]))+1)
            max_area = max(cur_area, max_area)
    return max_area

def largest_inner_rectangle_area(data):
    '''
    find all pairs s.t. no other pairs lines cross through those lines? This assumes that the inputs actually makea cohernet geometric shape and don't say cross over themselves, I think this is true.

    step 1: make list of all lines in the form of (start, end, invarient, axis) where axis = 'x' or 'y' meaning it is either a line parallel to x or y axis.
    step 2: do logic like above, but also for each rectangle, check wether any of the lines crosses any of the lines given. 
    '''
    connecting_lines = []
    for i in range(len(data)):
        a = data[i]
        if i<len(data-1):
            b = data[i+1]
        else: 
            b = data[0]
        


    pass
 
def get_data():
    with open(INPUT_FILENAME) as f:
        lines = f.readlines()
        coords = [[int(s.strip()) for s in line.split(',')] for line in lines]
    
    return coords

def main():
    data = get_data()
    p1_sol = largest_rectangle_area(data)

    print('largest possible rectangle area: {}'.format(p1_sol))

if __name__ == "__main__":
    main()