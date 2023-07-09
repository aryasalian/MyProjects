"""
This program solves the infamous 15 Puzzle Problem (Check out https://en.wikipedia.org/wiki/15_puzzle if you don't know what it is yet) and returns the solution in the form of a set of
instructions to be followed to reach the right configuration. Not all configurations of the puzzle are solvable; the program will find solutions to only the inherently solvable 
configurations and will leave the inherently unsolvable configurations at the popularly known "14-15 configuration" where all pieces are in their right place except for 14 and 15
(their places are switched)

As it is, finding the solution to the 15 Puzzle Problem would be very difficult to  reproduce in code. But this issue can be resolved by treating the 15 Puzzle Problem as a mathematical 
problem instead. And on doing so, we soon realise that by assuming the empty space to be a puzzle piece (in this case, a piece labelled 0), we can treat each movement of a puzzle piece 
as a transposition/exchange of the piece with the piece labelled 0 (the empty space). Hence, the set of instructions to be returned as output can be reduced to a set of all exchanges we 
would need to do to get the required configuration. Other important tricks to solve any even permutation of a 15 Puzzle Problem are cycle shift and 3-cycle (More info on the same can be
found at https://en.wikipedia.org/wiki/Permutation#Definition). In theory, you can achieve any even permutation of a set using a 3-cycle. Hence this is the key to our solution and it is 
also convenient to reproduce it in code by using transpositions to record the movements.

I/P: a list of all piece label names at any jumbled-up position (position is denoted by the index number of the element in the said list)
O/P: a list of all switches to be made to get the pieces in their right position (switches are denoted by just the label name of the piece to be switched with the empty space)
"""

# prints out the list of piece labels(jumbled/solved) in the form of a table(as it usually appears in real life)
def fancy_print(configuration):
    assert len(configuration) == 16
    print('------------')
    for i in range(len(configuration)):
        if configuration[i]<10:
            print(' ', end='')
        print(configuration[i], end = ' ')
        if i % 4 == 3:
            print()
    print('------------')


# returns the 2D index form of a specific index in the configuration list (For example: 0 would be (0, 0) and 11 would be (2, 3))
def to_2d_index(index):
    assert 0 <= index < 16
    return index//4, index%4


# applies the transposition(entered as param) on the current configuration list. Makes necessary checks before executing the exchange of the pieces in the configuration list.
# Note: a transposition is a tuple of indices from the configuration list where the pieces to be switched exist(the tuple does not store the piece label nos. that are present at these indices)
def apply_transposition(configuration, transposition):
    
    #necessary checks before confirming the action of exchange
    i, j = transposition
    assert i in range(16) and j in range(16)
    assert i != j
    i1, i2 = to_2d_index(i)
    j1, j2 = to_2d_index(j)
    assert abs(i1 - j1) + abs(i2 - j2) == 1               # to ensure pieces are not diagonally but vertically or horizontally neighbours to each other
    assert configuration[i]==0 or configuration[j]==0     # one of the pieces needs to be an empty space to facilitate the switch
    
    #checks complete, proceed with exchange
    configuration[i], configuration[j] = configuration[j], configuration[i]


# simplifies the code by feeding each transposition from the list of transpositions(entered as param) into the above written apply_transposition(list, list) func.
def apply_transpositions(configuration, transpositions):
    for transposition in transpositions:
        apply_transposition(configuration, transposition)


# allows us to perform a cycle shift(a series of exchanges) along a specified cyclic path which will help us later to perform a 3-cycle
def cycle_shift(configuration, path):
    
    # find the position of the empty space in this path and wrap the list to make it the starting point of the cyclic path
    start = 0
    while configuration[path[start]] != 0:
        start = start + 1
    rotated = path[start:]+path[:start]

    # perform the transpositions along the wrapped over path to perform the cyclic shift. Save the transpositions made in a list and return them as well
    transpositions = []
    for i in range(len(rotated)-1):
        transpositions += [(rotated[i], rotated[i+1])]
    apply_transpositions(configuration, transpositions)
    return (transpositions)


# defining constants for specific cycle paths which will be used in making a 3-cycle shift and bringing the a, b, c and empty space to the top right corner/2x2 square for performing a 3 cycle
cycle1 = [0, 4, 8, 12, 13, 14, 15, 11, 7, 3, 2, 6, 10, 9, 5, 1]
cycle2a = [1, 5, 4, 8, 9, 13, 14, 15, 11, 10, 6, 7, 3, 2]
cycle2b = [1, 5, 4, 8, 12, 13, 9, 10, 14, 15, 11, 7, 6, 2]
cycle3 = [1, 5, 9, 8, 12, 13, 14, 15, 11, 10, 6, 7, 3, 2]
cycle4 = [2, 6, 5, 9, 8, 12, 13, 14, 15, 11, 7, 3]


