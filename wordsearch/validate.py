from constants import DIRECTIONS


def validate(grid, wordlist):
    ''' Make sure there's only 1 possible solution '''
    for word in wordlist:
        if count_word(grid, word) != 1:
            return False
    return True


def count_word(grid, word):
    ''' Counts the number of times a given word is found '''

    count = 0
    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x][y] == word[0]:  # could this be a match?
                for direction in DIRECTIONS:
                    if check_for_word(grid, word, x, y, direction):
                        count += 1
    return count


def check_for_word(grid, word, x, y, direction):
    ''' Follows the given direction looking for the word given

    returns True if word found, False otherwise
    '''
    word_seen = ''
    while True:
        word_seen += grid[x][y]
        x += direction[0]
        y += direction[1]

        if word == word_seen:
            return True
        if not word.startswith(word_seen):
            return False
        if x < 0 or x >= len(grid):
            return False
        if y < 0 or y >= len(grid):
            return False
