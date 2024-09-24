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

# print the result
print(dicts_list)
