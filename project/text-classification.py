import nltk
import re
import csv
import sys

csv.field_size_limit(sys.maxsize)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))


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
            prepocessed_text = preprocess_text(text)
            if prepocessed_text:
                if mail_type == "Safe Email":
                    with open("safe.txt", 'a') as f:
                        f.write(f'{prepocessed_text}\n')
                else:
                    with open('phishing.txt', 'a') as f:
                        f.write(f'{prepocessed_text}\n')


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

def write_language_model(language_model, output_file):
    output_file = output_file.split('.')[0]
    with open(f'{output_file}_language_model.txt', 'w') as f:
        for word, count in language_model.items():
            f.write(f'{word} {count}\n')
        

def main():
    #file_path = "emails.csv"
    # divide_files(file_path)
    # result = tokenize_and_sort(file_path)

    # # Write the result to vocabulario.txt
    # with open('vocabulario.txt', 'w') as f:
    #     f.write(f'Numero de palabras:{len(result)}\n')
    #     for word in result:
    #         f.write(f'{word}\n')

    files = ["safe.txt", "phishing.txt"]
    for file in files:
        language_model = build_language_model(file, 'vocabulario.txt')
        write_language_model(language_model, file)

main()