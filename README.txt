Wavelets 
Michael Kellman, Matt Bauch, Raymond Xia

This is the readme for the code written for the class project.
This outlines the code governing the results of the project.
Please read the technical document for more infromation.

Important files:
	python/
		lgs.py
			creates Point-wise Mutual Information Graphs
		brown_test.py
			generates and saves training graphs and testing histograms. See first couple lines of script to fix the parameters.
		dict_gen.py
			parses and tokenizes articles into a usable list of words and returns dictionaries that are useful for graph generation
	matlab/
		hist_graph_classifier.m
			This script evaluates the main result of the project and can be ran to generate results. It handles reading in files, decomposing graphs, projecting graph signal on to decomposition, training SVM, tuning SVM, testing classifier, and cross validating results. See first couple lines of script to fix the parameters.
		bows_classifer.m
			This script evaluates the baseline results of the project. It implements a bag of words document classifcation algorithm. It handles reading in histograms, training Naive Bayes classifier, testing classifier, and cross validating results. See first couple lines of script to fix the parameters.
		display_top_vectors.m
			This is a function for viewing the first K primary dimensions of the N top eigenvectors of a graph after the fourier basis is computed.
		kfold.m
			Used to create partitions for cross validation
		sparse2mat.m / sparse2vect.m
			Reorders a spares matrix to the full matrix specified by dimensions.
	computation_results
		This is where the sparse matrices and spares histograms are saved generated in brown_test.py.

Dependencies: (Need to run code)
	NLTK: http://www.nltk.org/install.html. You need to install the library and the database for the corpa 
	SVMLIB: http://www.csie.ntu.edu.tw/~cjlin/libsvm/
	GSP: https://lts2research.epfl.ch/gsp/

To reproduce results:
	run brown_test.py (generates graphs and histograms, this are already generated)
	run bows_classifier.m (runs baseline bag of words)
	run hist_graph_classifier.m (runs our algorithm)