import sys
import random
import string
import re

def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary."""
    
    chain_dict = {}

    sentence_list = massage_corpus(corpus).split(".")
    for sentence in sentence_list:
        populate_dict(sentence, chain_dict)

    return chain_dict

def populate_dict(sentence, dict):

    list_of_words = sentence.split()
    if len(list_of_words) >= 2:
        last_tuple = len(list_of_words) - 2 
        for x in range(0, last_tuple):
            key_tuple = (list_of_words[x], list_of_words[x + 1])
            value_list = [list_of_words[x + 2]]
            dict[key_tuple] = dict.get(key_tuple, []) + value_list

        key_tuple = (list_of_words[last_tuple],list_of_words[last_tuple + 1])
        value_list = ["."]
        dict[key_tuple] = dict.get(key_tuple, []) + value_list
    #else:
        #sentence of length 1. Ingore word. 
    

def massage_corpus(corpus):
    """Takes corpus, returns list of sentences with cleaned words"""

    #super fucking jank

    corpus = corpus.replace("\n", " ").replace("-", " ").replace(":", " ").replace("!", ".").replace("?", ".").replace("\r", " ").replace("\t", " ").replace("  ", " ")
    valid_punctuation = string.letters + "." + " " + "," + ";" + "'"
    clean_text = ""
    for char in corpus:
        if char in valid_punctuation:
            clean_text = clean_text + char
    # sentences = clean_text.split(".")
    return clean_text.split(".")

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

    return custom_join(markov_sent)

def custom_join(list):
    # ".".join(list) == 

    # len(list)
    # return_string = ""
    # for x in range(0, len(list))
    #     return_string = return_string + "."
    # return return_string

    first_word = list[0]
    joined_string = string.capitalize(first_word)
    for x in range(1,len(list)-1):
        joined_string = joined_string + " " + list[x]
    joined_string = joined_string + "."

    return joined_string


def main():
    args = sys.argv

    program, file_name1, file_name2 = args
    file_object1 = open(file_name1)
    file_object2 = open(file_name2)

    file_string1 = file_object1.read()
    file_string2 = file_object2.read()
    
    combined_files = file_string1 + file_string2

    chain_dict = make_chains(combined_files)
    random_text = make_text(chain_dict)
    print random_text


if __name__ == "__main__":
    main()