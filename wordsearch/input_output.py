def write_wordsearch(f, wordsearch, wordlist):

    '''Writes wordsearch and wordlist to given output stream

    f: output stream, typically a file handle
    wordsearch: the grid
    wordlist: the words to find
    '''
    wordlist.sort()
    for word in wordlist:
        f.write("{word}\n".format(word=word))

    f.write("\n\n")

    for row in wordsearch:
        f.write(" ".join(row))
        f.write("\n")


def load_wordlist(f):
    ''' Retrieves valid words (and errors) from the given line-delimited input source

    returns a wordlist and list of errors found
    '''
    wordlist = f.readlines()
    return sanitize_wordlist(wordlist)


def sanitize_wordlist(wordlist):
    ''' Ensures the wordlist is 'safe'

    Will remove whitespace, make uppercase and ensures
    there aren't any duplicates or substrings and
    words are at least 3 characters

    returns two lists: valid wordlist and any found errors
    '''
    wordlist = map(str.strip, wordlist)
    wordlist = map(str.upper, wordlist)

    words = " ".join(wordlist)
    errors = []

    for word in wordlist:
        if len(word) < 3:
            errors.append(word)
            wordlist.remove(word)

        # if word appears more than once or is a substring, reject it
        if words.count(word) > 1:
            errors.append(word)
            wordlist.remove(word)

    return wordlist, errors
