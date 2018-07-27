
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial import distance

from utility import save_model,load_model,write_to_file
from conf import GOOGLE_CLUSTER_PATH,GOOGLE_ENGLISH_WORD_PATH,GOOGLE_WORD_FEATURE
    

def hierarchical_cluster(centers,words):    
    
    to_merge = linkage(centers,method='average', metric='cosine')
    
    clusters = {}
    maxcluster =0
    print('len to_merge',len(to_merge))
    for i, merge in enumerate(to_merge):
        
        if merge[0] <= len(to_merge):

            a = centers[int(merge[0]) - 1]
            a=words[int(merge[0]) ]
        else:
          
            a = clusters[int(merge[0])]


        if merge[1] <= len(to_merge):
            b = words[int(merge[1])]

        else:
            b = clusters[int(merge[1])]

        distance=merge[2]
        count = merge[3]
        clusters[1 + i + len(to_merge)] = {
            'children' : [a, b],'distance':distance,'count':count
        }
        
        maxcluster=1 + i + len(to_merge)

    return clusters,maxcluster

def main():        
    """load the feature and cluster them by linkage.
    Record all the cluster tree and dump it.
    """
    words_set = load_model(GOOGLE_WORD_FEATURE)
    
    features=[]
    words=[]
    count = 0
    
    for word in words_set:
        v= words_set[word]
        if v is not None:
            features.append(v)
            words.append(word)
            count+=1
        
    clusters,maxcluster = hierarchical_cluster(features,words)
        
    #can not use json.dump
    txt =str(clusters[maxcluster])
    txt = txt.replace("'", '"')
    write_to_file(GOOGLE_CLUSTER_PATH, txt.encode(encoding='utf_8', errors='strict'), mode='wb+')

if __name__ == '__main__':
    main()