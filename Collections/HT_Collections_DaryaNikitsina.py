# import module for random values creation
import random
# import string module for random letter key creation
import string

# Create a list of random number of dicts (from 2 to 10)
# dict's random numbers of keys should be letter, dict's values should be a number (0-100)

# produce int value as a number of dictionaries in range between 2 and 10
dict_quantity = random.randint(2, 10)

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

    # create the dict, where: key is a letter from keys, value is a random value in range of 0 and 100
    letter_number_dict = {key: random.randint(0, 100) for key in keys}

    # collect all previously created dicts into one list of dicts
    dicts_list.append(letter_number_dict)

# print intermediate result
print(dicts_list)

# Get previously generated list of dicts and create one common dict:
# if dicts have same key, we will take max value, and rename key with dict number with max value
# if key is only in one dict - take it as is

# initiate a dictionary to store max values and keys for them
max_values = {}

# for an index and dictionary in the list of dicts
for index, dictionary in enumerate(dicts_list):
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

# print final result
print(common_dict)
