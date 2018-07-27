import os
import shutil
import json
from utility import write_to_file,load_model
from scipy.cluster.hierarchy import dendrogram, linkage
from conf import GOOGLE_CLUSTER_PATH,OID_SAVE_FOLDER,GOOGLE_CLUSTER_FLAT_PATH,\
    CHECKED_OID_SAVE_FOLDER,GOOGLE_WORD_FEATURE
try:
    import matplotlib.pyplot as pyplot
except :
    pyplot = None
    print('Warning:Can not import pyplot')

knowoidgroup={'12112222222222222222222222222222222222222222222222222222222222222222222122222222222222222222':'people_names',
              '1111':'economy',
              '1211122':'electtonic',
              '11222':'verb',
              '121122222222222222222222222222222222222222222222222221':'electornic_digital',
              '12112222222222222222222222222222222222222222222222222222221':'werid',
              '111212':'political',
              '122111':'editor',
              '121222221':'food_drink_animal',
              '11221':'phiysics',
              '122212':'music',
              '12122212':'cemestry',
              '121222222211':'clothes',
              '122211':'zongjiao',
              '122221':'guojia',
              '1211222222222222222222222222222222222222222222222221':'weird',
              '12112222222222222222222222222222222222222222222222222222222222222222222122222222222222221':'city',
              '121122222222222222222222222222222222222222222222222222222222222222222221222222222222222221':'usa city',
              '1211222222222222222222222222222222222222222222222222222222222222222222211':'guo jia'
              ,'1211222222222222222222222222222222222222222222222222221':'qi che',
              '121122222222222222222222222222222222222222222222222222222221':'ala bo',
              '121122222222222222222222222222222222222221':'unkow',
              '12112222222222222222222222222222222222221':'yi yao',
              '121122222222222222222222222222222222222222222222222222222222222222222222':'ri qi',
              '12112222222222222222222222222222222222222222222222222222222222222222222122222222221':'univercity',
              '122222221':'workers',
              '121122222221':'olympic',
              '1211222222222221':'time',
              '12112222222222221':'weird',
              '1211222222222222222222222222221':'unit',
              '12112222222222222222222222222222222222222222222221':'region',
              '121122222222222222222222222222222222222222222222221':'region',
              '121122222222222222222222222222222222222222222222222222221':'region',
              '1211222222222222222222222222222222222222222222222222222222222222222222212221':'news',
              '1222221':'help',
              '111221':'staff',
              '1121111':'experiment',
              '1211121':'zhi shi chang quan',
              '1212211':'jiao tong gong ju',
              '11211122':'quantity',
              '11211211':'creation',
              '11211211':'water',
              '11211211':'di qu lv you',
              '11211211':'body weapon',
              '11211211':'medical',
              '11211211':'opinion',
              '11211211':'zu cheng',
              '11211211':'sex and married',
              '11211211':'whether',
              '11211211':'people',
              '11211211':'education',
              '11212222211':'time relation and cheng du ',
              '11212222222':'big small',
              '12122222222':'bed house',
              '112122222121':'duo shao xiang tong bu tong',
              '112122222211':'personal ability',
              '112122222212':'personality',
              '121222222212':'da yin da bao',
              '1121222221221':'jia she ren wei zhuang tai',
              '12112222222221':'contact ',
              '112122222122221':'suoyou xu ci',
              '12112222222222222221':'zhong guo',
              '121122222222222222222222222222222222222222222222222222222222222222222221222222221':'yu qi ci',
              '12121':'angle '
              }

