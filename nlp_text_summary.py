# Import dependencies
from collections import defaultdict
from heapq import nlargest
from io import StringIO
from string import punctuation

import streamlit as st
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer


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

def remove_stopwords_and_punct_in_portuguese(text):
    words = word_tokenize(text.lower())
    return [word for word in words if word not in stopwords_ptbr]

def sumarize_text_portuguese(text, n_sent=2):
    words_not_stopwords = remove_stopwords_and_punct_in_portuguese(text)
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

def remove_stopwords_and_punct_in_english(text):
    words = word_tokenize(text.lower())
    return [word for word in words if word not in stopwords_en]

def sumarize_text_english(text, n_sent=2):
    words_not_stopwords = remove_stopwords_and_punct_in_english(text)
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

    st.title('Summarize texts with NLP :hugging_face:')
    st.info('Is easy! Enter your text and choose a language and a series of sentences that you consider important for your summary!\
        The rest is done by natural language processing and statistics!')

    uploaded_file  = st.text_area('Enter text to be summarize:', height = 350)
    if st.button('Summarize'):
        if uploaded_file == '':
            st.error('Please enter some text')
        #     # To convert to a string based IO:
        #     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        #     # To read file as string:
        #     uploaded_file = stringio.read()

        # Sidebar Menu
        options = ["Portuguese", "English"]
        menu = st.sidebar.selectbox("Choose a language:", options)

        # Choices
        if (menu == "Portuguese"):
            st.title("This is the summary of your text :unlock:")
            n_sent = st.sidebar.slider('Choose a number of important sentences:', value = 50)
            sumarize_text_portuguese(uploaded_file, n_sent)

        if (menu == "English"):
            st.header("English Language. \n \n This is the summary of your text.")
            n_sent = st.sidebar.slider('Number of sentences (default is 2).', value = 50)
            sumarize_text_english(uploaded_file, n_sent=5)

        st.sidebar.info('Check out the project on [Github](https://github.com/marinaramalhete/NLP-Text-Summary-App)')


if __name__ == '__main__':
    main()
