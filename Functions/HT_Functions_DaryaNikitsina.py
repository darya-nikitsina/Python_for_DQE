import random
import string
import re


# Home Task 2 reorganization

# Function to create a list with random number of dicts populated with random int values
# add some default values for arguments
def create_list_of_dicts(min_dict_number=0, max_dict_number=100, min_value=0, max_value=1000):
    # produce int value as a number of dictionaries in range between min_number and max_number
    dict_quantity = random.randint(min_dict_number, max_dict_number)

    # create a variable for the list of dicts
    dicts_list = []

    # for loop to populate the list with dicts
    for d in range(dict_quantity):
        # since there are 26 letters in the english alphabet,
        # use 26 as a max number of key-value pair in each dict
        keys_quantity = random.randint(1, 26)

        # create random keys for the dict as lowercase letters in range of 'a' and 'z'
        # sample method guaranties the uniqueness of keys in a dictionary
        keys = random.sample(string.ascii_lowercase, keys_quantity)

        # create the dict, where: key is a letter from keys, value is a random value in range of min_value and max_value
        letter_number_dict = {key: random.randint(min_value, max_value) for key in keys}

        # collect all previously created dicts into one list of dicts
        dicts_list.append(letter_number_dict)

    return dicts_list


# Create function to get previously generated list of dicts and create one common dict
def create_common_dict(list_of_dicts):
    # if dicts have same key, we will take max value, and rename key with dict number with max value
    # if key is only in one dict - take it as is

    # initiate a dictionary to store max values and keys for them
    max_values = {}

    # for an index and dictionary in the list of dicts
    for index, dictionary in enumerate(list_of_dicts):
        # dict number is greater by one than the index (because first index is 0)
        dict_num = index + 1

        # for key and value in a view of key-value pairs (as tuples in the list)
        for key, value in dictionary.items():
            # if key is not on the dict of max values
            if key not in max_values:
                # place value and dict_num to the dict
                max_values[key] = (value, dict_num)
            # if key is on the dict
            else:
                max_value, max_dict = max_values[key]
                # and if the value for the key is higher than previously added value
                if value > max_value:
                    # replace the value with higher one
                    max_values.update({key: (value, dict_num)})

    # initiate the common dict for all dicts from the list
    common_dict = {}

    # for key-value pair (where value is a tuple of value and dict_num) in the max_values dict
    for key, (value, dict_num) in max_values.items():
        # if number of the same keys (sum of occurrences of one key) more than 1
        if sum(key in dictionary for dictionary in dicts_list) > 1:
            # add combination of key and dict_num from max_values as a key, and value as a value
            # to the common_dict
            common_dict[f'{key}_{dict_num}'] = value
        # in other case
        else:
            # add key from the max_values as a key, and value as a value to the common_dict
            common_dict[key] = value

    return common_dict


dicts_list = create_list_of_dicts(2, 10, 0, 100)
common_dict = create_common_dict(dicts_list)

# print final result
print(dicts_list)
print(common_dict)


# Home Task 2 reorganization
# Function to create new sentence from last words of each sentence from a text
def create_new_sentence(some_text):
    # split the text into sentences for future creation a new sentence
    sentences = re.split(r'(?<=[.!?])\s+', some_text)

    # create new sentence using last word from each sentence
    # I define a sentence as a set of words written in a string.
    # Assume that the meaning of each word and the relationship of words in the sentence are irrelevant.

    # create a list of last words from each sentence
    # use list comprehension to get the last word of each sentence
    last_words_and_punctuation_marks = [sentence.split()[-1] for sentence in sentences if sentence]

    # remove the last element from each item in the list because the last words were taken along with the punctuation mark
    last_words = [word[:-1] for word in last_words_and_punctuation_marks]

    # join the last words into a new sentence and add delimiter to the end of new sentence
    new_sentence = ' '.join(last_words) + r'.'

    return new_sentence


# Function to find a place and add a sentence to the place
def add_sentence(sentence, text):
    # find index of a sentence as an item of the list after that I need to add new sentence
    place_to_insert = re.search(r'END OF this Paragraph\.', text)

    # insert new sentence to the end of the paragraph in the RAW TEXT if the place_to_insert exists
    if place_to_insert:
        position_end = place_to_insert.end()
        updated_text = text[:position_end] + ' ' + sentence + text[position_end:]
    else:
        updated_text = text

    return updated_text


# Function to replace iz to is where it is necessary
def replace_iz_with_is(text):
    replaced_text = re.sub(r'(?<![“"])\biz\b(?![”"])', 'is', text, flags=re.IGNORECASE)

    return replaced_text


# Function to normalize a text from letter case point of view
def normalize_letter_case(text):
    # Capitalize each sentence in the text
    # Split updated text for sentences to capitalize each of them
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Capitalize each sentence and put it to a normalized_sentences list
    normalized_sentences = [sentence.capitalize() for sentence in sentences]

    # replace sentences in updated_text in mixed case with sentences in capitalized case
    normalized_text = text

    for i in range(len(sentences)):
        orig_sentence = sentences[i]
        norm_sentence = normalized_sentences[i]
        normalized_text = normalized_text.replace(orig_sentence, norm_sentence, 1)

    return normalized_text


# Function to find number of whitespaces in the original raw text
def find_whitespaces(text):
    whitespaces_quantity = len(re.findall(r'\s', text))

    return whitespaces_quantity


# Check the functions with raw text
raw_text = r'''homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
'''


new_sentence = create_new_sentence(raw_text)
updated_text = add_sentence(new_sentence, raw_text)
replaced_text = replace_iz_with_is(updated_text)
normalized_text = normalize_letter_case(replaced_text)
whitespace_quantity = find_whitespaces(normalized_text)

print(f'Normalized text is: {normalized_text}')
print(f'Number of whitespace characters is: {whitespace_quantity}')



