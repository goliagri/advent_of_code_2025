#https://adventofcode.com/2025/day/10
INPUT_FILENAME = "inputs/input_10.txt"
def get_min_button_presses(data):
    res = 0

    def bfs(target, buttons):
        
        visited = {} #dict of frozen sets -> minimum num of steps to reach
        frontier = [] #bfs means queue-ordered frontier in terms of frozen sets.

        visited[frozenset()] = 0
        frontier.append(frozenset())

        while frontier:
            cur_state = frontier.pop(0)
            cur_depth = visited[cur_state]
            if cur_state == target:
                return cur_depth
            next_depth = cur_depth + 1
            for button in buttons:
                next_state = cur_state ^ button
                if not next_state in visited.keys():
                    frontier.append(next_state)
                    visited[next_state] = next_depth
                
        return None #failed to find any series of button presses to reach target state

    for machine_spec in data:
        #we want to use button presses to search space 
        min_button_presses = bfs(machine_spec['lights_on'], machine_spec['buttons'])
        if min_button_presses is None:
            raise Exception('failed to find any solving set of button presses')
        res += min_button_presses

    return res

''' #Wayyyy too inneficient, can't do searching over such a large space
def get_min_button_presses_joltage(data):
    res = 0

    def bfs(target, buttons):
        
        visited = {} #dict of frozen sets -> minimum num of steps to reach
        frontier = [] #bfs means queue-ordered frontier in terms of frozen sets.

        visited[tuple([0 for _ in range(len(target))])] = 0
        frontier.append(tuple([0 for _ in range(len(target))]))

        while frontier:
            cur_state = frontier.pop(0)
            #print(cur_state)
            for i in range(len(target)):
                if target[i] < cur_state[i]:
                    continue
            cur_depth = visited[cur_state]
            if cur_state == target:
                return cur_depth
            next_depth = cur_depth + 1
            for button in buttons:
                next_state = list(cur_state)
                for a in button:
                    next_state[a] += 1
                next_state = tuple(next_state)
                if not next_state in visited.keys():
                    frontier.append(next_state)
                    visited[next_state] = next_depth
                
        return None #failed to find any series of button presses to reach target state

    for machine_spec in data:
        #we want to use button presses to search space 
        min_button_presses = bfs(machine_spec['joltage_limits'], machine_spec['buttons'])
        print('!')
        if min_button_presses is None:
            raise Exception('failed to find any solving set of button presses')
        res += min_button_presses

    return res
'''

def get_data():
    res = []
    with open(INPUT_FILENAME) as f:
        lines = f.readlines()
        lines = [[a.strip() for a in line.split(' ')] for line in lines]

        for line in lines:
            res.append({'lights_on': set(), 'buttons':[], 'joltage_limits':[]})
            for a in line:
                b = a[1:-1]
                #is lights_on
                if a[0] == '[':
                    for i, indicator in enumerate(b):
                        if indicator == '#':
                            res[-1]['lights_on'].add(i)
                    res[-1]['lights_on'] = frozenset(res[-1]['lights_on'])

                elif a[0] == '(':
                    b = frozenset([int(j) for j in b.split(',')])
                    res[-1]['buttons'].append(b)

                elif a[0] == '{':
                    res[-1]['joltage_limits'] = [int(j) for j in b.split(',')]

                else:
                    raise Exception(' uknown dtype indicator {}'.format(a[0]))
    
    return res

def main():
    data = get_data()
    p1_sol = get_min_button_presses(data)
    p2_sol = get_min_button_presses_joltage(data)

    print('minimum presses to turn all machines on: {}'.format(p1_sol))
    print('minimum presses to achieve joltage targets: {}'.format(p2_sol))

if __name__ == "__main__":
    main()