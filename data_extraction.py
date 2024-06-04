#!/usr/bin/env python
# coding: utf-8

# # DATA EXTRACTION

# Importing the neceassary modules

# In[1]:


import pandas as pd
import requests


# In[2]:


import os
from bs4 import BeautifulSoup


# Storing the URLS required

# In[3]:


input_df=pd.read_excel('Input.xlsx')


# In[4]:


input_df


# Make a directory for the articles extracted

# In[5]:


if not os.path.exists('articles'):
    os.makedirs('articles')


# Function to extract articles text

# In[6]:


def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extracting title and body text
    title = soup.find('h1').get_text() if soup.find('h1') else ''
    body = ' '.join(p.get_text() for p in soup.find_all('p'))
    list_items = soup.find_all('li')

    # Extract and print text from each <li> tag, including all nested tags
    item_text=[]
    for item in list_items:
        item_text.append(item.get_text(separator=" ", strip=True))
        #print(item_text)
    paragraph=' '.join(item_text)
    return f"{title}\n{body}\n{paragraph}"


# In[7]:


#iterating over the urls
for  _,row in input_df.iterrows():
    url,url_id=row['URL'],row['URL_ID']
    try:
        article_text=extract_article_text(url)
        with open(f'articles/{url_id}.txt', 'w', encoding='utf-8') as file:
            file.write(article_text)
        print(f"Article text extracted and saved for URL_ID {url_id}")
    except Exception as e:
        print(f"Error extracting article text for URL_ID {url_id}: {e}")

