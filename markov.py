#!/usr/bin/env python

import sys
import random
import string

def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    #using corpus instead of "file_string" b/c corpus is the generic argument used for this block of code.  It is replaced w/ whatever is passed in the main function.''

    chain_dict = {}

    sentence_list = massage_corpus(corpus)
    for sentence in sentence_list:
        sentence = sentence.strip()
        list_of_words = sentence.split(" ")
        last_tuple = len(list_of_words) - 2 
        for x in range(0, last_tuple):
           key_tuple = (list_of_words[x], list_of_words[x + 1])
           value_list = [list_of_words[x + 2]]
           chain_dict[key_tuple] = chain_dict.get(key_tuple, []) + value_list

        key_tuple = (list_of_words[last_tuple],list_of_words[last_tuple + 1])
        value_list = ["."]
        chain_dict[key_tuple] = chain_dict.get(key_tuple, []) + value_list

    return chain_dict

def massage_corpus(corpus):
    """Takes corpus, returns list of sentences"""

    #probably be cleaned up with maketrans and translate

    corpus = corpus.replace("\n", " ").replace("!", ".").replace("?", ".").replace('\'', "").replace("(", "").replace(")", "")
    return  corpus.split(".")

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    random_value = None
    key_list = chains.keys()
    random_tuple = random.choice(key_list)
    markov_sent = [random_tuple[0], random_tuple[1]]
    while random_value != ".":
        tuple_values = chains[random_tuple]
        random_value = random.choice(tuple_values)
        markov_sent.append(random_value)
        random_tuple = (random_tuple[1], random_value)

    # print markov_sent

    #writing a join as a loop
    #markov_sent is a list! We're going to concatinate the strings in this list. 
    # for word in markov_sent:

    str = " "
    markov_string = str.join(markov_sent)
    return markov_string

def main():
    args = sys.argv

    program, file_name = args
    file_object = open(file_name)
    file_string = file_object.read()

    input_text = "sample.txt"

    chain_dict = make_chains(file_string)
    random_text = make_text(chain_dict)
    print random_text


if __name__ == "__main__":
    main()