from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree

import spacy

nlp = spacy.load('en')

def clean_tweet(tweet):
    twitter_punc = ['#', '@']
    terms_to_remove = ['Edinburgh', 'Glasgow', 'Scotstoun', 
        'Murrayfield', 'Scotland', 'Warrior',
        'England', 'Wales', 'Italy', 'France',
        'Ireland', 'Pro14', 'Guinness']
    filter_list = twitter_punc + terms_to_remove

    filtered = [word for word in tweet.split() if not any(punc in word for punc in filter_list)]

    return ' '.join(filtered)


def extract_entities(tweet):
    cleaned_tweet = clean_tweet(tweet)
    parsed = nlp(cleaned_tweet).ents
    entities = list([entity.text for entity in parsed if entity.label_ == 'PERSON'])

    return entities