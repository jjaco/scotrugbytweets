from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree

from more_itertools import windowed
import pandas as pd

def clean_tweet(tweet):
	twitter_punc = ['#', '@', 'https', '//t.co', 'RT']
	terms_to_remove = ['Edinburgh', 'Glasgow', 'Scotstoun', 
        'Murrayfield', 'Scotland', 'Warrior',
        'England', 'Wales', 'Italy', 'France',
        'Ireland', 'Pro14', 'Guinness']
	filter_list = twitter_punc + terms_to_remove

	filtered = [word for word in tweet.split() if not any(punc in word for punc in filter_list)]

	return ' '.join(filtered)


def extract_entities(tweet):
	cleaned_tweet = clean_tweet(tweet)
	part_of_speech = pos_tag(word_tokenize(cleaned_tweet))
	chunked_pos = ne_chunk(part_of_speech)
	tree_entities = [chunk for chunk in chunked_pos if type(chunk) == Tree]
	flat_entities = [[name for (name, label) in entity] for entity in tree_entities]

	return str([" ".join(name) for name in flat_entities])


def extract_feature_vector(tweet, tweet_index):
    cleaned_tweet = clean_tweet(tweet)
    part_of_speech = pos_tag(word_tokenize(cleaned_tweet))

    entities_with_labels = [(entity, label, tweet_index) for entity, label in part_of_speech]

    def _forename_surname_labeller(sentence):
        padded_sentence = (
            [(None, None, None)] 
            + sentence 
            + [(None, None, None)]
        )
        labels = list(zip(*padded_sentence))[1]
        paired_labels = list(windowed(labels, n=2))
        
        mask = []
        for paired_label in paired_labels:
            label_before, label = paired_label
            if label == 'NNP':
                if label_before == 'NNP':
                    mask.append(2)
                else:
                    mask.append(1)
            else:
                mask.append(0)
                
        sentence_df = pd.DataFrame(padded_sentence).dropna()
        sentence_df.columns = ['word', 'pos', 's_id']
        sentence_df['label'] = mask[:-1]
        
        return sentence_df

    results_df = _forename_surname_labeller(entities_with_labels)

    return results_df[['word', 'label', 's_id']]