# performs a complete 3-cycle which includes bringing the 3 elements to a corner, performing the 3-cycle and retracing the steps which were made to bring the 3 elements to the corner.
# Note: a, b and c are piece label names, not indices on the board. A dead cell is a cell whose elements will never change when we perform a cyclic shift over a particular cyclic path.
def do_3_cycle(cfg, a, b, c):
    assert a in range(16) and b in range(16) and c in range(16)
    assert a!=b and b!=c and c!=a
    assert a!=0 and b!=0 and c!=0
    transpositions = []
    
    # move a to top left corner(position 0)
    while cfg[0] != a:
        transpositions += cycle_shift(cfg, cycle1)
        
    # move c below a
    if cfg[12] != c:
        if cfg[12] == 0:
            transposition = (12, 8 if cfg[8]!=c else 13)  # removes the empty space from the dead cell where the path cycle2a will never cross over
            transpositions += [transposition]
            apply_transposition(cfg, transposition)
        
        while cfg[4] != c:
            transpositions += cycle_shift(cfg, cycle2a)  # performs the cycle shift to bring c below a
        
    else:
        assert cfg[12] == c
        if cfg[3] == 0:
            transposition = (3, 7)     # removes empty space from cycle2b's dead cell by switching with cfg[7]. Switching with cfg[7] is safe because it cannot be c(we asserted that c is at 12)
            transpositions += [transposition]
            apply_transposition(cfg,transposition)
            
        while cfg[4] != c:
            transpositions += cycle_shift(cfg, cycle2b)  # performs the cycle shift to bring c below a
    
    # move b next to a
    while cfg[1] != b:
        transpositions += cycle_shift(cfg, cycle3)   # performs the cycle shift to bring b next to a
        
    #move empty space next to the 2x2 block
    if cfg[10] == 0:
        transposition = (10,11)       # removes empty space from cycle4's dead cell
        transpositions += [transposition]
        apply_transposition(cfg,transposition)
        
    while cfg[5] != 0:
        transpositions += cycle_shift(cfg, cycle4)   # performs the cycle shift to bring empty space next to the 3 elements to be cycled
        
    assert cfg[0] == a and cfg[1] == b and cfg[4] == c and cfg[5] == 0
    
    # Now that the 3-cycle is done, we retrace our steps
    abccycle_and_reverse = [(1, 5), (0, 1), (0, 4), (4, 5)] + list(reversed(transpositions))
    apply_transpositions(cfg, abccycle_and_reverse)
    transpositions += abccycle_and_reverse    # all transpositions which were used to perform the 3-cycle and retracing steps are added on to the list of transpositions
    return transpositions


# finds the list of transpositions needed to get the final solution
# Note: this is not the final output, we will have to convert it into a list of piece label names which have to be moved into the empty space to get the solution
def transpositions_solution(configuration):
    standard = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]   # the configuration we intend to match
    transpositions = []
    current = list(configuration)
    
    for i in range(13):
        if current[i] != standard[i]:
            idx = current.index(standard[i])     # here idx is the position of the piece which would be moved to a position i
            assert idx > i
            spare = i+1 if i+1 != idx else i+2       # a spare element at position 'spare' is designated as the 3rd element to facilitate the 3-cycle
            a, b, c = current[idx], current[i], current[spare]
            transpositions += do_3_cycle(current, a, b, c)   # all transpositions required to get the solution are added to this list
        assert current[i]==standard[i]
    return transpositions


# outputs the solution in the required format(i.e. a list of piece label names which have to be moved into the empty space to get the solution)
def solution(configuration):
    transpositions = transpositions_solution(configuration)   # accesses the transpositions required to get the solution
    answer = []
    current = list(configuration)
    
    for trans in transpositions:
        i, j = trans
        label = current[i] if current[i]!=0 else current[j]   # the solution should only contain the label name of the piece to be switched with the empty space, not 0 i. e. 
                                                              # (the label name we assumed for our empty space)
        answer.append(label)
        apply_transposition(current, trans)    # not including this would cause an issue at line 165
    
    print("Required moves of pieces to reach the standard configuration are:")    
    return answer

#-----------------------------------------------------------------------------------------
#-----------------------------------* TESTING *-------------------------------------------
#-----------------------------------------------------------------------------------------

print("Original configuration before any moves:")
config1 = [1,3,4,5,2,6,7,8,9,10,11,12,14,13,15,0]
fancy_print(config1)
print()
print(solution(config1))    
print()
print("Configuration reached after executing all these moves:")
apply_transpositions(config1, transpositions_solution(config1))        
fancy_print(config1)
