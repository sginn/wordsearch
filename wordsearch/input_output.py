def write_wordsearch(f, wordsearch, wordlist):

    '''prints 2d wordsearch to screen

        [['a','b','c'], ['d', 'e', 'f'], ['g','h','i']]

        a b c
        d e f
        g h i
    '''
    for row in wordsearch:
        f.write(" ".join(row))
        f.write("\n")

    for word in wordlist:
        f.write("{word}\n".format(word=word))


def load_wordlist(f):
    wordlist = f.readlines()
    return sanitize_wordlist(wordlist)


def sanitize_wordlist(wordlist):
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
