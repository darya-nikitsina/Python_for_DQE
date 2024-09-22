# Import numpy module
import numpy as np

# Create list of 100 random numbers from 0 to 1000

# since I will use number of values in the list more than 1 time, create a variable for it
list_size = 100
# create and populate a list with random values according to requirements
random_numbers = list(np.random.randint(low=0, high=1000, size=list_size))


# Sort list from min to max(without using sort())

# create a new variable for sorted list and assign it random_numbers list from scratch
sorted_numbers = random_numbers
# for every i value in the list from first to last
for i in range(0, list_size):
    # for every value k (k is a next value after i) from second to last
    for k in range(i + 1, list_size):
        # if value i greater than or equal to k
        if sorted_numbers[i] >= sorted_numbers[k]:
            # swap i and k
            sorted_numbers[i], sorted_numbers[k] = sorted_numbers[k], sorted_numbers[i]
        else:
            # leave as is
            sorted_numbers[i], sorted_numbers[k]


# Calculate average for even and odd numbers

# create a list for values in random_numbers they remainder of divided by 2 is 0
even_numbers = [num for num in sorted_numbers if num % 2 == 0]
# create a list for values in random_numbers they remainder of divided by 2 is not 0
odd_numbers = [num for num in sorted_numbers if num % 2 != 0]

# try to count average for even numbers: sum of even values divide by number of values in the list
try:
    even_avg = sum(even_numbers)/len(even_numbers)
# except ZeroDivisionError if the variable has no values
except ZeroDivisionError:
    even_avg = 'There is no even values!'

# the same for the odd_numbers
try:
    odd_avg = sum(odd_numbers)/len(odd_numbers)
except ZeroDivisionError:
    odd_avg = 'There is no odd values!'

# print both average result in console
print('Average for even values from sorted list of random numbers:', even_avg,
      '\n' 'Average for odd values from sorted list of random numbers:', odd_avg)
