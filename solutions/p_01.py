#https://adventofcode.com/2025/day/1

INPUT_FILENAME = "inputs/input_01.txt"

def get_num_zeros_after_rot_in_sequence(instructions):
    '''
    Given a list of instructions of the form (direction of rotation (str "R" or "L"), magnitude of rotation (int)), start at 50 and make those rotations as if turning a 0-99 dial. Return the total number of times the dial lands on 0 after a full rotation.
    '''
    DIAL_SIZE = 100
    STARTING_VAL = 50

    zero_count = 0
    cur_num = STARTING_VAL

    #invariant: cur_num is set to num currently pointed to on dial at iteration i, zero_count is set to the total number of rotations which ended pointing to 0 up to iteration i
    for direction, magnitude in instructions:
        sign = 1 if direction == "R" else -1
        cur_num = (cur_num + (magnitude * sign)) % DIAL_SIZE
        if cur_num == 0:
            zero_count += 1
    
    return zero_count

def get_num_zeros_during_rot_in_sequence(instructions):
    '''
    Given a list of instructions of the form (direction of rotation (str "R" or "L"), magnitude of rotation (int)), start at 50 and make those rotations as if turning a 0-99 dial. Return the total number of times the dial passes over 0 (either durring or at the end of a rotation)

    not robust to instructions of turning 0, eg "L0", I think these are invalid though so should be fine. 
    '''
    DIAL_SIZE = 100
    STARTING_VAL = 50

    zero_count = 0
    cur_num = STARTING_VAL

    #invariant: cur_num is set to num currently pointed to on dial at iteration i, zero_count is set to the total number of rotations which ended pointing to 0 up to iteration i
    for direction, magnitude in instructions:
        sign = 1 if direction == "R" else -1

        prev_num = cur_num
        cur_num = (cur_num + (magnitude * sign)) 
        
        #counts number of wrap arounds, generally involve traversing 0
        zero_crosses = abs(cur_num // 100)

        # if we start at 0 and wrap around downards, we are overcounting by 1
        if prev_num == 0 and sign == -1:
            zero_count -= 1 

        cur_num = cur_num % DIAL_SIZE

        #if we end at 0 and arrived there from above, we are undercounting by 1
        if cur_num == 0 and sign == -1:
            zero_count += 1 


        zero_count += zero_crosses
    
    return zero_count


def get_instructions():
    # translate txt file into instructions in the form of (direction, magnitude) tuples (currently no checks for validity)
    instructions = []
    with open(INPUT_FILENAME) as file:
        for line in file:
            if not line: #ignore empty lines 
                continue
            direction = line[0]
            quant = int(line[1:])
            instructions.append((direction, quant))

    return instructions


def main():
    instructions = get_instructions()
    num_zeros_after_rot= get_num_zeros_after_rot_in_sequence(instructions)
    num_zeros_during_rot = get_num_zeros_during_rot_in_sequence(instructions)
    print("number of 0's after completed rotations {}".format(num_zeros_after_rot))
    print("number of times pointer passes over 0 ever {}".format(num_zeros_during_rot))


if __name__ == "__main__":
    main()