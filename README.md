# wordsearch
Creates word search puzzles, with an optional answer key

https://en.wikipedia.org/wiki/Word_search

# Usage

When provided a source word list, the code generates a word search puzzle.

    $ wordsearch wordlist.txt --answer_key answers.txt
    == Loading wordlist
    == Generating wordsearch
    Validating grid
    == Writing wordsearch
    AFRAID
    ALCOHOLIC
    ALLOW
    AUTHORITY
    BORDER
    CARTOGRAPHY
    CHANNEL
    DISTANCE
    MISMATCHED
    SCATTER
    SECRETARY
    SICK
    WANTING


    G S C I L O H O C L A
    C A R T O G R A P H Y
    L R I D I A R F A D T
    W E O M C H A N N E L
    F D E H C T A M S I M
    L R W A N T I N G H T
    S O Y R A T E R C E S
    I B T E C N A T S I D
    C N A L L O W C N E O
    K M Y T I R O H T U A
    T R E T T A C S C N R

### Additional Arguments

**answer_key <path>**
Outputs the answer key to the specified Path.  
The answer key marks the randomly inserted characters

The example above's answer key looks like the following:

    AFRAID
    ALCOHOLIC
    ALLOW
    AUTHORITY
    BORDER
    CARTOGRAPHY
    CHANNEL
    DISTANCE
    MISMATCHED
    SCATTER
    SECRETARY
    SICK
    WANTING


    # # C I L O H O C L A
    C A R T O G R A P H Y
    # R # D I A R F A # #
    # E # # C H A N N E L
    # D E H C T A M S I M
    # R W A N T I N G # #
    S O Y R A T E R C E S
    I B # E C N A T S I D
    C # A L L O W # # # #
    K # Y T I R O H T U A
    # R E T T A C S # # #

**grid_size <value>**
Allows for a multiplier to make the grid bigger.  By default, the grid tries to be the smallest
square possible.  This can cause excessive computation times, so adding some padding will not only
allow for more word placement options but increase the difficulty.
