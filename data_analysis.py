#!/usr/bin/env python
# coding: utf-8

# # DATA ANALYSIS

# Importing all the required modules and packages for the the data analysis

# In[19]:


import re
import nltk
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
import os
import pandas as pd
import traceback
from sklearn.pipeline import Pipeline
import string


# downloading the punkt and stopwords fromm the nltk

# In[2]:


#download NLTk resourses
nltk.download('punkt')
nltk.download('stopwords')


# Creating a function in order to create segregate and store the positive and neagtive words

# In[3]:


def create_sentiment_dictionary():
        #load the provided positive and neagtive words
        with open('Master_Dictionary/positive-words.txt','r') as file:
            positive_words=set(word.strip() for word in file)
        with open('Master_Dictionary/negative-words.txt','r') as file:
            negative_words=set(word.strip() for word in file)
            
        return positive_words,negative_words


# To perform sentiment analysis using positive and negative words on the cleaned text

# In[4]:


#to perform sentimental analysis
def perfom_sentiment_analysis(text,positive_words,negative_words):
    words=nltk.word_tokenize(text)
    positive_score=sum(1 for word in words if word in positive_words)
    negative_score=sum(1 for word in words if word in negative_words)
    polarity_score=(positive_score-negative_score)/((positive_score+negative_score)+0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(words) + 0.000001)
    return positive_score, negative_score, polarity_score, subjectivity_score


# To append the dictionary structure of each article to the main list 

# In[5]:


def form_list_output_scores(text_output_metrics_cumulative,output_metrics):
    text_output_metrics_cumulative.append(output_metrics)


# To count the syllabes per word in the text

# In[6]:


def count_syllables_per_word(text):
    words=nltk.word_tokenize(text)
    total_cnt_syllables=0
    for word in words:
        if word.endswith("es") or word.endswith("ed"):
            continue
        else:
            total_cnt_syllables=total_cnt_syllables+count_syllables(word)
            
    syllables_count_per_word_metric=total_cnt_syllables/len(words)
    return syllables_count_per_word_metric


# To count syllables present in each word

# In[7]:


def count_syllables(word):
    cnt=sum(1 for letter in word if letter.lower() in 'aeioy')
    return cnt


# To count the complex words in the cleaned text

# In[8]:


def complex_word_count(text):
    words=nltk.word_tokenize(text)
    sum_complex_words=0
    for word in words:
        if count_syllables(word)>2:
            sum_complex_words=sum_complex_words+1
    return sum_complex_words


# Function to clean the extracted data using the libraries provided

# In[9]:


#function to clean the stop_words
def clean_text(text):
    #load the stop words
    stop_words=set()
    with open('stopwords/StopWords_Auditor.txt','r') as file:
        stop_words.add(word.strip() for word in file)
    with open('stopwords/StopWords_Currencies.txt','r') as file:
        stop_words.add(word.strip() for word in file)
    with open('stopwords/StopWords_DatesandNumbers.txt','r') as file:
        stop_words.add(word.strip() for word in file)
    with open('stopwords/StopWords_Generic.txt','r') as file:
        stop_words.add(word.strip() for word in file)
    with open('stopwords/StopWords_GenericLong.txt','r') as file:
        stop_words.add(word.strip() for word in file)
    with open('stopwords/StopWords_Geographic.txt','r') as file:
        stop_words.add(word.strip() for word in file)
    with open('stopwords/StopWords_Names.txt','r') as file:
        stop_words.add(word.strip() for word in file)
    tokens=word_tokenize(text.lower())
    cleaned_tokens=[]
    for token in tokens:
        cleaned_token=[charac for charac in token if charac not in string.punctuation]
        cleaned_token_string=''.join(cleaned_token)
        if cleaned_token_string.isalnum() and cleaned_token_string not in stop_words:
            cleaned_tokens.append(cleaned_token_string)
    cleaned_text=' '.join(cleaned_tokens)
    return cleaned_text


# In[10]:


def total_cleaned_words_cnt(text):
    words=nltk.word_tokenize(text)
    return len(words)


# Function to analyze readability

