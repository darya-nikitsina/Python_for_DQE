# import re module to use its split() method
import re

# create a variable for the raw text
raw_text = r'''homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
'''

# split the text into sentences by colon or period, since there are possible sentence delimiters in the text
sentences = re.split(r'(?<=[.:])\s+', raw_text)

# create new sentence using last word from each sentence
# I define a sentence as a set of words written in a string.
# Assume that the meaning of each word and the relationship of words in the sentence are irrelevant.

# create a list of last words from each sentence
# use list comprehension to get the last word of each sentence
last_words_and_punctuation_marks = [sentence.split()[-1] for sentence in sentences if sentence]

# remove the last element from each item in the list because the last words were taken along with the punctuation mark
last_words = [word[:-1] for word in last_words_and_punctuation_marks]

# join the last words into a new sentence
new_sentence = ' '.join(last_words)

# add delimiter to the end of new sentence
new_sentence += r'.'

# find index of a sentence as an item of the list after that I need to add new sentence
necessary_sentence = None
for sentence in sentences:
    if sentence.endswith("END OF this Paragraph."):
        necessary_sentence = sentence
        break
    else:
        pass

necessary_sentence_index = sentences.index(necessary_sentence)

# add new sentence into particular part of the raw text
sentences.insert(necessary_sentence_index + 1, new_sentence)

# use loop to capitalize each separated sentence from the sentences
normalized_sentences = [sentence.capitalize() for sentence in sentences]

# replace 'iz' with 'is' where it is needed
# loop throw every word in every sentence
for word in range(len(normalized_sentences)):
    if ' iz ' in normalized_sentences[word]:
        normalized_sentences[word] = normalized_sentences[word].replace('iz', 'is')

# join sentences to fully normalize the text
normalized_text = ' '.join(normalized_sentences)

# find number of whitespaces in the original raw text
whitespaces_quantity = len(re.findall(r'\s', normalized_text))

# check results
print(normalized_text)
print(whitespaces_quantity)