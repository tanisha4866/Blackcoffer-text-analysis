#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from bs4 import BeautifulSoup as bs

urls=[]
url_file=pd.read_excel(r'C:\\Users\\ragha\\Downloads\\Input.xlsx')
for i in url_file:
    urls.append(i)
    
#url extraction
    
import requests
urls=[]
url_file=pd.read_excel(r'C:\\Users\\ragha\\Downloads\\Input.xlsx')
for i in url_file['URL']:
    urls.append(i)

#function to fetch the html

def yip(urls):
    coursereq = requests.get(urls)
    coursecontent = coursereq.content
    coursereqs = bs(coursecontent, "html.parser")
    return coursereqs

html=[]
for i in urls:
    html.append(yip(i))

#content & title
content=[]
title=[]
for i in html:
    title.append(i.find('h1',{'class':'entry-title'}))
    content.append(i.find('div',{'class':'td-post-content tagdiv-type'}))
    


# In[ ]:


import nltk
from nltk import word_tokenize,sent_tokenize
import string
nltk.download('stopwords')
from nltk.corpus import stopwords 
from itertools import count
import operator as op

#function to perform the whole task

def text_analysis(content):
   
    # extraction of text
    text = content.text
    text = text.replace('\n',' ')

    # tokeization
    sent=sent_tokenize(text)
    word=(word_tokenize(text))
    word = [words.lower() for words in word]

    # Removing punctuation
    def remove_punctuation(input_string):
        translator = str.maketrans("", "", string.punctuation)
        result = input_string.translate(translator)
        return result

    without_punctuation_text = remove_punctuation(text)


    #mergeing stopwords 
    
    custom_stopwords= str(pd.read_csv(r'C:\Users\ragha\Desktop\stopwords.txt')).split()
    total_stopwords = nltk.corpus.stopwords.words('english')
    total_stopwords.extend(custom_stopwords)
    total_stopwords = [words.lower() for words in total_stopwords]

    # removing stopwords from the text 
    removing_custom_words=[]

    for words in word:
        if not words in total_stopwords:
            removing_custom_words.append(words)

    #calculating formulas

    negative = pd.read_excel(r'C:\\Users\\ragha\\Downloads\\negative-words.xlsx')
    negative=list(negative['Words'])
    positive = pd.read_excel(r'C:\\Users\\ragha\\Downloads\\positive-words.xlsx')
    positive=list(positive['Words'])

    def count_items_in_list(input_list, item):
        countt = input_list.count(item)
        return countt

    negative_score=[]
    positive_score=[]

    for i in negative:
        item_count = count_items_in_list(removing_custom_words, i)
        if item_count>0:
            negative_score.append(item_count)

    for i in positive:
        item_count = count_items_in_list(removing_custom_words, i)
        if item_count>0:
            positive_score.append(item_count)

    #negative_score
    negative_score=sum(negative_score)

    # positive_score
    positive_score=sum(positive_score)

    # Polarity_Score
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

    # subjectivity_score
    subjectivity_score = (positive_score + negative_score)/ ((len(removing_custom_words)) + 0.000001)

    # Average_Sentence_Length
    average_sentence_length = (len(removing_custom_words) / len(sent))
    
    #removing words with 'ed' and 'es' 
    new_text_for_vowels=[w for w in removing_custom_words if not w.endswith('ed' or 'es')]
 
    #syllable_per_word
    def Check_Vow(string, vowels):
        final = [each for each in string if op.countOf(vowels, each) > 0]
        complex_words.append(len(final))

    vowels = "aeiou"
    complex_words=[]
    for i in new_text_for_vowels:
        Check_Vow(i,vowels)

    complex_words=[w for w in complex_words if  (w>2)]
    complex_words_count=sum(complex_words)
    syllable_per_word = sum(complex_words)/len(removing_custom_words)
    
    #percentage_of_complex_words
    percentage_of_complex_words =(len(complex_words) / len(removing_custom_words))

    #fog_index
    fog_index = 0.4 * (average_sentence_length + percentage_of_complex_words)

    #average_number_of_words_per_sentence
    average_number_of_words_per_sentence = len(without_punctuation_text) /len(sent)

    #pronouns_count
    pronouns = ["i" ,'we', 'my', 'ours', 'us']
    pronouns_count=[]

    for i in pronouns:
        items = count_items_in_list(text, i)
        if items>0:
            pronouns_count.append((items))

    pronouns_count=sum(pronouns_count)

    #character
    def check_freq(x):
        freq = {}
        for c in set(x):
            freq[c] = x.count(c)
        return freq

    lettercount = check_freq(without_punctuation_text)
    total_letter = sum(lettercount.values())

    #average_word_length
    average_word_length = total_letter/ len((removing_custom_words))
    
    #word_count
    word_count = len(removing_custom_words)

    Negative_Score.append(negative_score) 
    Positive_Score.append(positive_score)
    Polarity_Score.append(polarity_score)
    Subjectivity_Score.append(subjectivity_score)
    Average_Sentence_Length.append(average_sentence_length)
    Complex_Words.append(complex_words_count)
    Syllable_Per_Word.append(syllable_per_word)
    Percentage_Of_Complex_Words.append(percentage_of_complex_words)
    Fog_Index.append(fog_index)
    Average_Number_of_Words_Per_Sentence.append(average_number_of_words_per_sentence)
    Pronouns_Count.append(pronouns_count)
    Average_Word_Length.append(average_word_length)
    Word_Count.append(word_count)

    return negative_score

Negative_Score=[]
Positive_Score=[]
Polarity_Score=[]
Subjectivity_Score=[]
Average_Sentence_Length=[]
Complex_Words=[]
Percentage_Of_Complex_Words=[]
Fog_Index=[]
Average_Number_of_Words_Per_Sentence=[]
Pronouns_Count=[]
Average_Word_Length=[]
Word_Count=[]
Syllable_Per_Word=[]

error ={}
for i in content:
    try:
        print(text_analysis(i))
    except:
        continue



# In[ ]:



final_dataframe ={'POSITIVE SCORE':Positive_Score,'NEGATIVE SCORE' : Negative_Score,'POLARITY SCORE':Polarity_Score,'SUBJECTIVITY SCORE':Subjectivity_Score,'AVG SENTENCE LENGTH':Average_Sentence_Length,'COMPLEX WORD COUNT': Complex_Words,'PERCENTAGE OF COMPLEX WORDS':Percentage_Of_Complex_Words,'FOG INDEX':Fog_Index,'AVG NUMBER OF WORDS PER SENTENCE':Average_Number_of_Words_Per_Sentence,'WORD COUNT':Word_Count,'SYLLABLE PER WORD':Syllable_Per_Word,'PERSONAL PRONOUNS':Pronouns_Count,'AVG WORD LENGTH':Average_Word_Length}
final_dataframe=pd.DataFrame(final_dataframe)

final_dataframe.to_excel('Blackcoffer_text_analysis.xlsx')

