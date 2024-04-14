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

    # # Remove stopwords
    if word in stop_words:
        return None

    if word == '':
        return None
    
    return word

def main():
    file_path = "emails.csv"
    result = tokenize_and_sort(file_path)

    # Write the result to vocabulario.txt
    with open('vocabulario.txt', 'w') as f:
        f.write(f'Numero de palabras:{len(result)}\n')
        for word in result:
            f.write(f'{word}\n')

main()