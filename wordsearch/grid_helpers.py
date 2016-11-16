from constants import EMPTY_SPACE


def would_wrap_grid(x, y, grid):
    if x < 0 or x >= len(grid) or y < 0 or y >= len(grid):
        return True
    return False


def see_if_word_found(grid, word, x, y, direction):
    word_seen = ''
    possible_coordinates = set()

    while True:
        possible_coordinates.add((x, y))
        word_seen += grid[x][y]
        x += direction[0]
        y += direction[1]

        if word == word_seen:
            return True, possible_coordinates
        elif not word.startswith(word_seen) or would_wrap_grid(x, y, grid):
            return False, set()


def merge_grid(destination, source):
    for x in range(len(source)):
        for y in range(len(source)):
            if source[x][y] != EMPTY_SPACE:
                destination[x][y] = source[x][y]


def find_protected_cells(answer_key):
    '''returns a list of (x, y) tuples which are not EMPTY_SPACE

    '''
    protected_cells = []
    for x in range(len(answer_key)):
        for y in range(len(answer_key)):
            if answer_key[x][y] != EMPTY_SPACE:
                protected_cells.append((x, y))

    return protected_cells


def is_palindrome(word):
    return word == word[::-1]
