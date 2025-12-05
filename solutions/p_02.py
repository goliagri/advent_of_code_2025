#https://adventofcode.com/2025/day/2
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
            #turn sum of halfs into sum of repeats
            repeat_sums = half_val_sums + half_val_sums * (10**i)
            res += repeat_sums

            cur_half_val = 10**(i+1)

    return res

def sum_invalid_ids_pt2(ranges):
    '''
    given a list of tuples (start, end), find all ids such that (1) they are in at least one of the ranges, and (2) they are composed of a repeated series of characters (e.g. 123123)
    '''
    res = 0
    #helper func to go repeat_pref, num repeats -> repeated num
    def repeat_val(val, repeats):
        res = 0
        val_digits = math.ceil(math.log(val+1, 10))
        for i in range(repeats):
            res += val * 10**(val_digits*i)
        return res
    
    #helper method which fetches half of the smallest repeat pref such that its repeat form is larger than num
    def get_infimum_repeat_pref(num, repeats):
        num_digits = math.ceil(math.log(num+1, 10))
        num_repeat_digits = num_digits//repeats
        #if num_digits is not a multiple of repeats, then 10000... is going to be the infimussm pref
        if num_digits % repeats != 0:
            res = 10**num_repeat_digits
        #otherwise set to either exactly the first repeat pref of num, or that + 1 if not big enough
        else:
            first_repeat_length = num // (10**(num_digits - num_repeat_digits))
            res = first_repeat_length
            if repeat_val(first_repeat_length, repeats) < num:
                res += 1
        return res

    for range_start, range_end in ranges:
        range_end_digits = math.ceil(math.log(range_end+1, 10))
        for repeats in range(2,range_end_digits+1):
            
            start_pref = get_infimum_repeat_pref(range_start, repeats)
            end_pref = get_infimum_repeat_pref(range_end, repeats)
            #if end val found is exactly range_end, then fine, if above need to decriment by one to be bellow range
            if repeat_val(end_pref, repeats) > range_end:
                end_pref -= 1

            #now how to efficiently sum all repeats given the halfs between start_pref and end_pref? 
            #idea: go by increments of same digits, then can just sum all halfs and perform effective repeat on it.
            start_pref_num_digits = math.ceil(math.log(start_pref+1, 10))
            end_pref_num_digits = math.ceil(math.log(end_pref+1, 10))

            print('-----------------------')
            print('repeats {}'.format(repeats))
            print('range_start {}'.format(range_start))
            print('range_end {}'.format(range_end))
            print('start_pref {}'.format(start_pref))
            print('end_pref {}'.format(end_pref))


            cur_pref = start_pref
            for i in range(start_pref_num_digits, end_pref_num_digits+1):
                #if in num digits of end of range, thats the stopping point, otherwise go to 99999....
                if i == end_pref_num_digits:
                    target_pref = end_pref
                else:
                    target_pref = 10**(i+1)-1

                #formula for summing all nums between n and m is (n-m+1)(n+m)/2
                pref_sums =  (target_pref - cur_pref + 1)*(target_pref + cur_pref)//2
                #turn sum of halfs into sum of repeats
                repeat_sums = 0
                for j in range(repeats):
                    repeat_sums += pref_sums * 10**(i*j)

                print('*{}'.format(repeat_sums))
                res += repeat_sums

                cur_pref = 10**(i+1)    

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
    invalid_sum_v1 = sum_invalid_ids(ranges)
    invalid_sum_v2 = sum_invalid_ids_pt2(ranges)
    print('sum of repeat-2 ids: {}'.format(invalid_sum_v1))
    print('sum of repeat-anything (except 1) ids:{}'.format(invalid_sum_v2))



if __name__ == "__main__":
    main()