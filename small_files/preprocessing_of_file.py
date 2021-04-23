from nltk.corpus import stopwords
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize


def doPreprocessing(alreadyStoredAnswer):

    # with open(givenFileName, "r") as fin:

    individual_items_list = []

    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(alreadyStoredAnswer)
        
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 

    filtered_sentence = [] 

    #removing stopwords
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w)
            
    #removing duplicate entry
    for w in filtered_sentence:
        if w not in individual_items_list:
            individual_items_list.append(w)  

    # making lowercase
    for w in individual_items_list:
        individual_items_list = [w.lower() for w in individual_items_list]

    return individual_items_list



def doPreprocessingOfText(givnTextData):
    individual_items_list = []

    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(givnTextData)
        
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 

    filtered_sentence = [] 

    #removing stopwords
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w)
            
    #removing duplicate entry
    for w in filtered_sentence:
        if w not in individual_items_list:
            individual_items_list.append(w)  

    # making lowercase
    for w in individual_items_list:
        individual_items_list = [w.lower() for w in individual_items_list]

    return individual_items_list

        