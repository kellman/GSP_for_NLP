clear
addpath '../computation_results/'
%% Naive Bayes and SVM train/test
% total number of testing articles
numTest = 300;
% number of category classes
numClass = 3;
% number of training instances to train on 
perTrain = 200;
% numer of testing instances to test on
perTest = 100;

%% read in global nodes and global graph
f = fopen('../computation_results/global_node.txt','r');
global_nodes = textscan(f,'%s'); 
fclose(f);
edges_sparse = csvread('../computation_results/global_edges.csv');
global_edges = sparse2mat(edges_sparse,size(global_nodes{1},1));

%% read in all test graphs and histograms
test_wts = cell(numClass,numTest);
test_size = zeros(numClass,numTest);
for i = 1:numClass
    for j = 1:numTest
        file1 = strcat('../computation_results/weight_',num2str(i),'_',num2str(j-1),'.csv');
        f = dir(file1);
        if (f.bytes == 0),
            test_wts{i,j} = zeros(size(global_nodes{1},1),1);
            disp('Im empty');
        else
            edge_sparse = csvread(file1);
            test_size(i,j) = size(edge_sparse,1);
            test_wts{i,j} = sparse2vect(edge_sparse,size(global_nodes{1},1));
        end
    end
end
%% Reorder histograms (flatten)
train_class = zeros(size(global_nodes{1},1),numTest*numClass);
for i = 1:numClass
    for j = 1:numTest
        x = (i-1)*numTest + j;
        train_class(:,x) = test_wts{i,j};
    end
end

%% normalize data
% train_class = bsxfun(@minus, train_class, mean(train_class,2));
% train_class = bsxfun(@rdivide, train_class, std(train_class,[],2));

%% Train on k sets (divide data using KFold)
class_labels = ones(numTest*numClass,1);
class_labels(numTest + 1:2*numTest) = 2;
class_labels((2*numTest) + 1:3*numTest) = 3;

% L = 20;
% % sigma = linspace(.05,2,L);
% % gamma = (1./sigma).^2;
% gamma = linspace(1/size(train_class,1),L/size(train_class,1),L);
% sigma = sqrt(1./gamma);
K = 30;

results = zeros(K,1);

% for l = 1:L
% l = 1;
% params = sprintf('-t 2 -b 1 -g %f',gamma(l));
for i = 1:K
    [testingInd,trainingInd] = kfold(class_labels,K,i);
    %% training data
    trainData = train_class(:,trainingInd);
    trainLabel = class_labels(trainingInd);
    NB = fitNaiveBayes(trainData',trainLabel,'Distribution','mn');

    %% testing data
    testData = train_class(:,testingInd);
    testLabel = class_labels(testingInd);
    predicted_label= NB.predict(testData');
    results(i) = sum(predicted_label == testLabel) / length(testLabel);
end
% end

% output of parameter tuning
m = mean(results)
s = std(results)

%% Display results
% figure
% subplot 211
% plot(gamma,m,'bs-');
% ylim([55 75]);
% xlabel('Gamma (RBF Kernel parameter)'); ylabel('Average classification accuracy (%)');
% title('Average accuracy (%) vs. Kernel gamma');
% 
% subplot 212
% plot(gamma,s,'bs-');
% xlabel('Gamma (RBF Kernel parameter)'); ylabel('Standard deviation classification accuracy (%)');
% title('Standard deviation (%) vs. Kernel gamma');
% %% Error bar
% figure
% errorbar(gamma,m,s);
