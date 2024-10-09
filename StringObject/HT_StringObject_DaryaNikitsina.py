# import re module to use its split() method
import re

# create a variable for the raw text
raw_text = r'''homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
'''

# split the text into sentences for future creation a new sentence
sentences = re.split(r'(?<=[.!?])\s+', raw_text)

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

# find index of a sentence as an item of the list after that I need to add new sentence
place_to_insert = re.search(r'END OF this Paragraph\.', raw_text)

# insert new sentence to the end of the paragraph in the RAW TEXT if the place_to_insert exists
if place_to_insert:
    position_end = place_to_insert.end()
    updated_text = raw_text[:position_end] + ' ' + new_sentence + raw_text[position_end:]

# replace iz to is where it is necessary
updated_text = re.sub(r'(?<![“"])\biz\b(?![”"])', 'is', updated_text, flags=re.IGNORECASE)

# Capitalize each sentence in the text
# Split updated text for sentences to capitalize each of them
updated_sentences = re.split(r'(?<=[.!?])\s+', updated_text)

# Capitalize each sentence and put it to a normalized_sentences list
normalized_sentences = [sentence.capitalize() for sentence in updated_sentences]

# replace sentences in updated_text in mixed case with sentences in capitalized case
normalized_text = updated_text

for i in range(len(updated_sentences)):
    orig_sentence = updated_sentences[i]
    norm_sentence = normalized_sentences[i]
    normalized_text = normalized_text.replace(orig_sentence, norm_sentence, 1)

# find number of whitespaces in the original raw text
whitespaces_quantity = len(re.findall(r'\s', normalized_text))

# check results
print(normalized_text)
print(whitespaces_quantity)
