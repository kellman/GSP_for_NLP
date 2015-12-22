import nltk, re, pprint, string
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import brown, movie_reviews
from lgs import *

from math import *
from decimal import *

cat = brown.categories()
print cat

numTrain = 3000;
numTest = 100;

data1 = brown.sents(categories = cat[3])
data2 = brown.sents(categories = cat[10])
print len(data1)
print len(data2)


# create global dictionary of all words from both classes
# This gives global perspective over all of the words in the experiment so that
# each test instance can be easily projected on to each class graph.
data = [data1,data2]
sents_raw = [item for sublist in data for item in sublist]
print len(sents_raw)
total_raw = lump_array_to_string(sents_raw)
global_nodes = get_node_values(total_raw)

# look at data1
sents1 = lump_array_to_string(data1[0:numTrain])
sents1_test = lump_array_to_string(data1[numTrain:numTrain+numTest])
graph1 = class_graph_gen(sents1,global_nodes)

f = open('nodes1.txt','w')
[f.write(graph1[0][i] + " ") for i in xrange(0,len(graph1[0]))];
f.close()

f = open('edges1.csv','w')
[[f.write(str(graph1[1][i][j]) + " , ") for i in xrange(0,len(graph1[1]))] for j in xrange(0,len(graph1[1][0]))]
f.close()

print len(sents1)
print len(graph1)
print len(graph1[0][1])

# look at data2
sents2 = lump_array_to_string(data2[0:numTrain])
sents2 = lump_array_to_string(data2[numTrain:numTrain+numTest])
graph2 = class_graph_gen(sents2,global_nodes)

f = open('edges2.csv','w')
[[f.write(str(Graph[1][i][j]) + " , ") for i in xrange(0,len(Graph[1]))] for j in xrange(0,len(Graph[1][0]))]
f.close()



# print len(sents2)
# print len(graph2)
# print len(graph2[0][1])

# training data graph generation
# raw1 = lump_array_to_string()
# print raw1
# print filter(data1,xrange(0,numTrain))





# Movie Reviews
# data_pos = movie_reviews.categories()
# print data_pos
# print len(data_pos)

# print movie_reviews['pos']