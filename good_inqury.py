import json
from fuzzywuzzy import fuzz

fr = open('all_words.txt', 'r')
all_words = json.load(fr)
fr.close()

def closest_word(my_word):
    max_val = 0
    found_word = ''
    for word in all_words:
        count = fuzz.ratio(my_word, word)
        if count == 100:
            return(word)
        elif  count > max_val:
            max_val = count
            found_word = word
    return(found_word)


def fix_misspelling(inq):
    good_inq = ''
    for word in inq.split():
        if word.isdigit() or word in all_words:
            good_inq = good_inq + word
        else: 
            good_inq = good_inq + closest_word(word)
        good_inq = good_inq + ' '
    return(good_inq[0:-1])


if __name__ == "__main__":

    inq = input()
    print(good_inquiry(inq))
