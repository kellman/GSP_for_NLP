import nltk, re, pprint, string
from nltk.corpus import reuters, brown
from lgs import *
from math import *
from decimal import *

import os


# change this to your folder directory
__save_dir__ = "../computation_results/"

# This generates a testing graph and a histogram of words in article. Then saves it to sparse files.
def gen_test_graphs(para,numTest,class_ind,global_nodes, start_ind,global_dict):
    l = start_ind
    i = 0
    print numTest, i
    while i < numTest:
    	print i,l-start_ind
    	current = para[l]
    	current = [item for sublist in current for item in sublist] 
    	raw1 = " ".join(current)
        test_graphs = test_graph_gen(raw1,global_nodes,global_dict)
        l = l + 1
        if test_graphs == None:
            print 'None after dict_gen'
            continue
        test_graph = test_graphs[0]
        if all(v == 0 for values in test_graph[1] for v in values):
            print 'All zeros in graph'
            continue
        
        print "##################"
        print len(test_graphs[1])
        print "##################"
        # write edge matrix to file
        with open(__save_dir__+"edge_"+str(class_ind)+"_"+str(i)+".csv","w") as edges_file:
            for j in xrange(0,len(test_graph[1])):
                for k in xrange(0,len(test_graph[1][0])):
                    num = test_graph[1][j][k]
                    if num: # write only nonzero numbers
                        edges_file.write(str(j)+","+str(k)+","+str(num)+"\n")
        
        # write weights to file
        word_counts = test_graphs[1]
        with open(__save_dir__+"weight_"+str(class_ind)+"_"+str(i)+".csv","w") as weights_file:
            for j in xrange(0,len(word_counts)):
                if word_counts[j]:
                    weights_file.write(str(j)+","+str(word_counts[j])+"\n")
        i = i + 1
    return	


# print reuters.categories()

print brown.categories()

# print brown.sents(categories=['editorial'])[2]
print len(brown.paras(categories=['romance']))
print len(brown.paras(categories=['news']))
print len(brown.paras(categories=['government']))

# number from each class the global graphs is computed for
numTrain = 100
# number of testing article graphs computed
numTest = 150
# number of classes to compute over (this is hard coded in)
numClasses = 3


# classes choosen
cat1_para = brown.paras(categories=['romance'])
cat2_para = brown.paras(categories=['news'])
cat3_para = brown.paras(categories=['government'])

# compute global graph
cat1 = cat1_para[0:numTrain]
cat2 = cat2_para[0:numTrain]
cat3 = cat3_para[0:numTrain]

cat1raw = [i for sublist in cat1 for item in sublist for i in item] 
raw1 = " ".join(cat1raw);

cat2raw = [i for sublist in cat2 for item in sublist for i in item] 
raw2 = " ".join(cat2raw);

cat3raw = [i for sublist in cat3 for item in sublist for i in item] 
raw3 = " ".join(cat3raw);

total = [raw1,raw2,raw3];
total = " ".join(total);
exclude_list = stopwords.words('english')
global_dicts = dict_gen(total,0,1,exclude_list,[])
global_nodes= get_node_values(global_dicts);
print len(global_dicts)
print len(global_nodes)
graph_and_weights = class_graph_gen(total,global_nodes,global_dicts)
graph = graph_and_weights[0]
weights = graph_and_weights[1]

# write global nodes for class i
with open(__save_dir__+"global_node.txt","w") as nodes_file:
    for j in xrange(0,len(graph[0])):
        nodes_file.write(graph[0][j]+"\n")
# write sparse representation of edge matrix of global nodes for class i
with open(__save_dir__+"global_edges.csv","w") as edges_file:
    for j in xrange(0,len(graph[1])):
        for k in xrange(0,len(graph[1][0])):
            num = graph[1][j][k]
            if num: # write only nonzero numbers
                edges_file.write(str(j)+","+str(k)+","+str(num)+"\n")
print 'computed and saved global graphs'



# class 1
gen_test_graphs(cat1_para,numTest,1,global_nodes,numTrain,global_dicts)
print 'class 1 computed and saved'

# class 2
gen_test_graphs(cat2_para,numTest,2,global_nodes,numTrain,global_dicts)
print 'class 2 computed and saved'

# class 3
gen_test_graphs(cat3_para,numTest,3,global_nodes,numTrain,global_dicts)
print 'class 3 computed and saved'