def draw_cluster_tree(words_list,savefigpath):

    if pyplot is None:
        print('Can not drwa cluster tree pyplot is not ok')
    if len(words_list) > 1000:
        print('so much words')
        return
        
    if os.path.exists(savefigpath):
        return
    
    words_model = load_model(GOOGLE_WORD_FEATURE)

    features=[]
    words=[]
    count = 0
    for word in words_list:
        v= words_model[word]
        if v is not None:
            features.append(v)
            words.append(word)
            count+=1

    to_merge = linkage(features,method='average', metric='cosine')
    
    leaf_font_size = 25
    if len(words_list) > 300:
        pyplot.figure(figsize=(30, 250))   
    elif len(words_list) > 150:
        leaf_font_size = 30
        pyplot.figure(figsize=(30, 150))   
    elif len(words_list) > 100:
        leaf_font_size = 30
        pyplot.figure(figsize=(30, 100))   
    elif len(words_list) > 50:
        pyplot.figure(figsize=(30, 40))   
    else:
        pyplot.figure(figsize=(30, 30))     
    
    dendrogram(to_merge,labels=words,orientation='right',leaf_font_size=leaf_font_size)   #distance_sort
    pyplot.title('Hierarchical Clustering Dendrogram')

    pyplot.savefig(savefigpath)

def split_tree(root,clsid):
    
    if type(root) is not dict:
        return
    
    count= root['count']  

    if clsid in knowoidgroup :
        
        txt=json.dumps(root,indent=4)
 
        write_to_file(os.path.join(CHECKED_OID_SAVE_FOLDER,'{}.json'.format(clsid)),
                       txt.encode(encoding='utf_8', errors='strict'), 
                       mode='wb+')        
        return
    
    if count < OID_NODE_MAX_COUNT:   
        #dump the tree to file if count < OID_NODE_MAX_COUNT     
        
        if count < 4:
            return
        
        txt=json.dumps(root,indent=4)
 
        write_to_file(os.path.join(OID_SAVE_FOLDER,'{}.json'.format(clsid)),
                       txt.encode(encoding='utf_8', errors='strict'), 
                       mode='wb+')

        return
    
    left,right = root['children'] 
    
    oid = '{}1'.format(clsid)
    split_tree(left,oid)   
    
    oid = '{}2'.format(clsid)
    split_tree(right,oid)
    
def run_split_tree():
    
    path = GOOGLE_CLUSTER_PATH
    
    if os.path.exists(OID_SAVE_FOLDER):
        shutil.rmtree(OID_SAVE_FOLDER)
        
    os.mkdir(OID_SAVE_FOLDER)
    
    with open(path) as f:
        data = json.load(f)
        rootid = '1'
        split_tree(data,rootid)
        
def get_children(root,v):
    "get leaf word"
    if type(root) is dict:
        left ,right = root['children']
        get_children(left,v)
        get_children(right,v)
    else:
        v.append(root)
        
        
def dump_flat_result(oidpath,flatsavepath):    
    
    write_to_file(flatsavepath, ''.encode(encoding='utf_8', errors='strict'),mode='wb+')
    for filename in os.listdir(oidpath):
        fullname = os.path.join(oidpath,filename)
        if filename.endswith('.json'):
            print(fullname)
            with open(fullname,encoding='utf-8') as f:
                data = json.load(f)
                v=[]
                get_children(data,v)
                txt = ' '.join(v)
                txt+='\n'
                txt=filename+"\t"+str(len(v))+"\t"+txt
                write_to_file(flatsavepath, txt.encode(encoding='utf_8', errors='strict'))
                fullname = fullname.replace('.json','')
                draw_cluster_tree(v, fullname+'.pdf')
            
            

OID_NODE_MAX_COUNT = 700 
OID_NODE_MAX_COUNT = 600
OID_NODE_MAX_COUNT = 500
OID_NODE_MAX_COUNT = 377
OID_NODE_MAX_COUNT = 300
OID_NODE_MAX_COUNT = 335
OID_NODE_MAX_COUNT = 300
OID_NODE_MAX_COUNT = 230

def main():
    
#     run_split_tree()
#     dump_flat_result(OID_SAVE_FOLDER,GOOGLE_CLUSTER_FLAT_PATH)
    dump_flat_result(CHECKED_OID_SAVE_FOLDER,GOOGLE_CLUSTER_FLAT_PATH)
    
if __name__ =='__main__':
    main()
    

