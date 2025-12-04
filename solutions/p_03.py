INPUT_FILENAME = "inputs/input_03.txt"


def get_max_joltage(battery_list):
    res = 0

    for l in battery_list:
        max_val = max(l[:-1])

        first_max_idx = l.index(max_val)

        next_max_val = max(l[first_max_idx+1:])

        res += max_val*10 + next_max_val

    return res

def get_data():

    with open(INPUT_FILENAME) as f:
        lines = f.readlines()
        data = [ [int(a) for a in line.strip() ] for line in lines]

    return data





def main():
    data = get_data()
    max_joltage = get_max_joltage(data)
    print('Max Joltage from battery input: {}'.format(max_joltage))


if __name__ == "__main__":
    main()