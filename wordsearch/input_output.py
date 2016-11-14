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
    for word in wordlist:
        if words.count(word) > 1:
            print "DISCARDING ", word
            wordlist.remove(word)

    return wordlist
