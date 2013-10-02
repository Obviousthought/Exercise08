#!/usr/bin/env python
# open file, read file as string x 
# put string into list of words x
# create dictionary with keys as tuples from the list of words x
# account for case of words that are not followed by other words (go back and create a new sentence) x
# run make_chains until 140 characters or less to come up with a sentence x
# display sentence to the screen x
# tweet sentence x

import sys
import random
import twitter

api = twitter.Api(consumer_key='...', consumer_secret='...',
access_token_key='...', access_token_secret='...')

def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    dict_markov = {}
    list_of_words = corpus.split()
    for i in range(len(list_of_words)):
        list_of_words[i] = list_of_words[i].strip(",`'?;:\"!-_\t\"()").replace("_", " ").replace("--", " ")
    for i in range(len(list_of_words)-2):
        pair = (list_of_words[i], list_of_words[i+1])
        value = list_of_words[i+2]
        if dict_markov.get(pair):
            dict_markov[pair].append(value)
        else:
            dict_markov[pair] = [value]

    return dict_markov
        #returns the key (pair) and value (as a list) correctly 

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    sentence = []
    # chains imitates dict_markov
    list_of_keys = chains.keys()       

    random_key = random.choice(list_of_keys)
    random_value = random.choice(chains[random_key])
    
    #print "Random key to start with: ", random_key
    #print "Random value to start with: ", random_value
    
    sentence = random_key[0].capitalize() + " " + random_key[1] + " " + random_value + " "
    #print "Sentence before while loop: ", sentence

    while (len(sentence) <= 140):
        #print "Random key at start: ", random_key
        #print "Random value at start: ", random_value
        #print "Sentence at start: ", sentence

        random_key = (random_key[1], random_value)
        if random_key in chains:
            random_value = random.choice(chains[random_key])
        else:
            random_key = random.choice(list_of_keys)

        #print "Random key at end: ", random_key
        #print "Random value at end: ", random_value
        if len(sentence + random_value + " ") >= 140:
            if sentence[-1] == " ":
                sentence = sentence[0:-1]
                sentence = sentence + "."
            break
        sentence += random_value + " "
        #print "Sentence at end: ", sentence

    return sentence

def tweet(random_text):
    status = api.PostUpdate(random_text)
    return status

def main():
    script, filename = sys.argv

    f = open(filename)
    input_text = f.read()
    f.close()
    dictionary = make_chains(input_text)
    #print "Dictionary: ", dictionary
    tweet_text = make_text(dictionary)
    print tweet_text
    tweet(tweet_text)

if __name__ == "__main__":
    main()