import spacy

# Ensure 2 blank lines before the first function/class

def get_nlp():
    return spacy.load("en_core_web_sm")



nlp = get_nlp()

