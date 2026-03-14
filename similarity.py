import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# load dataset
data = pd.read_csv("dataset/code_pairs.csv")

# combine code snippets
corpus = list(data["code1"]) + list(data["code2"])

# create TF-IDF model
vectorizer = TfidfVectorizer()
vectorizer.fit(corpus)


def preprocess(code):
    code = code.lower()
    code = re.sub(r'[^a-zA-Z]', ' ', code)   # remove symbols
    code = re.sub(r'\s+', ' ', code)         # remove extra spaces
    return code


def compute_similarity(code1, code2):
    code1 = preprocess(code1)
    code2 = preprocess(code2)

    vectors = vectorizer.transform([code1, code2])
    score = cosine_similarity(vectors[0], vectors[1])

    return score[0][0]