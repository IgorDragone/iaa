import nltk
import re
import csv
import sys
import math
import pandas as pd

csv.field_size_limit(sys.maxsize)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from spellchecker import SpellChecker

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
spell = SpellChecker()

#######################################
# Tokenize the text and sort the words #
#######################################
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

#######################################
# Preprocess the text                 #
#######################################
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

#######################################
# Divide the emails in safe and phishing #
#######################################
def divide_files(file_path):
    #we delete the content of 'safe.txt' and 'phishing.txt'
    open('safe.txt', 'w').close()
    open('phishing.txt', 'w').close()

    # Open the file
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header
        for row in reader:

            # Tokenize the text
            mail_type = row[2]
            text = row[1]
            tokens = word_tokenize(text)  # Assuming the text is in the second column
            preprocessed_text = ''
            for word in tokens:
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


###############################
# Build the language model     #
###############################
def build_language_model(corpus_file, vocabulary_file):
    # Read the vocabulary
    with open(vocabulary_file, 'r') as f:
        vocabulary = f.read().splitlines()

    #we delete the first line of the vocabulary
    vocabulary = vocabulary[1:]

    # Initialize the language model
    language_model = {word: 0 for word in vocabulary}

    unknown_word_count = 0

    # Read the corpus
    with open(corpus_file, 'r') as f:
        for line in f:
            words = line.split()
            for word in words:
                if word in language_model:
                    language_model[word] += 1
                else:
                    unknown_word_count += 1
    
    if unknown_word_count > 0:
        language_model['<UNK>'] = unknown_word_count
                

    return language_model

#########################################
# Write the language model in a file    #
#########################################
def write_language_model(language_model, file):
    output_file = file.split('.')[0]
    
    number_of_emails = sum(1 for line in open(file))
    number_of_words = sum(language_model.values())
    with open(f'{output_file}_language_model.txt', 'w') as f:
        f.write(f'Numero de correos del corpus: {number_of_emails}\n')
        f.write(f'Numero de palabras del corpus: {number_of_words}\n')
        for word, count in language_model.items():
            log_prob = math.log((count + 1)/(number_of_words + len(language_model)))
            f.write(f'Palabra: {word}, Frecuencia: {count} LogProb: {log_prob}\n')

###############################
# Preprocess the input corpus #
###############################
def preprocess_input_corpus(input):
    #we delete the content of 'input_corpus.csv' and 'expected_output.csv'
    open('input_corpus.csv', 'w').close()
    open('expected_output.csv', 'w').close()

    # Open the file
    with open(input, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header
        for row in reader:

            # Tokenize the text
            text = row[1]
            classification = row[2]
            tokens = word_tokenize(text)  # Assuming the text is in the second column
            preprocessed_text = ''
            for word in tokens:
                prepocessed_word = preprocess_text(word)
                if prepocessed_word:
                    preprocessed_text += f'{prepocessed_word} '
    
            if preprocessed_text:
                with open('input_corpus.csv', 'a') as f:
                    f.write(f'{preprocessed_text}\n')
                with open('expected_output.csv', 'a') as f:
                    f.write(f'{classification}\n')
            
                    
        
###############################
# Classify the email          #
###############################
def classify_email(language_model_safe, language_model_phishing, input_corpus):
    file = open('clasificacion_alu0101469652.csv', 'w')
    file2 = open('resumen_alu0101469652.csv', 'w')

    number_of_safe_mails = sum(1 for line in open('safe.txt'))
    number_of_phishing_mails = sum(1 for line in open('phishing.txt'))
    number_of_mails = number_of_safe_mails + number_of_phishing_mails

    vocabulary_length = len(language_model_safe)
    safe_model_length = sum(language_model_safe.values())
    phishing_model_length = sum(language_model_phishing.values())

    # Open the file
    with open(input_corpus, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            text = row[0]
            #we write the first 10 words of the email
            file.write(f'{text[:10]}')
            words = text.split()
            safe_score = 0
            phishing_score = 0
            for word in words:
                if word in language_model_safe:
                    safe_score += math.log((language_model_safe[word] + 1)/(safe_model_length + vocabulary_length))
                else:
                    safe_score += math.log(1/(safe_model_length + vocabulary_length))

                if word in language_model_phishing:
                    phishing_score += math.log((language_model_phishing[word] + 1)/(phishing_model_length + vocabulary_length))
                else:
                    phishing_score += math.log(1/(phishing_model_length + vocabulary_length))
    

            safe_score += math.log(number_of_safe_mails/number_of_mails)
            phishing_score += math.log(number_of_phishing_mails/number_of_mails)

            #We round the scores to 2 decimal places
            safe_score = round(safe_score, 2)
            phishing_score = round(phishing_score, 2)

            #we write the score of the email
            file.write(f', {safe_score}, {phishing_score}')

            #we write the classification of the email
            if safe_score > phishing_score:
                file.write(', Safe Email\n')
                file2.write('Safe Email\n')
            else:
                file.write(', Phishing Email\n')
                file2.write('Phishing Email\n')

    file.close()
    file2.close()
    
###############################
# Compare the results         #
###############################
def compare_results(input, output):
    # Open the files
    number_of_emails = sum(1 for line in open(input))
    errors = 0
    with open(input, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        with open(output, 'r') as f2:
            reader2 = csv.reader(f2, delimiter=';')
            for row, row2 in zip(reader, reader2):
                if row[0] != row2[0]:
                    errors += 1

    accuracy = 1 - errors/number_of_emails
    accuracy = round(accuracy, 2)
    print(f'Accuracy: {accuracy}')



###############################
# Main function               #
###############################
def main():
    file_path = "PH_train_1.csv"
    result = tokenize_and_sort(file_path)

    # Write the result to vocabulario.txt
    with open('vocabulario.txt', 'w') as f:
        f.write(f'Numero de palabras:{len(result)}\n')
        for word in result:
            f.write(f'{word}\n')

    divide_files(file_path)

    files = ["safe.txt", "phishing.txt"]
    models = []
    for file in files:
        language_model = build_language_model(file, 'vocabulario.txt')
        models.append(language_model)
        write_language_model(language_model, file)

    input = 'PH_train_2.csv'
    preprocess_input_corpus(input)

    classify_email(models[0], models[1], 'input_corpus.csv' )
    compare_results('expected_output.csv', 'resumen_alu0101469652.csv')


main()