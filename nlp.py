from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree

def clean_tweet(tweet):
	twitter_punc = ['#', '@']
	filtered = [word for word in tweet.split() if not any(punc in word for punc in twitter_punc)]

	return ' '.join(filtered)


def extract_entities(tweet):
	cleaned_tweet = clean_tweet(tweet)
	part_of_speech = pos_tag(word_tokenize(cleaned_tweet))
	chunked_pos = ne_chunk(part_of_speech)
	tree_entities = [chunk for chunk in chunked_pos if type(chunk) == Tree]
	flat_entities = [[name for (name, label) in entity] for entity in tree_entities]

	return str([" ".join(name) for name in flat_entities])