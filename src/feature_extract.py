import gensim
from gensim.models import Word2Vec

from conf import GOOGLE_WORD2VEC_MODEL
from conf import GOOGLE_ENGLISH_WORD_PATH,GOOGLE_WORD_FEATURE
from utility import save_model

""" Word2vec extract from google pre-trained model
"""

def main():
    
    word_vectors = {}

    with open(GOOGLE_ENGLISH_WORD_PATH) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            if line:                
                word = line
                print(line)
                word_vectors[word]=None

    model = gensim.models.KeyedVectors.load_word2vec_format(GOOGLE_WORD2VEC_MODEL, binary=True) 
    
    for word in word_vectors:
        try:
            v= model.wv[word]
            word_vectors[word] = v
        except:
            pass
        
    save_model(word_vectors,GOOGLE_WORD_FEATURE)
    
if __name__ =='__main__':
    main()
