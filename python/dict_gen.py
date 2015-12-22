# dict_gen.py
# Utility functions supporting graph construction

# Change Log:
# 2015-03-04: 
#   - Complete dictionary 1 and 2 generation described in email
#     a raw string as input
#   - Problem: some words become not readable
# 2015-03-18: 
#   - Histogram added to data structure
#   - filt added to create global dictionary
#   - fixed bug on lower case conversion
# 2015-03-18: 
#   - Punctuations removed for all text
#   - Code shortened for table 1,2 generation
#   - print_table function added for better looking
#   - Debugging flag added
# 2015-03-19:
#   - Removed 'filt'. Merge function of 'filt' into 'dict_gen'
#   - 'dict_gen' arguments updated. 'replace_dict' added for text replacement
# 2015-03-22:
#   - Add POS tagging
#   - lemmatize based on tags (so fix the as->a error)
#   - Problem: All grammar types beside noun, verb, adjective, and adverb are
#             mapped to adjective in wordnet
# 2015-03-28:
#   - replace '\t' with '#######' in print_table

import nltk, re, pprint, string, math
from nltk.corpus import wordnet
#from nltk.stem.snowball import SnowballStemmer

# Normalizing text from http://www.nltk.org/book/ch03.html section 3.6
# - lower case
# - strip off affixes, also known as stemming OR
# - lemmatization (make sure words in dictionary)

# set to True for debug printing
DEBUG = 0

# keys of collective dictionary
# change this for better naming if necessary
__word_dict_key = 'WORDS'
__sent_dict_key = 'SENTS'
__hist_dict_key = 'HIST'

__wordnet_noun = wordnet.NOUN
__wordnet_verb = wordnet.VERB
__wordnet_adj = wordnet.ADJ
__wordnet_adv = wordnet.ADV
def get_dictionary():
    f = open("dict.txt","r")
    dictionary = f.read()
    dictionary = dictionary.split('\\\n')
    return dictionary

def dict_gen(raw_text, thres_down, thres_up, exclude_list, replace_dict, dictionary_words = True):
    """ Given raw text string, return a dictionary of dictionaries
        If returned dictionary has name 'dict' then use
            dict[__word_dict_key] to get word_dict
            dict[__sent_dict_key] to get sent_dict
            dict[__hist_dict_key] to get histogram
        raw_text     - raw text as a string
        thres_down   -least number of occurrence of word as fraction of total word count
        thres_up     - most number of occurrence of word as fraction of total word count
        exclude_list - list of words to exclude
        replace_dict - dictionary of words for replacement
                       e.g. to replace all 're' with 'are', replace_dict = {'re':'are'}
        dictionary_words - filter out all non-dicationry words
    """

    raw_text = raw_text.lower()
    sent_tokens = nltk.sent_tokenize(raw_text)
    word_tokens = [nltk.word_tokenize(st) for st in sent_tokens]

    # POS tagging
    word_tokens = nltk.tag.pos_tag_sents(word_tokens)

    # filtering exclude list
    word_tokens = [[w for w in sent if w[0] not in exclude_list] \
                      for sent in word_tokens]

    # filtering non-dictionary words
    if dictionary_words:
        OED = get_dictionary()
        word_tokens = [[w for w in sent if w[0] in OED] for sent in word_tokens]
        tmp = [j for i in word_tokens for j in i ]
        if tmp == []:
            return None

    # replacing words in replace
    word_tokens = [[w if w[0] not in replace_dict \
        else (replace_dict[w[0]],w[1]) for w in sent] for sent in word_tokens]

    # remove punctuation
    word_tokens = [[w for w in sent if w[0] not in string.punctuation] \
                for sent in word_tokens]

    # filtering words with occurrence out of range
    allwords = [w[0] for sublist in word_tokens for w in sublist]
    max_occurences = math.floor(len(allwords) * thres_up)
    min_occurences = math.ceil(len(allwords) * thres_down)
    words_in_range = [w for w in set(allwords) \
                        if min_occurences <= allwords.count(w) <= max_occurences]
    word_tokens = [[w for w in sent if w[0] in words_in_range] \
                      for sent in word_tokens]

    # remove empty sentences                
    word_tokens = [sent for sent in word_tokens if len(sent) > 0]
    if DEBUG: print "WORD TOKENS:\n",word_tokens

    # 3 popular stemmers
    #porter = nltk.PorterStemmer()
    #lancaster = nltk.LancasterStemmer()
    #snowball = SnowballStemmer("english", ignore_stopwords=True)
    #stemmed = [[porter.stem(t) for t in sent] for sent in word_tokens]
    #stemmed = [[lancaster.stem(t) for t in sent] for sent in word_tokens]
    #stemmed = [[snowball.stem(t) for t in sent] for sent in word_tokens]

    # use lemmatizer instead of stemmer
    wnl = nltk.WordNetLemmatizer()
    lmt = [[wnl.lemmatize(w[0],get_wordnet_pos(w[1])) \
            for w in sent] for sent in word_tokens]
    if DEBUG: print "LMT:\n",lmt
    if len(lmt) < 1:
        raise Exception('lemmatization error')
    if DEBUG:
        print "DEBUG:\n", lmt
        print word_tokens[1][11]

    # word -> [(sentence number, word position)]
    word_dict = {}
    # sentence number -> (sentence, starting word position)
    sent_dict = {}
    for i in xrange(0,len(lmt)):
        sent = lmt[i]
        # table 1
        for j in xrange(0,len(sent)):
            word = sent[j]
            if DEBUG: print word
            if word not in word_dict:
                word_dict[word] = [(i+1,j+1)]
            else:
                word_dict[word].append((i+1,j+1))
        # table 2
        if i == 0:
            sent_dict[i+1] = (sent,1) 
        else:
            sent_dict[i+1] = (sent,sent_dict[i][1]+len(sent_dict[i][0]))
    # word -> word count
    hist = {w:len(word_dict[w]) for w in word_dict}
    
    return {
        __word_dict_key: word_dict,
        __sent_dict_key: sent_dict,
        __hist_dict_key: hist
    }
    
def test():
    raw1 = """NLTK is a leading platform for building Python programs to
        work with human language data! It provides easy-to-use interfaces to
        over 50 corpora and lexical resources such as WordNet, along with a 
        suite of text processing libraries for classification, tokenization, 
        stemming, tagging, parsing, and semantic reasoning, and an active 
        discussion forum?"""
    raw2 = """De do do do, de da da da.
            Is all I want to say to you.
            De do do do, de da da da.
            Their innocence will pull me through.
            De do do do, de da da da.
            Is all I want to say to you.
            De do do do, de da da da.
            They're meaningless and all that's true."""
    exclude = ['da']
    replace = {"'re":'are', "'s":'is'}
    dict_test = dict_gen(raw2,0.0,0.2,exclude,replace)
    print_table(dict_test[__word_dict_key],'WORD DICT')
    print_table(dict_test[__sent_dict_key],'SENT DICT')
    print_table(dict_test[__hist_dict_key],'HISTOGRAM')

# Given table t and its name, print formatted table in console   
def print_table(t,name):
    print name, ':'
    for k in t.keys():
        print k, ':', t[k]

# map treebank tag to wordnet tag
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return __wordnet_adj
    elif treebank_tag.startswith('V'):
        return __wordnet_verb
    elif treebank_tag.startswith('N'):
        return __wordnet_noun
    elif treebank_tag.startswith('R'):
        return __wordnet_adv
    else:
        return __wordnet_adj # not sure if this will work for all cases

   
if __name__ == '__main__':
    test()
