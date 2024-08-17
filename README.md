## To sun the program and get the output:
* 1) run --> pip install -r requirements.txt  --- {To install required dependecies}
* 2) run --> python main.py  --- (To extract data and save it in required format)

## Basic explanation, how code works:

Importing Libraries: The script begins by importing necessary libraries such as BeautifulSoup for web scraping, pandas for data manipulation, requests for making HTTP requests, nltk for natural language processing tasks, and re for regular expressions.

File Paths Setup: The script sets up file paths for input data (an Excel file containing URLs), output data, and other artifacts required for analysis.

Data Extraction: The extract_data function extracts article content from provided URLs using web scraping techniques. It handles exceptions gracefully and returns either the extracted article or an error message.

Data Frame Creation: The getting_data_frame function iterates over the URLs in the input Excel file, extracts article content using the extract_data function, and constructs a pandas DataFrame containing URL IDs, URLs, and extracted articles.

Text Preprocessing: The script loads stop words from files, removes them from the articles, and removes punctuation from the cleaned text.

Sentiment Analysis: It loads positive and negative word lists, counts occurrences of these words in each article, calculates polarity and subjectivity scores, and adds them to the DataFrame.

Linguistic Feature Calculation: The script calculates various linguistic features such as average word length, personal pronoun count, syllables per word, average sentence length, percentage of complex words, Fog index, and average number of words per sentence. These features are added to the DataFrame.

Output: The DataFrame is then filtered to select relevant columns and saved as a CSV file named "Output_data.csv".

Main Function: The main function orchestrates the entire process by calling the necessary functions in order.

Execution: Finally, the script checks if it's being run directly (__name__ == '__main__') and if so, executes the main function.
