function [testIndices,trainIndices] = kfold(y,K,i)
%KFOLD Split unlabeled training data into K even groups
%   y               - n*1 class labels
%   K               - number of groups
%   i               - index of group to return as test data, (1 to K)
%   testIndices     - indices of examples for testing
%   trainIndices    - indices of examples for training

isrow = length(y) == size(y,2);
y = y(:);
labels = unique(y);
Nlabels = length(labels);

testIndices = [];
for li = 1:Nlabels
    labelIndices = find(y == labels(li));
    N = length(labelIndices);
    Ngroup = floor(N/K);
    Nextra = mod(N,K);
    
    i0 = (i-1) * Ngroup;
    if i <= Nextra
        i0 = i0 + i;
    else
        i0 = i0 + Nextra + 1;
    end
    i1 = i0 + Ngroup - 1;
    if i <= Nextra
        i1 = i1 + 1;
    end
    testIndices = [testIndices; labelIndices(i0:i1)];
end
trainLogical = true(size(y));
trainLogical(testIndices) = false;
trainIndices = find(trainLogical);

if isrow
    testIndices = testIndices';
    trainIndices = trainIndices';
end
end

