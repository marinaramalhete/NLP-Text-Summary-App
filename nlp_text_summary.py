# Import dependencies
from collections import defaultdict
from heapq import nlargest
# from io import StringIO
from string import punctuation

# If you have problems in install nltk, try the options:
import nltk
nltk.download('stopwords')
nltk.download('punkt')
import streamlit as st
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize

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
    st.markdown("<h4 '>Enter your text and choose a language and a series of sentences that you consider important for your summary!\
        The rest is done by natural language processing and statistics!</h4>", unsafe_allow_html=True)
    st.write('')

    uploaded_file = st.text_area('Type or paste here:',
                                 'Processamento de linguagem natural (NLP, em inglês) é uma subárea da ciência da\
                                  computação, inteligência artificial e da linguística que estuda os problemas da\
                                  geração e compreensão automática de linguas humanas naturais. Sistemas de geração\
                                  de linguagem natural convertem informação de bancos de dados de computadores em\
                                  linguagem compreensível ao ser humano e sistemas de compreensão de linguagem natural\
                                  convertem ocorrências de linguagem humana em representações mais formais, mais\
                                  facilmente manipuláveis por programas de computador. Alguns desafios do NLP são\
                                  compreensão de linguagem natural, fazer com que computadores extraiam sentido de\
                                  linguagem humana ou natural e geração de linguagem natural.', height=300)

    if uploaded_file is not None:
        # To convert to a string based IO:
        # stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # To read file as string:
        # uploaded_file = stringio.read()

        # Sidebar Menu
        options = ["Portuguese", "English"]
        menu = st.sidebar.selectbox("Choose a language:", options)

        # Choices
        if menu == "Portuguese":
            st.title("This is the summary of your text :unlock:")
            n_sent = st.sidebar.slider('Choose a number of important sentences:', value=1)
            sumarize_text_portuguese(uploaded_file, n_sent)

        if menu == "English":
            st.header("English Language. \n \n This is the summary of your text.")
            n_sent = st.sidebar.slider('Number of sentences (default is 2).', value=1)
            sumarize_text_english(uploaded_file, n_sent)

        st.sidebar.info('Check out the project on [Github](https://github.com/marinaramalhete/NLP-Text-Summary-App)')


if __name__ == '__main__':
    main()
