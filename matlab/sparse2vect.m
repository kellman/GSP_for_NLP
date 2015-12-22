function [ M ] = sparse2vect( edges_sparse,dim )
% Given sparse matrix representation [row,col,val]
% and dimension of result square matrix
% create that matrix
M = zeros(dim,1);
M(edges_sparse(:,1) + 1) = edges_sparse(:,2);

end

