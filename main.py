from bs4 import BeautifulSoup
import pandas as pd
import requests
import string
import nltk
import sys
import os
import re

input_data_path = os.path.join(os.getcwd(),'artifacts','Input.xlsx')
input_data = pd.read_excel(input_data_path)

artical_data_path = os.path.join(os.getcwd(),'artifacts','articles')

stopword_data_path = os.path.join(os.getcwd(),'artifacts','StopWords')

master_dictionary_data_path = os.path.join(os.getcwd(),'artifacts','MasterDictionary')


def extract_data(url):
    print(f"Extracting data from url: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        heading = soup.find_all('div',{'id':'td-outer-wrap'})[0].find_all('article')[0].find_all('div')[0].find_all('div')[0].find_all('div')[2].find_all('div')[0].find_all('header')[0].find_all('h1')[0].get_text()
        print(f'Extracted Heading: {heading}')

        description = soup.find('div',{'id':'td-outer-wrap'}).find('article').find('div',{'class':'td-pb-row'}).find('div',{'class':'td-ss-main-content'}).find('div',{'class':'td-post-content tagdiv-type'}).find_all(text=True)
        description  = description [:-2]

        cleaned_description = []
        for data in description:
            if data != '\n':
                cleaned_description.append(data)
        
        final_description = " ".join(cleaned_description)
        print(f"Extracted description:\n{final_description}")
        
        article = heading + final_description
        print(f"Final extracted article:\n{article}")
        
        return article
    except Exception as e:
        print(f'An exception occured while extracting data from {url}\nThe Exception is {e}')
        try:
            heading = soup.find_all('div',{'id':'td-outer-wrap'})[0].find_all('div',{'id':'tdb-autoload-article'})[0].find_all('div')[0].find_all('div')[0].find_all('article')[0].find_all('div')[0].find_all('div')[0].find_all('div',{'id':'tdi_117'})[0].find_all('div')[0].find_all('div')[0].find_all('div')[0].find_all('h1')[0].get_text()
            print(f'Extracted Heading: {heading}')

            description = soup.find('div',{'id':'td-outer-wrap'}).find('article').find('div',{'class':'td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type'}).find('div',{'class':'tdb-block-inner td-fix-index'}).find_all(text=True)
            description  = description [:-2]

            cleaned_description = []
            for data in description:
                if data != '\n':
                   cleaned_description.append(data)
        
            final_description = " ".join(cleaned_description)
            print(f"Extracted description:\n{final_description}")
        
            article = heading + final_description
            print(f"Final extracted article:\n{article}")

            return article
        except Exception as e:
            print(f"Error occurred while extracting article using second path: {e}")
            return "Error 404 link not accesible"
        

def getting_data_frame():
    URL_ID = []
    URL = []
    articles = []
    for index_id in range(len(input_data)):
        print(index_id)
        article_data = extract_data(input_data["URL"][index_id])
        if article_data != "Error 404 link not accesible":
            articles.append(article_data)
            URL.append(input_data["URL"][index_id])
            URL_ID.append(input_data["URL_ID"][index_id])

        else:
            print(f"{input_data['URL'][index_id]} is not working")
    
    df = pd.DataFrame({
        "URL_ID":URL_ID,
        "URL":URL,
        "articles":articles
    })

    return df

def calculate_average_word_length(text):
    words = text.split()
    total_characters = sum(len(word) for word in words)
    total_words = len(words)
    if total_words > 0:
        return total_characters / total_words
    else:
        return 0

def count_personal_pronouns(text):
    pronoun_pattern = r'\b(?:I|we|my|ours|us)\b(?!\s+US\b)'
    pronoun_matches = re.findall(pronoun_pattern, text, flags=re.IGNORECASE)
    return len(pronoun_matches)

def count_syllables(word):
    word = word.lower()
    exceptions = ["es", "ed"]
    vowels = 'aeiou'
    vowel_count = 0
    prev_char = None
    for char in word:
        if char in vowels and (prev_char is None or prev_char not in vowels):
            vowel_count += 1
        prev_char = char
    
    for exception in exceptions:
        if word.endswith(exception):
            vowel_count -= 1
    
    vowel_count = max(1, vowel_count)
    
    return vowel_count

def calculate_syllable_count(text):
    words = text.split()
    syllable_counts = [count_syllables(word) for word in words]
    return syllable_counts

def count_syllables_1(word):
    word = word.lower()
    exceptions = ["es", "ed"]
    vowels = 'aeiou'
    vowel_count = 0
    prev_char = None
    for char in word:
        if char in vowels and (prev_char is None or prev_char not in vowels):
            vowel_count += 1
        prev_char = char
    
    for exception in exceptions:
        if word.endswith(exception):
            vowel_count -= 1
    
    vowel_count = max(1, vowel_count)
    
    return vowel_count

def count_complex_words(text):
    words = text.split()
    complex_word_count = sum(1 for word in words if count_syllables_1(word) > 2)
    return complex_word_count

def calculate_average_sentence_length(text):
    sentences = nltk.sent_tokenize(text)
    total_words = sum(len(nltk.word_tokenize(sentence)) for sentence in sentences)
    total_sentences = len(sentences)
    if total_sentences > 0:
        return total_words / total_sentences
    else:
        return 0

def calculate_average_words_per_sentence(text):
    sentences = nltk.sent_tokenize(text)
    total_words = sum(len(nltk.word_tokenize(sentence)) for sentence in sentences)
    total_sentences = len(sentences)
    if total_sentences > 0:
        return total_words / total_sentences
    else:
        return 0
    
def main():
    data =  getting_data_frame()
    df = data.dropna()
    
    stopwords_list = []
    for filename in os.listdir(stopword_data_path):
        file_path = os.path.join(stopword_data_path, filename)
        with open(file_path, 'r',encoding="ISO-8859-1") as file:
             for line in file:
                 stopword = line.strip().split('|')[0].strip()
                 stopwords_list.append(stopword.lower())
    
    df['clean_articles'] = df['articles'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stopwords_list]))
    df['clean_articles'] = df['clean_articles'].apply(lambda x: ''.join([char for char in x if char not in string.punctuation]))

    positive_words = []
    negative_words = []
    for filename in os.listdir(master_dictionary_data_path):
        if filename == 'positive-words.txt':
           file_path = os.path.join(master_dictionary_data_path, filename)
           with open(file_path, 'r',encoding="ISO-8859-1") as file:
                for line in file:
                    positive = line.strip()
                    positive_words.append(positive.lower())
        elif filename == 'negative-words.txt':
            file_path = os.path.join(master_dictionary_data_path, filename)
            with open(file_path, 'r',encoding="ISO-8859-1") as file:
                for line in file:
                    negative = line.strip()
                    negative_words.append(negative.lower())

    positive_words = list(set(positive_words))
    negative_words = list(set(negative_words))

    positive = []
    pos = []
    for sen in df['clean_articles']:
        word_list = sen.split(" ")
        for word in word_list:
            if word in positive_words:
                pos.append(word)
        positive.append(pos)
        pos = []

    negative = []
    neg = []
    for sen in df['clean_articles']:
        word_list = sen.split(" ")
        for word in word_list:
            if word in negative_words:
                neg.append(word)
        negative.append(neg)
        neg = []

    df['positive'] = positive
    df['negative'] = negative
    df['POSITIVE SCORE'] = [len(x) for x in df['positive']]
    df['NEGATIVE SCORE'] = [len(x) for x in df['negative']]
    df['POLARITY SCORE'] = ((df['POSITIVE SCORE'] - df['NEGATIVE SCORE'])/(df['POSITIVE SCORE'] + df['NEGATIVE SCORE']+ 0.000001)) 
    df['total_number_of_words'] = [len(x.split(' ')) for x in df['clean_articles']]
    df['SUBJECTIVITY SCORE'] = ((df['POSITIVE SCORE'] + df['NEGATIVE SCORE'])/(df['total_number_of_words'])+0.000001)
    df['AVG WORD LENGTH'] = df['clean_articles'].apply(calculate_average_word_length)
    df['PERSONAL PRONOUNS'] = df['clean_articles'].apply(lambda x: count_personal_pronouns(x))
    df['SYLLABLE PER WORD'] = df['clean_articles'].apply(lambda x: calculate_syllable_count(x))
    df['WORD COUNT'] = df['total_number_of_words']
    df['COMPLEX WORD COUNT'] = df['clean_articles'].apply(lambda x: count_complex_words(x))
    df['AVG SENTENCE LENGTH'] = df['articles'].apply(calculate_average_sentence_length)
    df["PERCENTAGE OF COMPLEX WORDS"] = df['COMPLEX WORD COUNT']/df['WORD COUNT']
    df['FOG INDEX'] = 0.4*(df['AVG SENTENCE LENGTH'] + df['PERCENTAGE OF COMPLEX WORDS'])
    df['AVG NUMBER OF WORDS PER SENTENCE'] = df['clean_articles'].apply(calculate_average_words_per_sentence)
    Output_data = df[['URL_ID','URL','POSITIVE SCORE','NEGATIVE SCORE','POLARITY SCORE','SUBJECTIVITY SCORE','AVG SENTENCE LENGTH','PERCENTAGE OF COMPLEX WORDS','AVG NUMBER OF WORDS PER SENTENCE','COMPLEX WORD COUNT','WORD COUNT','SYLLABLE PER WORD','PERSONAL PRONOUNS','AVG WORD LENGTH']]
    Output_data.to_csv("Ouput_data.csv")
    print("done")

if __name__ == '__main__':
    main()

