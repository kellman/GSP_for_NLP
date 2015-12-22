import nltk, re, pprint, string
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import brown, movie_reviews
from lgs import *

from math import *
from decimal import *

import os

# Set to True for debug printing
DEBUG = 0

numTrain = 20;
numClasses = 3;
numTest = 10;
# train on first 20 and test on last 10

<<<<<<< Updated upstream
# Process all data
fileids = ["./data/US/politics_us_","./data/Sports/sports_",\
    "./data/Business/business_"];
cum_data = [{},{},{}]
global_nodes = {}

# Process training class
for i in xrange(0,numClasses):
    # read raw data
    for count in xrange(1,31):
        with open(fileids[i]+str(count)+".txt","r") as myfile:
            data = myfile.read()
        cum_data[i][count] = data.decode('utf-8').encode("ascii", "ignore")
    # get and process all training data
    train_data = [cum_data[i][j] for j in xrange(1,numTrain+1)]
    train_data = " ".join(train_data)
    glob_nodes = get_node_values(train_data)
    global_nodes[i] = glob_nodes
    graph = class_graph_gen(train_data,glob_nodes)
    # write global nodes for class i
    with open(fileids[i]+"nodes"+".txt","w") as nodes_file:
        for j in xrange(0,len(graph[0])):
            nodes_file.write(graph[0][j]+"\n")
    # write sparse representation of edge matrix of global nodes for class i
    with open(fileids[i]+"edges"+".csv","w") as edges_file:
        for j in xrange(0,len(graph[1])):
            for k in xrange(0,len(graph[1][0])):
                num = graph[1][j][k]
                if num: # write only nonzero numbers
                    edges_file.write(str(j)+","+str(k)+","+str(num)+"\n")

# get and process each testing data
for i in xrange(0,numClasses):
    for j in xrange(numTrain+1, numTrain+numTest+1):
        if DEBUG:
            print (fileids[i] + str(j) + ":")
<<<<<<< Updated upstream
            print i,j
        test_data = cum_data[i][j]
        for m in xrange(0,numClasses):
            graph = test_graph_gen(test_data,global_nodes[m])
            with open(fileids[i] + str(j) + '_testclass'+str(m+1)+\
                '_edges.csv','w') as edges_file:
                for k in xrange(0,len(graph[1])):
                    for l in xrange(0,len(graph[1][0])):
                        num = graph[1][k][l]
                        if num:
                            edges_file.write(str(k)+","+str(l)+","+\
                                str(num)+"\n")
=======
            print len(graph[0])
            print len(graph[1])
        with open(fileids[i] + str(j) + '_testclass'+str(i)+'_edges.csv','w')\
         as edges_file:
            for k in xrange(0,len(graph[1])):
                for l in xrange(0,len(graph[1][0])):
                    num = graph[1][k][l]
                    if num:
                        edges_file.write(str(k)+","+str(l)+","+str(num)+"\n")
=======
# class 1
fileids = "./data/US/politics_us_"
cum_data_1 = {}
for count in xrange(1,31):
    with open(fileids+str(count)+".txt","r") as myfile:
        data = myfile.read()
        cum_data_1[count] = data.decode('utf-8').encode("ascii", "ignore")

# class 2
fileids = "./data/Sports/sports_"
cum_data_2 = {}
for count in xrange(1,31):
    with open(fileids+str(count)+".txt","r") as myfile:
        data = myfile.read()
        cum_data_2[count] = data.decode('utf-8').encode("ascii", "ignore")

# class 3
fileids = "./data/Business/business_"
cum_data_3 = {}
for count in xrange(1,31):
    with open(fileids+str(count)+".txt","r") as myfile:
        data = myfile.read()
        cum_data_3[count] = data.decode('utf-8').encode("ascii", "ignore")



# training class1
data = [cum_data_1[i] for i in xrange(1,numTrain+1)]
print len(data)
total_data = ""
for arts in data:
	total_data += arts

global_nodes = get_node_values(total_data)
graph1 = class_graph_gen(total_data,global_nodes)

f = open('nodes1.txt','w')
[f.write(graph1[0][i] + " ") for i in xrange(0,len(graph1[0]))];
f.close()

f = open('edges1.csv','w')
[[f.write(str(graph1[1][i][j]) + " , ") for i in xrange(0,len(graph1[1]))] for j in xrange(0,len(graph1[1][0]))]
f.close()

# test
fileids = "./data/US/politics_us_"
for i in xrange(numTrain + 1,numTrain + numTest + 1):
	data = cum_data_1[i]
	test_graph = test_graph_gen(data,global_nodes)
	print len(test_graph[0])
	print len(test_graph[1])
	f = open(fileids + str(i) + 'testclass1_edges.csv','w')
	[[f.write(str(test_graph[1][i][j]) + " , ") for i in xrange(0,len(graph1[1]))] for j in xrange(0,len(graph1[1][0]))]
	f.close()

