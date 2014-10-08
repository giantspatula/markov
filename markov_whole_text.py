#!/usr/bin/env python

import sys
import random
import string
import re

def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    
    chain_dict = {}

    word_list = massage_corpus(corpus)
    populate_dict(word_list, chain_dict)

    return chain_dict

def populate_dict(word_list, dict):

    last_tuple = len(word_list) - 2 
    for x in range(0, last_tuple):
        key_tuple = (word_list[x], word_list[x + 1])
        value_list = [word_list[x + 2]]
        dict[key_tuple] = dict.get(key_tuple, []) + value_list

    key_tuple = (word_list[last_tuple],word_list[last_tuple + 1])
    dict[key_tuple] = dict.get(key_tuple, []) + value_list


def massage_corpus(corpus):
    """Takes corpus, returns list of words including valid punctuation"""

    corpus = corpus.replace("\n", " ").replace("-", " ").replace(":", " ").replace("!", ".").replace("?", ".").replace("\r", " ").replace("\t", " ").replace("  ", " ")
    valid_punctuation = string.letters + "." + " " + "," + ";" + "'"
    clean_text = ""
    for char in corpus:
        if char in valid_punctuation:
            clean_text = clean_text + char
    list_of_words = clean_text.split()

    return list_of_words

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    random_value = None
    key_list = chains.keys()
    random_tuple = random.choice(key_list)
    print random_tuple
    word1, word2 = random_tuple
    markov_chain = [string.capitalize(word1), word2]
    #markov_chain = string.capitalize(word1) + 1 + word2
    # keeps it under 140 characters)
    sentence_length = len(word1) + len(word2) + 1
    while sentence_length < 140:
        tuple_values = chains.get(random_tuple, None)
        if tuple_values == None:
            #markov_chain = markov_chain + ". "
            markov_chain.append(".")
            random_tuple = random.choice(key_list)
            tuple_values = chains.get(None)
            sentence_length += 2
        else:
            random_value = random.choice(tuple_values)
            markov_chain.append(random_value)
            #markov_chain = markov_chain + " " + ra
            random_tuple = (random_tuple[1], random_value)
        sentence_length += len(random_value) + 1 #(accounts for spacess
    
    return " ".join(markov_chain[:-1])

# def custom_join(list):

#     first_word = list[0]
#     joined_string = string.capitalize(first_word)
#     for x in range(1,len(list)-1):
#         joined_string = joined_string + " " + list[x]
#     joined_string = joined_string + "."

#     return joined_string


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