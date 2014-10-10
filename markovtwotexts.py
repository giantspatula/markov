#!/usr/bin/env python

import sys
import random
import string
from clean import *
import twitter
import os

def make_chains(corpus, split_character = "."):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    
    chain_dict = {}

    sentence_list = corpus.split(split_character)
    for sentence in sentence_list:
        populate_dict(sentence, chain_dict, split_character)

    return chain_dict

def populate_dict(sentence, dict, split_character):
    """ Here a sentence is defined as whatever is between our make_chains split_character. It could be ., it could be \n."""

    list_of_words = sentence.split() #splits on space
    if len(list_of_words) >= 2:
        last_tuple = len(list_of_words) - 2 
        for x in range(0, last_tuple):
            key_tuple = (list_of_words[x], list_of_words[x + 1])
            value_list = [list_of_words[x + 2]]
            dict[key_tuple] = dict.get(key_tuple, []) + value_list

        key_tuple = (list_of_words[last_tuple],list_of_words[last_tuple + 1])
        value_list = [split_character]
        dict[key_tuple] = dict.get(key_tuple, []) + value_list
    #else:
        #sentence of length 1. Ingore word. 

def make_text(chains, script_formatting, split_character):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    random_value = None
    key_list = chains.keys()
    random_tuple = random.choice(key_list)
    if script_formatting:
        while random_tuple[0][-1] != ":" or random_tuple[0][0] not in string.uppercase:
            random_tuple = random.choice(key_list)
    else:
        while random_tuple[0][0] not in string.uppercase:
            random_tuple = random.choice(key_list)
    # print script_formatting
    # print random_tuple
    markov_sent = [random_tuple[0], random_tuple[1]]
    while random_value != split_character:
        tuple_values = chains[random_tuple]
        random_value = random.choice(tuple_values)
        markov_sent.append(random_value)
        random_tuple = (random_tuple[1], random_value)

    # print markov_sent

    return custom_join(markov_sent, script_formatting)

def custom_join(list, script_formatting):

    joined_string = list[0]
    if script_formatting:
        for x in range(1,len(list)-1):
            if list[x][-1] == ":":
                list[x] = "\n" + string.capitalize(list[x])
            joined_string = joined_string + " " + list[x]
        if joined_string[-1] not in ".!?,":
            joined_string += ".\n"
        else:
            joined_string += "\n"
    else:
        for x in range(1,len(list)-1):
            joined_string = joined_string + " " + list[x]
        joined_string = joined_string + ". "

    return joined_string

def tweet(message):

    consumer_key = os.environ.get("TWEETUSERNAME", None)
    consumer_secret = os.environ.get("TWEETPASSWORD", None)
    access_key = os.environ.get("TWEETACCESSKEY", None)
    access_secret = os.environ.get("TWEETACCESSSECRET", None)

    api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                    access_token_key=access_key, access_token_secret=access_secret)

    status = api.PostUpdate(message)

def main():
    args = sys.argv

    split_character = ""

    if len(sys.argv) == 4:
        program, file_name1, file_name2, split_arg = args
        split_character = str(split_arg)
    elif len(sys.argv) == 3:
        program, file_name1, file_name2 = args
        split_character = "."
    else:
        print "correct usage: markov_by_sent.py, file_name, [split_character]"
    
    script_formatting = False

    while True:
        if split_character == ".":
            # print "Splitting file by", split_character
            clean_file1 = make_clean_sentence_file(file_name1)
            clean_file2 = make_clean_sentence_file(file_name2)
            break
        elif split_character == "newline":
            # print "Splitting file by", split_character
            clean_file1 = make_clean_script_file(file_name1)
            clean_file2 = make_clean_script_file(file_name2)
            split_character = "\n"
            script_formatting = True
            break
        else:
           raise TypeError ("Illegal split character")

    file_string1 = open(clean_file1).read()
    file_string2 = open(clean_file2).read()


    chain_dict1 = make_chains(file_string1, split_character)
    chain_dict2 = make_chains(file_string2, split_character)

    total_len = 0
    twitter_list = []
    loop = 0

    x = random.randrange(1,5)

    while total_len < 140:
        dictionary = random.choice([chain_dict1, chain_dict2])
        random_text = make_text(dictionary, script_formatting, split_character)
        loop = loop + 1
        if total_len + len(random_text) <= 140:
            twitter_list.append(random_text)
            total_len += len(random_text)
        if len(twitter_list) == x:
            # print "Broke on num sentences"
            break
        if loop == 1000:
            # print "Broke on loop"
            break


    twitter_string = "".join(twitter_list)
    print twitter_string
    try:
        tweet(twitter_string)
        print "Tweeted: " + twitter_string
    except UnicodeDecodeError:
        print "Did not work."

if __name__ == "__main__":
    main()