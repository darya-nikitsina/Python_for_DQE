import csv
from collections import Counter
import re

news_feed = '../Classes_OOP/NewsFeed.txt'

def open_read(file):
    try:
        with open(file, 'r', encoding='utf-8') as s:
            text = s.read()

        return text

    except BaseException as ex:
        print("File can't be opened because of exception:")
        print(ex)


# count number of word repetitions
def word_count(source_file=news_feed):

    try:
        source_text = open_read(source_file).lower()

        # negative lookbehind (?<!°) part in regular expression to exclude elements after °
        # since it can't be a real meaningful word
        words = re.findall(r"(?<!°)\b[a-z]+(?:['’][a-z]+)?\b", source_text)

        # find count for each word
        word_count = Counter(words)

        # sort the dictionary by count descending for better readability
        sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

        with open('WordCount.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='-')

            for word, count in sorted_word_count:
                writer.writerow([word, count])

        print('Number of word repetition has been successfully written to the WordCount.csv')

    except BaseException as exception:
        print("Something went wrong. Number of word repetitions can't be counted and/or recorded. Please see exception:")
        print(exception)


def letter_stats (source_file=news_feed):
    try:
        source_text = open_read(source_file)

        letters = re.findall(r'[a-zA-Z]', source_text)

        # calculate stats for a single letter
        all_letters_count = Counter(letter.lower() for letter in letters)
        uppercase_letters_count = Counter(letter for letter in letters if letter.isupper())

        # total number of all letters to be used in percentage
        all_total_number = len(letters)

        letter_stats = []
        for letter in sorted(all_letters_count.keys()):
            count_all = all_letters_count[letter]
            count_uppercase = uppercase_letters_count[letter.upper()]
            percentage = (count_all / all_total_number) * 100
            letter_stats.append([letter.lower(), count_all, count_uppercase, f"{percentage:.2f}"])

        with open('LetterStats', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='|')
            writer.writerow(['letter', 'count_all', 'count_uppercase', 'percentage'])
            writer.writerows(letter_stats)

        print('Letter statistics has been successfully written to the LetterStats.csv file.')

    except BaseException as ex:
        print("Something went wrong. Statistics can't be counted and/or recorded. Please see exception:")
        print(ex)

def letter_word_statistics():
    word_count()
    letter_stats()

