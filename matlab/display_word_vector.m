function [] = display_word_vector(nodes,weights,N)
    [~,I] = sort(abs(weights));
    I = flipud(I);
    result = '';
    for i = 1:N
        result  = strcat(result,' ',nodes(I(i)) ,'<-->', num2str(abs(weights(I(i)))),' ');
    end
    result
end