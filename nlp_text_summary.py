# Import dependencies
from collections import defaultdict
from heapq import nlargest
from io import StringIO
from string import punctuation

import streamlit as st
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize


# If you have problems in install nltk, try the options:
# import nltk
# nltk.download('stopwords')

# import nltk
# import ssl
# try:
#      _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
# nltk.download()


# Functions for resume in Portuguese
stopwords_ptbr = set(stopwords.words('portuguese') + list(punctuation))

def RemoveStopWordsAndPunctInPortuguese(text):
    words = word_tokenize(text.lower())
    return [word for word in words if word not in stopwords_ptbr]

def SumarizeTextPortuguese(text, n_sent=2):
    words_not_stopwords = RemoveStopWordsAndPunctInPortuguese(text)
    sentences = sent_tokenize(text)
    frequency = FreqDist(words_not_stopwords)
    important_sentences = defaultdict(int)

    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in frequency:
                important_sentences[i] += frequency[word]

    numb_sent = n_sent
    idx_important_sentences = nlargest(numb_sent,
                                        important_sentences,
                                        important_sentences.get)

    for i in sorted(idx_important_sentences):
        st.write(sentences[i])


# Functions for resume in English
stopwords_en = set(stopwords.words('english') + list(punctuation))

def RemoveStopWordsAndPunctInEnglish(text):
    words = word_tokenize(text.lower())
    return [word for word in words if word not in stopwords_en]

def SumarizeTextEnglish(text, n_sent=2):
    words_not_stopwords = RemoveStopWordsAndPunctInEnglish(text)
    sentences = sent_tokenize(text)
    frequency = FreqDist(words_not_stopwords)
    important_sentences = defaultdict(int)

    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in frequency:
                important_sentences[i] += frequency[word]

    numb_sent = n_sent
    idx_important_sentences = nlargest(numb_sent,
                                        important_sentences,
                                        important_sentences.get)

    for i in sorted(idx_important_sentences):
        return st.write(sentences[i])


def main():

    st.title('NLP Summary Text')
    st.header('Summary texts in Portuguese or English.')

    uploaded_file  = st.file_uploader('Upload your text!')
    if uploaded_file is not None:
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # To read file as string:
        uploaded_file = stringio.read()

        # Sidebar Menu
        options = ["Select language", "Portuguese", "English"]
        menu = st.sidebar.selectbox("Menu options", options)

        # Choices
        if (menu == "Portuguese"):
            st.header("Portuguese Language. \n This is the summary of your text.")
            n_sent = st.sidebar.slider('Number of sentences (default is 2).', value = 100)
            SumarizeTextPortuguese(uploaded_file, n_sent)

        if (menu == "English"):
            st.header("English Language. \n \n This is the summary of your text.")
            n_sent = st.sidebar.slider('Number of sentences (default is 2).', value = 100)
            SumarizeTextEnglish(uploaded_file, n_sent=5)

        st.sidebar.title('Hi, everyone!')
        st.sidebar.info('I hope this app is userful for you! \n \
            You find me here: \n \
            www.linkedin.com/in/marinaramalhete')


if __name__ == '__main__':
    main()
