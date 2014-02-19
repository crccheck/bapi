import re


def chunks(l, n):
    """
    Yield successive n-sized chunks from l.

    http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def find_data(text):
    # trim text
    start = text.index('var icon')
    text = text[start:]
    end = text.index('}')
    lines = text[:end].strip().split('\n')
    return list(chunks(lines, 6))
