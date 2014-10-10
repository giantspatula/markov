import string
import os.path 

def make_clean_text(file_name):
    """Takes in a text_file and creates a new clean_text_file clean of all punctuation and returns the clean file name as a string."""

    clean_file_name = "clean_" + file_name

    if not os.path.isfile(clean_file_name):
        dirty_file_object = open(file_name)
        dirty_file_string = dirty_file_object.read()
        no_punct_string = remove_punctuation(dirty_file_string)
        clean_file_object = open(clean_file_name, 'w')
        clean_file_object.write(no_punct_string)
        clean_file_object.close()
    
    return clean_file_name
        
def make_clean_sentence_file(file_name):
    "Takes in a text_file and cleans it up enough to split it based on '.' latter down the line."

    clean_file_name = "clean_sentence_" + file_name

    if not os.path.isfile(clean_file_name):
        dirty_file_object = open(file_name)
        dirty_file_string = dirty_file_object.read()
        no_punct_string = format_for_sentence_split(dirty_file_string)
        clean_file_object = open(clean_file_name, 'w')
        clean_file_object.write(no_punct_string)
        clean_file_object.close()
    
    return clean_file_name

def make_clean_script_file(file_name):
    "Takes in a text_file and cleans it up enough to split it based on '\n' latter down the line."

    clean_file_name = "clean_script_" + file_name

    if not os.path.isfile(clean_file_name):
        dirty_file_object = open(file_name)
        dirty_file_string = dirty_file_object.read()
        no_punct_string = format_whitespace(dirty_file_string)
        clean_file_object = open(clean_file_name, 'w')
        clean_file_object.write(no_punct_string)
        clean_file_object.close()
    
    return clean_file_name

def format_whitespace(corpus):
    """Replaces multiple newlines with single newline."""

    corpus = corpus.replace("\n\n", "\n").replace(">", "").replace("<", "").replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("\"", "")

    return corpus

def remove_whitespace():
    pass

def remove_punctuation(dirty_string):

    clean_string = ""

    for char in dirty_string:
        if char not in string.punctuation:
        # looking at each character in the dirty file.  If it is a punctuation included in string.punctuation, then do nothing.
            # I do not want it in my new clean string
            # If the character is not included in string.punctuation, then add it to a new clean string
            clean_string = clean_string + char

    return clean_string

def format_for_sentence_split(corpus):
    """Takes corpus string, returns clean text string ready to be split on '.'"""

    #super fucking jank

    corpus = corpus.replace("\n", " ").replace(":", " ").replace("!", ".").replace("?", ".").replace("\r", " ").replace("\t", " ").replace("  ", " ")
    valid_punctuation = string.letters + "." + " " + "," + ";" + "\'" + "-"
    print valid_punctuation
    clean_text = ""
    for char in corpus:
        if char in valid_punctuation:
            clean_text = clean_text + char
    # sentences = clean_text.split(".")
    return clean_text
