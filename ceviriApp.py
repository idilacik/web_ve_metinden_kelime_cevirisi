from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def pageOpener(url):
    """Adresi verilen sayfayi acar gereksiz HTML etiketlerini temizler"""
    htmlPage = urlopen(url).read()
    soup = BeautifulSoup(htmlPage, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    return text


def get_wordnet_pos(tag):
    """POS tag'ini WordNet formatina cevirir"""
    if tag.startswith('J'):
        return 'a'
    elif tag.startswith('V'):
        return 'v'
    elif tag.startswith('N'):
        return 'n'
    elif tag.startswith('R'):
        return 'r'
    else:
        return 'n'


def word_list_make(lemmatized_list):
    """Sozlukte olan kelimeleri listeler"""
    word_file= open("merged_file1.txt", "r", encoding="utf-8")
    x = word_file.readlines()
    word_file.close()

    dict_words = {}

    for line in x:
        y = line.split("\t")
        if len(y) >= 2:
            eng = y[0].strip().lower()
            turkce = y[1].strip()
            dict_words[eng] = turkce

    result = {}

    for i in lemmatized_list:
        clean_word = i.strip().lower()
        if clean_word in dict_words:
            result[clean_word] = dict_words[clean_word]

    return dict(sorted(result.items()))

def translate_from_url(url):
    """URL'den sayfa cekip kelime cevirir"""

    text = pageOpener(url)
    tokens = word_tokenize(text)
    tagged_tokens = pos_tag(tokens)

    # lemmatize et
    lemmatized_list = []
    for word, tag in tagged_tokens:
        if word.lower() in ['am', 'is', 'are']:
            lemmatized_list.append(word.lower())
        else:
            lemmatized_list.append(lemmatizer.lemmatize(word, get_wordnet_pos(tag)))

    # sozlukten cevir
    word_dict = word_list_make(lemmatized_list)

    return word_dict

def translate_from_text(text):
    """Metinden ceviri yapar"""

    tokens = word_tokenize(text)
    tagged_tokens = pos_tag(tokens)

    lemmatized_list = []
    for word, tag in tagged_tokens:
        if word.lower() in ['am', 'is', 'are']:
            lemmatized_list.append(word.lower())
        else:
            lemmatized_list.append(lemmatizer.lemmatize(word, get_wordnet_pos(tag)))

    word_dict = word_list_make(lemmatized_list)

    return word_dict

