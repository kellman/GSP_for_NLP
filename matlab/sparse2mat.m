function [ M ] = sparse2mat( edges_sparse,dim )
% Given sparse matrix representation [row,col,val]
% and dimension of result square matrix
% create that matrix
M = zeros(dim);
M(sub2ind(size(M),edges_sparse(:,1)+1,edges_sparse(:,2)+1)) = edges_sparse(:,3);

end

