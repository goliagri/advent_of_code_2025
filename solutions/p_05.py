#https://adventofcode.com/2025/day/5
INPUT_FILENAME = "inputs/input_05.txt"

def find_fresh_ingredients(ranges, IDs):
    if not ranges:
        return 0
    ranges = sorted(ranges)
    #merge overlapping ranges
    non_overlapping_ranges = combine_overlapping_ranges(ranges)

    #process: binary search till either find is valid or no valid range
    def bts(val, lo, hi):
        if lo >= hi:
            return False
        mid = (lo+hi)//2
        a,b = non_overlapping_ranges[mid]
        if val >= a and val <= b:
            return True

        
        if val < a:
            return bts(val, lo, mid)
        elif val > b:
            return bts(val, mid+1, hi)

    res = 0
    for id in IDs:
        #if bts(id, 0, len(ranges)):
        #    res += 1

        for a,b in non_overlapping_ranges:
            if id >= a and id <= b:
                res += 1
                if not bts(id, 0, len(non_overlapping_ranges)):
                    print("MISSED BINARY SEARCH: Range --- {} ; ID --- {}".format((a,b), id))
                break
        
    return res

def combine_overlapping_ranges(ranges):
    new_ranges = []
    cur_range = ranges[0]
    for i in range(1, len(ranges)):
        next_range = ranges[i]
        if next_range[0] <= cur_range[1]:
            cur_range = (cur_range[0], max(cur_range[1],next_range[1]))
        else:
            new_ranges.append(cur_range)
            cur_range = next_range
    new_ranges.append(cur_range)
    return new_ranges

def total_fresh_ids_in_ranges(ranges):
    ranges = sorted(ranges)
    combined_ranges = combine_overlapping_ranges(ranges)

    res = 0
    for a,b in combined_ranges:
        res += b - a + 1
    return res


def get_data():
    ranges = []

    with open(INPUT_FILENAME) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            line = [int(a) for a in line.split('-')]
            ranges.append(tuple(line))
        
        IDs = [int(line.strip()) for line in f.readlines()]

    return ranges, IDs


def main():

    ranges, IDs = get_data()
    p1_sol = find_fresh_ingredients(ranges, IDs)
    p2_sol = total_fresh_ids_in_ranges(ranges)
    
    print('number of valid ids: {}'.format(p1_sol))
    print('number of possible valid ids in range {}'.format(p2_sol))


if __name__ == "__main__":
    main()