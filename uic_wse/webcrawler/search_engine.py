
from collections import defaultdict
from collections import Counter
import math
import pickle
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import heapq
import pathlib


stemmer = PorterStemmer()
stop_words = stopwords.words("english")

def tokenize_query(query):

    words = []
    regex_EXP = re.compile(r'[^\W\d]+')
    word_match=regex_EXP.finditer(query)
    
    for i in word_match:
        words.append(i.group())
    trimmed_words = []
    for word in words:
        if len(word)!=1 and len(word)!=2:
            trimmed_words.append(word.lower())
    query_tokens = [
            stemmer.stem(token)
            for token in trimmed_words
            if (token not in stop_words and stemmer.stem(token) not in stop_words)
        ]
    return query_tokens

def cosine_similarity(top_n,webpages_tokens,query_tokens,df,urls):
    doc_length = {}
    for key_i,value_i in webpages_tokens.items():
        tf = Counter(value_i)
        doc_l = 0
        for key_j,value_j in tf.items():
            div_l = len(webpages_tokens)/len(df[key_j])
            idf_l = math.log(div_l,2)
            weight = value_j*idf_l
            doc_l += weight*weight
        doc_length[key_i] = math.sqrt(doc_l)
    cosine_sim = {}
    for key_i,value_i in webpages_tokens.items():
        sumx = 0
        if doc_length[key_i]==0:
            continue
        for word in query_tokens:
            if len(df[word])==0:
                continue
            div = len(webpages_tokens)/len(df[word])
            idf = math.log(div,2)
            term_f = value_i.count(word)
            sumx += term_f*idf*idf

        cosine_sim[key_i] = sumx/doc_length[key_i]

    keys = list(cosine_sim.keys())
    values = list(cosine_sim.values())
    vals = [-val for val in values]
    heapq.heapify(vals)
    top_most = []
    # print(abs(-heapq.heappop(vals)))
    for _ in range(top_n):
        top = abs(-heapq.heappop(vals))
        index_page = values.index(top)
        if urls.get(int(keys[index_page])):
            top_most.append(urls.get(int(keys[index_page])))

    return top_most

def return_links(query):
    query_tokens = tokenize_query(query)

    current_path = pathlib.Path(__file__)
    pickel_folder = current_path.parent / "pickle_files"
    file1 = pickel_folder / "6000_pages_crawled.pickle"
    file2 = pickel_folder / "6000_inverted_index.pickle"
    file3 = pickel_folder / "6000_webpages_tokens.pickle"

    webpages_tokens = {}
    urls = {}
    df = {}
    #     # folder to store pickle files
    # pickle_folder = "./pickle_files/"
    # os.makedirs(pickle_folder, exist_ok=True)

        # Loading web page tokens from pickle files
    with open(file3, "rb") as f:
        webpages_tokens = pickle.load(f)

    # loading inverted index from pickle files
    with open(file2, "rb") as f:
        df = pickle.load(f)

    # loading urls mapper from pickle files
    with open(file1, "rb") as f:
        urls = pickle.load(f)

    links = cosine_similarity(10,webpages_tokens,query_tokens,df,urls)


    return links



















#Retrieves the top most relevant documents having the highest similarity scores to the query
 

