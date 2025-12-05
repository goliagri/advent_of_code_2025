#https://adventofcode.com/2025/day/3
INPUT_FILENAME = "inputs/input_03.txt"


def get_max_joltage(battery_list, batteries_on):
    '''
    battery_list is a list of list of integers each of the inner lists being of length > batteries_on denoting banks of batteries with given integer values
    batteries_on is the number of batteries to be turned on per bank.
    Returns the maximum joltage from sum of all banks
    Each bank's joltage is equal to the concatenation of the values of the batteries turned on in that order. 
    '''
    res = 0

    for l in battery_list:
        max_bank_joltage = 0
        battery_vals = []
        last_picked_battery_index = -1
        for i in range(batteries_on, 0, -1):
            if i > 1: 
                max_val =  max(l[last_picked_battery_index+1:-(i-1)])
            else:
                max_val =  max(l[last_picked_battery_index+1:])
            max_idx = l.index(max_val, last_picked_battery_index+1)
            battery_vals.append(max_val)
            last_picked_battery_index = max_idx

        for j in range(0,batteries_on):
            max_bank_joltage += battery_vals[j] * 10**(batteries_on-(j+1))

        res += max_bank_joltage

    return res

def get_data():

    with open(INPUT_FILENAME) as f:
        lines = f.readlines()
        data = [ [int(a) for a in line.strip() ] for line in lines]

    return data





def main():
    data = get_data()
    max_joltage_2_batteries = get_max_joltage(data, 2)
    max_joltage_12_batteries = get_max_joltage(data, 12)
    print('Max Joltage from 2-batteries per bank: {}'.format(max_joltage_2_batteries))
    print('Max Joltage from 12-batteries per bank: {}'.format(max_joltage_12_batteries))


if __name__ == "__main__":
    main()