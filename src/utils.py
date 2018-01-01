from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

porter_stem = PorterStemmer()


def get_stemmed_string(input_string):
    words = word_tokenize(input_string)
    final_output = []
    stop_words_rem = set(stopwords.words('english'))
    for tokens in words:
        if tokens not in stop_words_rem:
            final_output.append(porter_stem.stem(tokens.lower()))
    return ' '.join(final_output)