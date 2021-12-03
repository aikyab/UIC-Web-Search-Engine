# load dependency libraries
import re
import pickle
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import defaultdict
from collections import Counter
import pathlib

from os import listdir
from os.path import isfile, join


stop_words = stopwords.words("english")

stemmer = PorterStemmer()

query = "College of nursing"


# folder name storing downloaded web pages
current_path = pathlib.Path(__file__)
documents = current_path.parent / "docs_retrieved"
only_files = [f for f in listdir(documents) if isfile(join(documents, f))]



def tag_visible(element):
    if element.parent.name in ["style", "script", "head", "meta", "[document]"]:
        return False

    elif isinstance(element, Comment):
        return False

    elif re.match(r"[\s\r\n]+", str(element)):
        return False
    else:
        return True

# function to simply return all text information from html page
def get_text_from_code(page):
    soup = BeautifulSoup(page, "html.parser")

    text_in_page = soup.find_all(text=True)

    visible_text = filter(tag_visible, text_in_page)
    return " ".join(term.strip() for term in visible_text)

# dict to store tokens in each web page
webpage_tokens = {}


for file in only_files:
    with open(documents / str(file),encoding="latin-1") as f:
        # web_page = open(pages_folder + file, "r", encoding="utf-8")
        code = f.read()

        text = get_text_from_code(code)
        text = text.lower()

        text = re.sub("[^a-z]+", " ", text)
        tokens = text.split()

        clean_stem_tokens = [
            stemmer.stem(token)
            for token in tokens
            if (token not in stop_words and stemmer.stem(token) not in stop_words)
            and len(stemmer.stem(token)) > 2
        ]
        webpage_tokens[file] = clean_stem_tokens

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

def df_calc(webpages_tokens):
    df = defaultdict(list)
    for key,value in webpages_tokens.items():
        for word in value:
            if key not in df[word]:
                df[word].append(key)
    return df

inverted_index = df_calc(webpage_tokens)

# pickling inverted index and web page tokens

current_path = pathlib.Path(__file__)
pickle_folder = current_path.parent / "pickle_files"

webpage_tokens_pickle = pickle_folder / "3000_webpages_tokens.pickle"

inverted_index_pickle = pickle_folder / "3000_inverted_index.pickle"

with open(webpage_tokens_pickle, "wb") as f:
    pickle.dump(webpage_tokens, f)

with open(inverted_index_pickle, "wb") as f:
    pickle.dump(inverted_index, f)