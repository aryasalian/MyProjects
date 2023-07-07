def fancy_print(configuration):
    from _ast import If
    assert len(configuration) == 16
    print('------------')
    for i in range(len(configuration)):
        if configuration[i]<10:
            print(' ', end='')
        print(configuration[i], end = ' ')
        if i % 4 == 3:
            print()
    print('------------')
    
def to_2d_index(index):
    assert 0 <= index < 16
    return index//4, index%4

'a transposition is a tuple of place \
locations(not piece numbers/labels)'

def apply_transposition(configuration, transposition):
    i, j = transposition
    assert i in range(16) and j in range(16)
    assert i != j
    i1, i2 = to_2d_index(i)
    j1, j2 = to_2d_index(j)
    assert abs(i1 - j1) + abs(i2 - j2) == 1
    assert configuration[i]==0 or configuration[j]==0
    
    configuration[i], configuration[j] = configuration[j], configuration[i]
    
def apply_transpositions(configuration, transpositions):
    for transposition in transpositions:
        apply_transposition(configuration, transposition)
        
def cycle_shift(configuration, path):
    start = 0
    while configuration[path[start]] != 0:
        start = start + 1
    rotated = path[start:]+path[:start]
    transpositions = []
    for i in range(len(rotated)-1):
        transpositions += [(rotated[i], rotated[i+1])]
    apply_transpositions(configuration, transpositions)
    return (transpositions)

'defining constants for specific cycle paths which will be used \
in making a 3 cycle shift and bringing the a, b, c and d to \
a corner/ 2x2 square'

cycle1 = [0, 4, 8, 12, 13, 14, 15, 11, 7, 3, 2, 6, 10, 9, 5, 1]
cycle2a = [1, 5, 4, 8, 9, 13, 14, 15, 11, 10, 6, 7, 3, 2]
cycle2b = [1, 5, 4, 8, 12, 13, 9, 10, 14, 15, 11, 7, 6, 2]
cycle3 = [1, 5, 9, 8, 12, 13, 14, 15, 11, 10, 6, 7, 3, 2]
cycle4 = [2, 6, 5, 9, 8, 12, 13, 14, 15, 11, 7, 3]


'a, b, c are piece names/labels'
def do_3_cycle(cfg, a, b, c):
    assert a in range(16) and b in range(16) and c in range(16)
    assert a!=b and b!=c and c!=a
    assert a!=0 and b!=0 and c!=0
    transpositions = []
    
    'move a to top left corner(position 0)'
    while cfg[0] != a:
        transpositions += cycle_shift(cfg, cycle1)
        
    'move c below a'
    if cfg[12] != c:
        if cfg[12] == 0:
            transposition = (12, 8 if cfg[8]!=c else 13)
            transpositions += [transposition]
            apply_transposition(cfg, transposition)
        
        while cfg[4] != c:
            transpositions += cycle_shift(cfg, cycle2a)
        
    else:
        assert cfg[12] == c
        if cfg[3] == 0:
            transposition = (3, 7) #cfg[7] cannot be c since c's at 12
            transpositions += [transposition]
            apply_transposition(cfg,transposition)
            
        while cfg[4] != c:
            transpositions += cycle_shift(cfg, cycle2b)
    
    'move b next to a'
    while cfg[1] != b:
        transpositions += cycle_shift(cfg, cycle3)
        
    'move empty space next to the 2x2 block'
    if cfg[10] == 0:
        transposition = (10,11)
        transpositions += [transposition]
        apply_transposition(cfg,transposition)
        
    while cfg[5] != 0:
        transpositions += cycle_shift(cfg, cycle4)
        
        
    assert cfg[0] == a and cfg[1] == b and cfg[4] == c and cfg[5] == 0
    'now that 3-cycle is done, we retrace our steps'
    abccycle_and_reverse = [(1, 5), (0, 1), (0, 4), (4, 5)] + \
                            list(reversed(transpositions))
    apply_transpositions(cfg, abccycle_and_reverse)
    transpositions += abccycle_and_reverse
    return transpositions

def transpositions_solution(configuration):
    standard = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    transpositions = []
    current = list(configuration)
    
    for i in range(13):
        if current[i] != standard[i]:
            idx = current.index(standard[i])
            assert idx > i
            'piece at position idx should be moved to i'
            spare = i+1 if i+1 != idx else i+2
            a, b, c = current[idx], current[i], current[spare]
            transpositions += do_3_cycle(current, a, b, c)
        assert current[i]==standard[i]
        
    return transpositions

def solution(configuration):
    transpositions = transpositions_solution(configuration)
    answer = []
    current = list(configuration)
    
    for trans in transpositions:
        i, j = trans
        label = current[i] if current[i]!=0 else current[j]
        answer.append(label)
        apply_transposition(current, trans)
    
    print("Required moves of pieces to reach the standard configuration are:")    
    return answer

'-------------------------------------------------------------'

print("Original configuration before any moves:")
config1 = [1,3,4,5,2,6,7,8,9,10,11,12,14,13,15,0]
fancy_print(config1)
print()
print(solution(config1))    
print()
print("Configuration reached after executing all these moves:")
apply_transpositions(config1, transpositions_solution(config1))        
fancy_print(config1)