import nltk
import re
import csv
import sys
import math

csv.field_size_limit(sys.maxsize)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from spellchecker import SpellChecker

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
spell = SpellChecker()

# Tokenize the text and sort the words
def tokenize_and_sort(file_path):
    words = []
    # Open the file
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header
        for row in reader:
            # Tokenize the text
            tokens = word_tokenize(row[1])  # Assuming the text is in the second column
            for token in tokens:
                prepocessed_token = (preprocess_text(token))
                if prepocessed_token:
                    words.append(prepocessed_token)

    # Remove duplicates and sort
    unique_sorted_words = sorted(set(words))

    return unique_sorted_words

def preprocess_text(word):
    # Convert to lowercase
    word = word.lower()

    # # # Correct the spelling
    # word = spell.correction(word)
    # if word == None : return None

    # # stem the word
    # word = stemmer.stem(word)

    # # Remove URLs
    word = re.sub(r'http\S+|www\S+|https\S+', '', word, flags=re.MULTILINE)

    # # Remove HTML tags
    word = re.sub(r'<.*?>', '', word)

    # # Remove hashtags
    word = re.sub(r'#\w+', '', word)

    # # Remove punctuation
    word = re.sub(r'[^\w\s]', '', word)

    # # Remove lower bars
    word = re.sub(r'_', '', word)

    # if is a number, create the token number
    if word.isnumeric():
        return "<NUMBER>"
    
    #if it contains a number, create the token number
    if any(char.isdigit() for char in word):
        return None

    # # Remove stopwords
    if word in stop_words:
        return None

    if word == '':
        return None
    
    return word

def divide_files(file_path):
    # Open the file
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header
        for row in reader:

            # Tokenize the text
            mail_type = row[2]
            text = row[1]
            preprocessed_text = ''
            for word in text.split():
                prepocessed_word = preprocess_text(word)
                if prepocessed_word:
                    preprocessed_text += f'{prepocessed_word} '
    
            if preprocessed_text:
                if mail_type == "Safe Email":
                    with open("safe.txt", 'a') as f:
                        f.write(f'{preprocessed_text}\n')
                else:
                    with open('phishing.txt', 'a') as f:
                        f.write(f'{preprocessed_text}\n')


def build_language_model(corpus_file, vocabulary_file):
    # Read the vocabulary
    with open(vocabulary_file, 'r') as f:
        vocabulary = f.read().splitlines()

    # Initialize the language model
    language_model = {word: 0 for word in vocabulary}

    # Read the corpus
    with open(corpus_file, 'r') as f:
        for line in f:
            words = line.split()
            for word in words:
                if word in language_model:
                    language_model[word] += 1

    return language_model

def write_language_model(language_model, file):
    output_file = file.split('.')[0]
    
    number_of_emails = sum(1 for line in open(file))
    number_of_words = sum(language_model.values())
    with open(f'{output_file}_language_model.txt', 'w') as f:
        f.write(f'Numero de correos del corpus: {number_of_emails}\n')
        f.write(f'Numero de palabras del corpus: {number_of_words}\n')
        unknown_words = 0
        for word, count in language_model.items():
            if count == 0:
                unknown_words += 1
            else:
                log_prob = math.log((count + 1)/(number_of_words + len(language_model)))
                f.write(f'Palabra: {word}, Frecuencia: {count} LogProb: {log_prob}\n')
        
        f.write(f'Palabra: <UNKNOWN>, Frecuencia: {unknown_words} LogProb: {math.log(1/(number_of_words + len(language_model)))}\n')
        

def main():
    # file_path = "emails.csv"
    # result = tokenize_and_sort(file_path)

    # # Write the result to vocabulario.txt
    # with open('vocabulario.txt', 'w') as f:
    #     f.write(f'Numero de palabras:{len(result)}\n')
    #     for word in result:
    #         f.write(f'{word}\n')

    # divide_files(file_path)

    files = ["safe.txt", "phishing.txt"]
    for file in files:
        language_model = build_language_model(file, 'vocabulario.txt')
        write_language_model(language_model, file)

main()