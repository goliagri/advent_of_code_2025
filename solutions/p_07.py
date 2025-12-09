#https://adventofcode.com/2025/day/7
INPUT_FILENAME = "inputs/input_07.txt"


def run_splitter(data):
    
    depth = len(data)
    width = len(data[0])

    running_beams = [0 for _ in range(width)]
    res = 0

    for i in range(depth):
        new_beams = [0 for _ in range(width)]
        for j in range(width):
            if running_beams[j] == 1:
                if data[i][j] == '^':   
                    res += 1
                    if j > 0:
                        new_beams[j-1] = 1
                    if j < width-1:
                        new_beams[j+1] = 1
                else:
                    new_beams[j] = 1
            if data[i][j] == 'S':
                new_beams[j] = 1
            
        running_beams = new_beams

    return res

def run_quantum_splitter(data):
    depth = len(data)
    width = len(data[0])
    running_beams = [0 for _ in range(width)]

    for i in range(depth):
        new_beams = [0 for _ in range(width)]
        for j in range(width):
            if running_beams[j] >= 1:
                if data[i][j] == '^':
                    if j > 0:
                        new_beams[j-1] += running_beams[j]
                    if j < width - 1:
                        new_beams[j+1] += running_beams[j]
                else:
                    new_beams[j] += running_beams[j]
            if data[i][j] == 'S':
                new_beams[j] = 1
            
        running_beams = new_beams
        
    return sum(running_beams)


def get_data():
    with open(INPUT_FILENAME) as f:
        lines = f.readlines()
        lines = [[a for a in s.strip()] for s in lines]
    
    return lines




def main():
    data = get_data()

    p1_sol = run_splitter(data)
    p2_sol = run_quantum_splitter(data)

    print('number of total beam splits: {}'.format(p1_sol))
    print('number of total timelines in quantum splits: {}'.format(p2_sol))


if __name__ == "__main__":
    main()