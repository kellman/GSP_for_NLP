function [] = display_top_vectors(words,E,N,K)
    for i = 0:K-1
        display_word_vector(words,E(:,end-i),N)
    end
end