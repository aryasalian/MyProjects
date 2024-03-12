# 15-Puzzle Solver

This program solves the infamous [15-Puzzle Problem](https://en.wikipedia.org/wiki/15_puzzle) and returns the solution in the form of a set of
instructions to be followed to reach the right configuration. Not all configurations of the puzzle are solvable; the program will find solutions to only the inherently solvable 
configurations and will leave the inherently unsolvable configurations at the popularly known **_"14-15 configuration"_** where all pieces are in their right place except for 14 and 15
(their places are switched).

As it is, finding the solution to the 15 Puzzle Problem would be very difficult to reproduce in code. But this issue can be resolved by treating the 15 Puzzle Problem as a mathematical 
problem instead. And on doing so, we soon realise that by assuming the empty space to be a puzzle piece (in this case, a piece labelled 0), we can treat each movement of a puzzle piece 
as a transposition/exchange of the piece with the piece labelled 0 (the empty space). Hence, the set of instructions to be returned as output can be reduced to a set of all exchanges we 
would need to do to get the required configuration. Other important tricks to solve any even permutation of a 15 Puzzle Problem are cycle shift and 3-cycle (more info on the same can be
found [here](https://en.wikipedia.org/wiki/Permutation#Definition)). In theory, you can achieve any even permutation of a set using a 3-cycle. Hence this is the key to our solution and it is 
also convenient to reproduce it in code by using transpositions to record the movements.

![15-puzzle](https://github.com/aryasalian/MyProjects/assets/138736627/17b0cdbc-fba1-44d8-8985-2ad0901f3d91)


## More about the code's specifics:
<ins>I/P</ins>: a list of all piece label names at any jumbled-up position (position is denoted by the index number of the element in the said list)

<ins>O/P</ins>: a list of all switches to be made to get the pieces in their right position (switches are denoted by just the label name of the piece to be switched with the empty space)
