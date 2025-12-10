#https://adventofcode.com/2025/day/9
INPUT_FILENAME = "inputs/input_09.txt"


def largest_rectangle_area(data):
    max_area = 0
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            cur_area = (abs(data[i][0]-data[j][0])+1) *((abs(data[i][1]-data[j][1]))+1)
            max_area = max(cur_area, max_area)
    return max_area
 
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