import string

import constants
from grid_helpers import find_protected_cells, is_palindrome, see_if_word_found
from random import choice, randrange, sample, shuffle
from validate import validate


def generate_wordsearch(wordlist, min_grid_size=1):
    ''' Creates a wordsearch and returns the generated grid and an answer key

    wordlist: The words to populate the grid with
    difficulty: Adjusts the size of the grid and thus amount of fill-in squares,
                recommend not setting bigger than 3 or 4
    '''
    shuffle(wordlist)

    # Start the grid with size equal to longest word in list
    word_lengths = map(len, wordlist)
    total_chars = len("".join(wordlist))
    initial_grid_size = max(word_lengths + [min_grid_size])
    while initial_grid_size * initial_grid_size <= 1.4 * total_chars:
        initial_grid_size += 1

    answer_key = _init_grid(initial_grid_size)

    while not place_words(answer_key, words_left=wordlist) or not validate(answer_key, wordlist):
        # we couldn't find a solution, so make the grid bigger and try again
        print "Couldn't place words on grid size of ", len(answer_key), "trying bigger"
        answer_key = _init_grid(len(answer_key)+1)

    '''
        Create a random grid
        merge answer_key over
        if a word found too many times, swap a letter
    '''

    protected_cells = find_protected_cells(answer_key)
    random_grid = _copy_grid(answer_key)
    fill_in(random_grid, wordlist)

    failure_count = 0
    while not validate(random_grid, wordlist):
        failure_count += 1
        scramble_found_words(random_grid, wordlist, protected_cells)
        # if after 5 tries we still haven't made it work, let's abandon and start over
        # TODO: it's pretty bad to recurse here.
        # Really should try placing words again with a larger grid
        if failure_count > 5:
            return generate_wordsearch(wordlist, min_grid_size)

    return random_grid, answer_key


def fill_in(grid, wordlist, sample_size=8):
    ''' Fill in empty spaces in the grid, using letters from the wordlist

    grid: the wordsearch grid to fill in
    wordlist: used to seed random fill in
    sample_size: number of random alphabet letters to salt the wordlist letters with
    '''
    preference_letters = list(set(''.join(wordlist))) + sample(list(string.uppercase),
                                                               min(sample_size, 26))
    for x in range(0, len(grid)):
        for y in range(0, len(grid)):
            if grid[x][y] == constants.EMPTY_SPACE:
                grid[x][y] = choice(preference_letters)


def scramble_found_words(grid, wordlist, protected_cells=set()):
    ''' Ensure the given wordlist only appears once

    Searches the grid for a given word.
    If the word is found more than once, scrambles any cells which are not included
    in the protected_cell list (derived from an answer_key)

    '''
    for word in wordlist:
        count = 0
        coordinates_of_words = set()
        for x in range(len(grid)):
            for y in range(len(grid)):
                if grid[x][y] == word[0]:
                    for direction in constants.DIRECTIONS:
                        found, possible_coordinates = see_if_word_found(grid, word, x, y, direction)
                        if found:
                            coordinates_of_words.union(possible_coordinates)
                            count += 1

        if (count >= 2 and is_palindrome(word)) or (count >= 1 and not is_palindrome(word)):
            positions_ok_to_scramble = coordinates_of_words.difference(protected_cells)
            for x, y in positions_ok_to_scramble:
                grid[x][y] = choice(string.uppercase)


def place_words(grid, words_left):
    '''Main word placement algorithm (recursive)

    Attempts to place a word in the grid at a random location and direction
    If the word can't be placed there, a new direction and/or position is chosen.
    Once all positions have been checked and it doesn't fit, we need to unwind the last word
    and try again.
    '''
    if not words_left:
        return True

    word_to_place = words_left[0]

    tested_positions = set()
    # randomize directions to try
    directions = sample(constants.DIRECTIONS, len(constants.DIRECTIONS))
    num_cells_in_grid = len(grid)*len(grid)
    backtrack_count = 0

    while len(tested_positions) < num_cells_in_grid:

        # grab a random position and mark it
        xpos = randrange(0, len(grid))
        ypos = randrange(0, len(grid))
        tested_positions.add((xpos, ypos))

        # if this is not a possible starting spot, continue
        if grid[xpos][ypos] != constants.EMPTY_SPACE and grid[xpos][ypos] != word_to_place[0]:
            continue

        # try to place the word
        for direction in directions:
            if _word_can_fit(grid, word_to_place, xpos, ypos, direction=direction):

                # hold onto a copy of this grid in case we need to revert
                backtrack_grid = _copy_grid(grid)

                # place the word, and recurse
                _insert_word(grid, word_to_place, xpos, ypos, direction)
                if place_words(grid, words_left=words_left[1:]):
                    # we placed all remaining words so return success!
                    return True
                else:
                    # remaining words couldn't fit, so undo the insertion and try next direction
                    _transfer_cells(grid, backtrack_grid)

    # we exhausted all positions and directions for this word, backtrack...
    return False


def _init_grid(size):
    ''' create a square grid '''
    return [[constants.EMPTY_SPACE for x in range(size)] for y in range(size)]


def _word_can_fit(grid, word, x, y, direction):

    ''' Checks to see if the given word can fit in the direction given from a start position

    grid: The grid to check, really only need grid width/height
    word: the word to check
    x, y: Coordinates to start from
    direction: one of the 8 directions are we assessing

    '''
    # would word placement go beyond edge of grid?
    end_x = len(word) * direction[0] + x
    end_y = len(word) * direction[1] + y

    if end_x < 0 or end_x > len(grid):
        return False

    if end_y < 0 or end_y > len(grid):
        return False

    # check placement of letters, if we hit a populated cell with a mismatched letter, fail
    for letter in word:
        if grid[x][y] == letter or grid[x][y] == constants.EMPTY_SPACE:
            x += direction[0]
            y += direction[1]
        else:
            return False

    return True


def _copy_grid(grid):
    ''' Generate a clone of the grid '''
    new_grid = _init_grid(len(grid))
    return _transfer_cells(new_grid, grid)


def _transfer_cells(grid, backtrack_grid):
    ''' Restore grid cell data with info from the saved backtrack_grid '''
    for x in range(len(backtrack_grid)):
        for y in range(len(backtrack_grid)):
            grid[x][y] = backtrack_grid[x][y]
    return grid


def _insert_word(grid, word, xpos, ypos, direction):
    '''Place the word on the grid

    grid:
    word: the word to place
    xpos, ypos: starting position
    direction: The direction to place letters

    Note: Assumes the word fits without collisions!
    '''
    for letter in word:
        grid[xpos][ypos] = letter
        xpos += direction[0]
        ypos += direction[1]
    return grid