for i in xrange(numTrain + 1,numTrain + numTest + 1):
	data = cum_data_2[i]
	test_graph = test_graph_gen(data,global_nodes)
	print len(test_graph[0])
	print len(test_graph[1])
	f = open(fileids + str(i) + 'testclass2_edges.csv','w')
	[[f.write(str(test_graph[1][i][j]) + " , ") for i in xrange(0,len(graph1[1]))] for j in xrange(0,len(graph1[1][0]))]
	f.close()

for i in xrange(numTrain + 1,numTrain + numTest + 1):
	data = cum_data_3[i]
	test_graph = test_graph_gen(data,global_nodes)
	print len(test_graph[0])
	print len(test_graph[1])
	f = open(fileids + str(i) + 'testclass3_edges.csv','w')
	[[f.write(str(test_graph[1][i][j]) + " , ") for i in xrange(0,len(graph1[1]))] for j in xrange(0,len(graph1[1][0]))]
	f.close()



# training class2
data = [cum_data_2[i] for i in xrange(1,numTrain+1)]
print len(data)
total_data = ""
for arts in data:
	total_data += arts

global_nodes = get_node_values(total_data)
graph2 = class_graph_gen(total_data,global_nodes)

f = open('nodes2.txt','w')
[f.write(graph2[0][i] + " ") for i in xrange(0,len(graph2[0]))];
f.close()

f = open('edges2.csv','w')
[[f.write(str(graph2[1][i][j]) + " , ") for i in xrange(0,len(graph2[1]))] for j in xrange(0,len(graph2[1][0]))]
f.close()

# test
fileids = "./data/Sports/sports_"
for i in xrange(numTrain + 1,numTrain + numTest + 1):
	data = cum_data_1[i]
	test_graph = test_graph_gen(data,global_nodes)
	print len(test_graph[0])
	print len(test_graph[1])
	f = open(fileids + str(i) + 'testclass1_edges.csv','w')
	[[f.write(str(test_graph[1][i][j]) + " , ") for i in xrange(0,len(graph2[1]))] for j in xrange(0,len(graph2[1][0]))]
	f.close()

for i in xrange(numTrain + 1,numTrain + numTest + 1):
	data = cum_data_2[i]
	test_graph = test_graph_gen(data,global_nodes)
	print len(test_graph[0])
	print len(test_graph[1])
	f = open(fileids + str(i) + 'testclass2_edges.csv','w')
	[[f.write(str(test_graph[1][i][j]) + " , ") for i in xrange(0,len(graph2[1]))] for j in xrange(0,len(graph2[1][0]))]
	f.close()

for i in xrange(numTrain + 1,numTrain + numTest + 1):
	data = cum_data_3[i]
	test_graph = test_graph_gen(data,global_nodes)
	print len(test_graph[0])
	print len(test_graph[1])
	f = open(fileids + str(i) + 'testclass3_edges.csv','w')
	[[f.write(str(test_graph[1][i][j]) + " , ") for i in xrange(0,len(graph2[1]))] for j in xrange(0,len(graph2[1][0]))]
	f.close()


# training class3
data = [cum_data_3[i] for i in xrange(1,numTrain+1)]
print len(data)
total_data = ""
for arts in data:
	total_data += arts

global_nodes = get_node_values(total_data)
graph3 = class_graph_gen(total_data,global_nodes)

f = open('nodes3.txt','w')
[f.write(graph3[0][i] + " ") for i in xrange(0,len(graph3[0]))];
f.close()

f = open('edges3.csv','w')
[[f.write(str(graph3[1][i][j]) + " , ") for i in xrange(0,len(graph3[1]))] for j in xrange(0,len(graph3[1][0]))]
f.close()

# test
fileids = "./data/Business/business_"
for i in xrange(numTrain + 1,numTrain + numTest + 1):
	data = cum_data_1[i]
	test_graph = test_graph_gen(data,global_nodes)
	print len(test_graph[0])
	print len(test_graph[1])
	f = open(fileids + str(i) + 'testclass1_edges.csv','w')
	[[f.write(str(test_graph[1][i][j]) + " , ") for i in xrange(0,len(graph3[1]))] for j in xrange(0,len(graph3[1][0]))]
	f.close()

for i in xrange(numTrain + 1,numTrain + numTest + 1):
	data = cum_data_2[i]
	test_graph = test_graph_gen(data,global_nodes)
	print len(test_graph[0])
	print len(test_graph[1])
	f = open(fileids + str(i) + 'testclass2_edges.csv','w')
	[[f.write(str(test_graph[1][i][j]) + " , ") for i in xrange(0,len(graph3[1]))] for j in xrange(0,len(graph3[1][0]))]
	f.close()

for i in xrange(numTrain + 1,numTrain + numTest + 1):
	data = cum_data_3[i]
	test_graph = test_graph_gen(data,global_nodes)
	print len(test_graph[0])
	print len(test_graph[1])
	f = open(fileids + str(i) + 'testclass3_edges.csv','w')
	[[f.write(str(test_graph[1][i][j]) + " , ") for i in xrange(0,len(graph3[1]))] for j in xrange(0,len(graph3[1][0]))]
	f.close()



>>>>>>> Stashed changes
>>>>>>> Stashed changes



