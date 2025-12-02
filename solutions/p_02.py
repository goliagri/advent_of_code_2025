import math

INPUT_FILENAME = "inputs/input_02.txt"

def sum_invalid_ids(ranges):
    '''
    given a list of tuples (start, end), find all ids such that (1) they are in at least one of the ranges, and (2) they are composed of a repeated series of characters (e.g. 123123)
    '''
    res = 0
    #helper func to go half_repeat -> repeat
    def repeat_val(val):
        return val + val*(10**(math.ceil(math.log(val+1,10))))
    
    #helper method which fetches half of the smallest repeat number that is larger than the input number
    def get_infimum_repeat_half(num):
        num_digits = math.ceil(math.log(num+1, 10))
        #if odd, then 100000.... is the min with num_digits//2 0's
        if num_digits % 2 == 1:
            res = 10**(num_digits//2)
        #if even, then set to either exactly the first half of num, or that num + 1 if second half is bigger.
        else:
            seperator = (10**(num_digits//2))
            start_first_half_of_digits = num // seperator
            start_second_half_of_digits = num % seperator
            
            res = start_first_half_of_digits
            if start_second_half_of_digits > start_first_half_of_digits:
                res += 1
    
        return res

    for range_start, range_end in ranges:
        start_half_val = get_infimum_repeat_half(range_start)
        end_half_val = get_infimum_repeat_half(range_end)
        print('------')
        print(range_start)
        print(start_half_val)
        print(range_end)
        print(end_half_val)
        #if end val found is exactly range_end, then fine, if above need to decriment by one to be bellow range
        if repeat_val(end_half_val) > range_end:
            end_half_val -= 1

        #now how to efficiently sum all repeats given the halfs between start_half_val and end_half_val? 
        #idea: go by increments of same digits, then can just sum all halfs and perform effective repeat on it.

        start_half_val_num_digits = math.ceil(math.log(start_half_val+1, 10))
        end_half_val_num_digits = math.ceil(math.log(end_half_val+1, 10))

        cur_half_val = start_half_val
        for i in range(start_half_val_num_digits, end_half_val_num_digits+1):
            #if in num digits of end of range, thats the stopping point, otherwise go to 99999....
            if i == end_half_val_num_digits:
                target_half_val = end_half_val
            else:
                target_half_val = 10**(i+1)-1

            #formula for summing all nums between n and m is (n-m+1)(n+m)/2
            half_val_sums =  (target_half_val - cur_half_val + 1)*(target_half_val + cur_half_val)//2
            print(half_val_sums)
            #turn sum of halfs into sum of repeats
            repeat_sums = half_val_sums + half_val_sums * (10**i)
            res += repeat_sums
            print('*' + str(repeat_sums))

            cur_half_val = 10**(i+1)

    return res

def get_ranges():
    with open(INPUT_FILENAME) as f:
        txt = f.readline()
        ranges = [a.split('-') for a in txt.split(',')]
        for i in range(len(ranges)):
            ranges[i][0] = int(ranges[i][0])
            ranges[i][1] = int(ranges[i][1])
        
    return ranges

def main():
    ranges = get_ranges()
    invalid_sum = sum_invalid_ids(ranges)
    print('sum of invalid ids: {}'.format(invalid_sum))



if __name__ == "__main__":
    main()