# In[11]:


def analyze_readibility(text):
    sentences=sent_tokenize(text)
    words=word_tokenize(text)
    avg_sentence_length=len(words)/len(sentences)
    complex_word_count=sum(1 for word in words if count_syllables(word)>2)
    percentage_complex_words = (complex_word_count / len(words)) * 100
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    return avg_sentence_length, percentage_complex_words, fog_index


# In[12]:


def avg_words_per_sentence(text):
    words=nltk.word_tokenize(text)
    sentences=nltk.sent_tokenize(text)
    avg_words_p_sentence=len(words)/len(sentences)
    return avg_words_p_sentence


# function to count personal pronouns

# In[13]:


def count_personal_pronouns(text):
    personal_pronouns=['i','we','my','ours','us']
    personal_pronoun_sum=0
    words=nltk.word_tokenize(text)
    for word in words:
        if word=='US':
            continue
        elif word.lower() in personal_pronouns:
            personal_pronoun_sum=personal_pronoun_sum+1
        
    return personal_pronoun_sum


# function to calculate the average word length

# In[14]:


def calculate_avg_word_length(text):
    word_token=word_tokenize(text)
    total_word_length=sum(len(word) for word in word_token)
    avg_word_length=total_word_length/len(word_token)
    return avg_word_length


# Main function

# In[22]:


def main():
    text_output_metrics_cumulative=[]
    if not os.path.exists('cleaned_texts'):
        os.makedirs('cleaned_texts')
    article_dir = 'articles/'
    articles_dir_loaded = os.listdir(article_dir)
    
    for file_name in articles_dir_loaded:
        try:
            with open(f'{article_dir}/{file_name}', 'r', encoding='utf-8', errors='ignore') as file:
                text = file.read()
                cleaned_text = clean_text(text)
                
                with open(f'cleaned_texts/{file_name}', 'w', encoding='utf-8', errors='ignore') as cleaned_file:
                    cleaned_file.write(cleaned_text)
                    
                # Creating a sentiment dictionary
                positive_words, negative_words = create_sentiment_dictionary()
                positive_score, negative_score, polarity_score, subjectivity_score = perfom_sentiment_analysis(cleaned_text, positive_words, negative_words)
                avg_sentence_length, percentage_complex_words, fog_index=analyze_readibility(cleaned_text)
                avg_words_p_sentence=avg_words_per_sentence(cleaned_text)
                sum_complex_words=complex_word_count(cleaned_text)
                word_count=total_cleaned_words_cnt(cleaned_text)
                syllables_count_per_word_metric=count_syllables_per_word(cleaned_text)
                pronoun_pronoun_sum=count_personal_pronouns(cleaned_text)
                avg_word_length=calculate_avg_word_length(cleaned_text)
                #Append the scores to the list
                output_metrics = {
                        'FILENAME': file_name,
                        'POSITIVE SCORE': positive_score,
                        'NEGATIVE SCORE': negative_score,
                        'POLARITY SCORE': polarity_score,
                        'SUBJECTIVITY SCORE': subjectivity_score,
                        'AVG SENTENCE LENGTH':avg_sentence_length,
                        'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
                        'FOG INDEX': fog_index,
                        'AVG NUMBER OF WORDS PER SENTENCE': avg_words_p_sentence,
                        'COMPLEX WORD COUNT': sum_complex_words,
                        'WORD COUNT': word_count,
                        'SYLLABLE PER WORD': syllables_count_per_word_metric,
                        'PERSONAL PRONOUNS': pronoun_pronoun_sum,
                        'AVG WORD LENGTH': avg_word_length
                }
                form_list_output_scores(text_output_metrics_cumulative,output_metrics)           
        except Exception as e:
            traceback.print_exc()
            print(e)
    print(text_output_metrics_cumulative)
    # Create a DataFrame and save it to an Excel file
    df = pd.DataFrame(text_output_metrics_cumulative)
    output = 'text_output_metrics_cumulative.csv'
    df.to_csv(output)  
            


# In[23]:


if __name__=='__main__':
    main()
    


# In[ ]:





# In[ ]:




