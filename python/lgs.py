# dict_gen.py
# Utility functions supporting graph construction

# Change Log:
# 2015-03-04: Complete dictionary 1 and 2 generation described in email given
# a raw string as input.
# Problem: some words become not readable

import nltk, re, pprint
from string import *
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

from math import *
from decimal import *
from multiprocessing import Pool

from dict_gen import *

# from sets import set

# Normalizing text from http://www.nltk.org/book/ch03.html section 3.6
# - lower case
# - strip off affixes, also known as stemming OR
# - lemmatization (make sure words in dictionary)


# set to True for debug printing
DEBUG = 1

# keys of collective dictionary
# change this for betting naming if necessary
__word_dict_key = 'WORDS'
__sent_dict_key = 'SENTS'
__hist_dict_key = 'HIST'


# calculates the PMI between two words
def PMI(w1,w2,word_dict,sent_dict):
    num_sents = len(sent_dict)

    loc1 = word_dict[w1]
    A = [a for (a,b) in loc1]
    s1 = frozenset(A)
    p_w1 = Decimal(len(s1))/Decimal(num_sents)

    loc2 = word_dict[w2]
    B = [a for (a,b) in loc2]
    s2 = frozenset(B)
    p_w2 = Decimal(len(s2))/Decimal(num_sents)

    p_w12 = Decimal(len(s1.intersection(s2)))/Decimal(num_sents)
    pmi = log(Decimal(p_w12)/Decimal(p_w1*p_w2))
    pmi = Decimal(pmi)/Decimal(log(2))
    # pmi = pmi + Decimal(10)
    return max(pmi,0.0)

# Gets all possible edges in sentence
def sent_edge_gen(sent_num,word_dict,sent_dict,window=6):
    # window = 6 optimal

    # gets sentence at sent_num
    sent = sent_dict[sent_num][0]

    Edges = []
    for i in xrange(0,len(sent)):
        for j in xrange(0,len(sent)):
            w1 = sent[i]
            w2 = sent[j]
            dist = abs(i-j)
            if w1 != w2 and dist < window:
                temp = [sorted([w1,w2]),dist]
                if temp not in Edges:
                    Edges.append(temp)
    return Edges

# computes/adds graph for one sentence to rest of essay's graph
def sent_graph_gen(sent_num,word_dict,sent_dict,nodes,verts):
    sent = sent_dict[sent_num][0]
    Edges = sent_edge_gen(sent_num,word_dict,sent_dict)

    # generates sentence edge matrix of size according to all words in piece
    # nodes = word_dict.keys()

    # print len(word_dict)
    # verts = [[0 for i in nodes] for j in nodes]

    for edge in Edges:

        # this ditches this edge if it isn't in the training global nodes
        # this is good it mains its position with respect to other word's distances.
        w1i = nodes.index(edge[0][0]) if edge[0][0] in nodes else None
        w2i = nodes.index(edge[0][1]) if edge[0][1] in nodes else None
        if ((w1i == None) or (w2i == None)):
            continue


        pmi = PMI(edge[0][0],edge[0][1],word_dict,sent_dict)
        dist2 = pow(edge[1],2)
        edge_wt = Decimal(1 + pmi)/Decimal(dist2)
        verts[w1i][w2i] = verts[w1i][w2i] + edge_wt
        verts[w2i][w1i] = verts[w2i][w1i] + edge_wt
    return [nodes, verts]


# wrapper so that it makes sense when I call it
def test_graph_gen(raw_text,global_nodes,global_dict):
    return class_graph_gen(raw_text,global_nodes,global_dict)


# computes class graph with edge matrix size of global nodes (all seen works in training corpus)
def class_graph_gen(raw_text,global_nodes,global_dict):
    exclude_list = stopwords.words('english')
    test_dict = dict_gen(raw_text,0,1,exclude_list,[])
    if test_dict == None:
        return None
    # now we use global nodes instead of test_dict words_list keys
    num_of_sentences = len(test_dict[__sent_dict_key])
    # print test_dict[__sent_dict_key]
    verts = [[0 for i in global_nodes] for j in global_nodes]
    PARTS = [global_nodes,verts]
    for i in xrange(1,num_of_sentences+1):
        PARTS = sent_graph_gen(i,test_dict[__word_dict_key],test_dict[__sent_dict_key],PARTS[0],PARTS[1])    # G = parts[0][1]
    # for i in xrange(1,num_of_sentences):
    #     G = add_graphs(parts[i][0],G,parts[i][0],parts[i][1])
    WEIGHTS = word_count(test_dict,global_dict)
    print len(PARTS), "PARTS"
    print len(WEIGHTS), "WEIGHTS"
    return (PARTS,WEIGHTS)

# this was a tester to create local graphs (not global class dictionaries)
def essay_graph_gen(raw_text):
    print raw_text
    exclude_list = stopwords.words('english')
    test_dict = dict_gen(raw_text,0,1,exclude_list,[])
    print test_dict
    # print_table(test_dict[__sent_dict_key],__sent_dict_key)
    # print_table(test_dict[__word_dict_key],__word_dict_key)
    num_of_sentences = len(test_dict[__sent_dict_key])
    # print test_dict[__sent_dict_key]
    nodes = test_dict[__word_dict_key].keys() 
    verts = [[0 for i in nodes] for j in nodes]
    PARTS = [nodes,verts]
    for i in xrange(1,num_of_sentences+1):
        PARTS = (sent_graph_gen(i,test_dict[__word_dict_key],test_dict[__sent_dict_key],PARTS[0],PARTS[1]))
    return PARTS



def lump_array_to_string(lot):
    text = ""
    for sent in lot:
        for word in sent:
            text = join([text,word]," ")
    return text

def get_node_values(test_dict):
    #exclude_list = stopwords.words('english')
    #test_dict = dict_gen(raw_text,0,1,exclude_list,[])
    return test_dict[__word_dict_key].keys()

def word_count(test_dict,global_dict):
    keys = global_dict[__word_dict_key].keys()
    result = [0] * len(keys)
    for i in xrange(0,len(keys)):
        if keys[i] in test_dict[__hist_dict_key]:
            result[i] = test_dict[__hist_dict_key][keys[i]]
    return result

def test():
    # raw = """NLTK is a leading platform for building Python programs to
    #     work with human language data! It provides easy-to-use interfaces to
    #     over 50 corpora and lexical resources such as WordNet, along with a 
    #     suite of text processing libraries for classification, tokenization, 
    #     stemming, tagging, parsing, and semantic reasoning, and an active 
    #     discussion forum?"""
    # raw = "I am a red dog. He is a weird long cat. Where is our green food? This is so fucked up. Matt green red dog"
    raw = "I am a red dog. Clifford is a red dog."
    PARTS = essay_graph_gen(raw);
    print PARTS


#     raw = """Once upon a time, while Brahmadatta was king of Benares, the Bodhisatta came to life at the foot of the Himalayas as a monkey. He grew strong and sturdy, big of frame, well to do, and lived by a curve of the river Ganges in a forest haunt. Now at that time there was a crocodile dwelling in the Ganges. The crocodile's mate saw the great frame of the monkey, and she conceived a longing to eat his heart. So she said to her lord, Sir, I desire to eat the heart of that great king of the monkeys!

# Good wife, said the crocodile, I live in the water and he lives on dry land. How can we catch him?

# By hook or by crook, she replied, he must be caught. If I don't get him, I shall die.

# All right, answered the crocodile, consoling her, don't trouble yourself. I have a plan. I will give you his heart to eat.

# So when the Bodhisatta was sitting on the bank of the Ganges, after taking a drink of water, the crocodile drew near, and said, Sir Monkey, why do you live on bad fruits in this old familiar place? On the other side of the Ganges there is no end to the mango trees, and labuja trees, with fruit sweet as honey! Is it not better to cross over and have all kinds of wild fruit to eat?

# Lord Crocodile, the monkey answered. The Ganges is deep and wide. How shall I get across?

# If you want to go, I will let you sit upon my back, and carry you over.

# The monkey trusted him, and agreed. Come here, then, said the crocodile. Up on my back with you! and up the monkey climbed. But when the crocodile had swum a little way, he plunged the monkey under the water.

# Good friend, you are letting me sink! cried the monkey. What is that for?

# The crocodile said, You think I am carrying you out of pure good nature? Not a bit of it! My wife has a longing for your heart, and I want to give it to her to eat.!

# Friend, said the monkey, it is nice of you to tell me. Why, if our heart were inside us, when we go jumping among the tree tops it would be all knocked to pieces!

# Well, where do you keep it? asked the crocodile.

# The Bodhisatta pointed out a fig tree, with clusters of ripe fruit, standing not far off. See, said he, there are our hearts hanging on yonder fig tree.

# If you will show me your heart, said the crocodile, then I won't kill you.

# Take me to the tree, then, and I will point it out to you.

# The crocodile brought him to the place. The monkey leapt off his back, and, climbing up the fig tree, sat upon it. Oh silly crocodile! said he. You thought that there were creatures that kept their hearts in a treetop! You are a fool, and I have outwitted you! You may keep your fruit to yourself. Your body is great, but you have no sense.

# And then to explain this idea he uttered the following stanzas:

# Rose-apple, jack-fruit, mangoes, too, across the water there I see;
# Enough of them, I want them not; my fig is good enough for me!
# Great is your body, verily, but how much smaller is your wit!
# Now go your ways, Sir Crocodile, for I have had the best of it. 
# The crocodile, feeling as sad and miserable as if he had lost a thousand pieces of money, went back sorrowing to the place where he lived.
# """

    

    # lot = [["hello","my","name","is","Matt","and","I","am","cool","."],["hello","I","Michael","."]]
    # raw = lump_array_to_string(lot)
    # Graph = essay_graph_gen(raw)

    # Writes graph to file so they can be read into MATLAB
    # f = open('nodes.txt','w')
    # [f.write(Graph[0][i] + " ") for i in xrange(0,len(Graph[0]))];
    # f.close()

    # f = open('edges.csv','w')
    # [[f.write(str(Graph[1][i][j]) + " , ") for i in xrange(0,len(Graph[1]))] for j in xrange(0,len(Graph[1][0]))]
    # f.close()


def print_table(t,name):
    print name, ':'
    for k in t.keys():
        print '\t', k, ':', t[k]


    # test_dict = dict_gen(raw)
    # print test_dict[__word_dict_key]

    # [nodes,verts1] =  sent_graph_gen(1,test_dict[__word_dict_key],test_dict[__sent_dict_key])

    # print verts1
    # [nodes,verts2] =  sent_graph_gen(2,test_dict[__word_dict_key],test_dict[__sent_dict_key])
    # [nodes,verts3] =  sent_graph_gen(3,test_dict[__word_dict_key],test_dict[__sent_dict_key])

    # print add_graphs(nodes,add_graphs(nodes,verts1,nodes,verts2),nodes,verts3)

    # print PMI("cat","is",test_dict[__word_dict_key],test_dict[__sent_dict_key])
    # print sent_graph_gen(1,test_dict[__word_dict_key],test_dict[__sent_dict_key])
    
if __name__ == '__main__':
    test()


# def add_graphs(nodes1,verts1,nodes2, verts2):
#     # nodes1 and nodes2 must be equal and verts1 and verts2 must be same dimension

#     output = [[0 for i in verts1] for j in verts1[0]]
#     if nodes1 == nodes2:
#         for i in xrange(1,len(verts1)):
#             for j in xrange(1,len(verts1[0])):
#                 output[i][j] = verts1[i][j] + verts2[i][j]
#     return output
