# <div align="center">TextExtractoNLP: Web data scrapping and feature extraction for NLP</div>
<div align="center">
  <img src="readme_data/TextExtractoNLP.jpg" alt="Watch-Guard-AI" width="500"/>
</div>

## Table of content
--------------
1. [Introduction](#introduction)
2. [Details](#details)
3. [Tools and  techniques used](#tools-and-techniques-used)


## Introduction
---------------
TextExtractoNLP is a data scrapping and natural language processing (NLP) project designed to automate the extraction of article content from URLs provided in an Excel file and perform detailed text analysis. Utilizing Python libraries like BeautifulSoup, Selenium, and Scrapy, the project focuses on deriving sentiment scores, readability metrics, and other key textual variables, helping to transform raw textual data into structured insights. The analysis includes calculating polarity, subjectivity, word count, syllable count, and identifying personal pronouns, ensuring comprehensive content evaluation.

This project is mainly focused on DATA SCRAPPING and FEATURE GENERATION out of scrapped data i.e. creating the dataset.

## Details
----------

* Scrapping the dataset using BeautifulSoup for each URL in input.xlsx in artifacts folder.
* Cleaning of textual data is done using stop words lists present in artifacts folder. Stop word list is custom defined stopwords.
* The feature of the data that are extracted are for NLP process are as follows:

1) **Positive Score**: This score is calculated by assigning the value of +1 for each word if found in the Positive Dictionary which is present in artifacts folder in MasterDictionary and then adding up all the values.
2) **Negative Score**: This score is calculated by assigning the value of -1 for each word if found in the Negative Dictionary which is present in artifacts folder in MasterDictionary and then adding up all the values. We multiply the score with -1 so that the score is a positive number.
3) **Polarity Score**: This is the score that determines if a given text is positive or negative in nature. It is calculated by using the formula: 
Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
4) **Subjectivity Score**: This is the score that determines if a given text is objective or subjective. It is calculated by using the formula: 
Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
5) **Average Sentence Length** = the number of words / the number of sentences
6) **Percentage of Complex words** = the number of complex words / the number of words 
7) **Fog Index** = 0.4 * (Average Sentence Length + Percentage of Complex words)
8) **Complex Word Count**: Complex words are words in the text that contain more than two syllables.
9) **Word Count**: We count the total cleaned words present in the text after removing stopwords and punctuation.
10) **Syllable Count Per Word**: We count the number of Syllables in each word of the text by counting the vowels present in each word. We also handle some exceptions like words ending with "es","ed" by not counting them as a syllable.
11) **Personal Pronouns**: To calculate Personal Pronouns mentioned in the text, we use regex to find the counts of the words - “I,” “we,” “my,” “ours,” and “us”. Special care is taken so that the country name US is not included in the list.

## Tools and  techniques used
-----------------------------
* Pandas
* BeautifulSoup
* nltk


