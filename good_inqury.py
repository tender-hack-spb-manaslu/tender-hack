import json
from fuzzywuzzy import fuzz

fr = open('all_words.txt', 'r')
all_words = json.load(fr)
fr.close()

def closest_word(my_word, min_ratio=50, verbose=False):
    '''
    if the actual distance is greater than max then don't fix the word
    '''
    max_val = 0
    found_word = ''
    for word in all_words:
        count = fuzz.ratio(my_word, word)
        if count == 100:
            return(word)
        elif  count > max_val:
            max_val = count
            found_word = word
    if verbose:
        print(f"word to fix: {my_word} fixed word: {found_word}, score: {max_val}, min_ratio: {min_ratio}")
    if max_val < min_ratio:
        if verbose:
            print("return word without changes")
        return my_word
    return(found_word)


def fix_misspelling(inq, min_ratio=50, verbose=False):  
    good_inq = ''
    for word in inq.split():
        if word.isdigit() or word in all_words:
            good_inq = good_inq + word
        else: 
            good_inq = good_inq + closest_word(word, min_ratio = min_ratio, verbose = verbose)
        good_inq = good_inq + ' '
    return(good_inq[0:-1])


if __name__ == "__main__":

    inq = input()
    print(good_inquiry(inq))
