import spacy


def get_nlp():
    return spacy.load("en_core_web_sm")


nlp = get_nlp()
