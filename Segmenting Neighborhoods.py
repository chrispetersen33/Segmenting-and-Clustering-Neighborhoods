#!/usr/bin/env python
# coding: utf-8

# # Segmenting and Clustering Neighborhoods in Toronto

# The purpose of this notebook is to scrape the following Wikipedia page, https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M, in order to obtain the data that is in the table of postal codes and to transform the data into a pandas dataframe.

# ### Import Libraries

# In[1]:


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


# #### Scrape the Wikipedia page

# #### Load the page to the soup

# In[2]:


wiki_link = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
page = requests.get(wiki_link).text
soup = BeautifulSoup(page, 'html5lib')
#print(soup.prettify())


# #### Get the postal code table

# In[3]:


table = soup.find('table', class_='wikitable')
#print(table.prettify())


# In[4]:


row = []
for tr in table.find_all('tr'):
	td = tr.find_all('td')
	row.append([tr.text.strip() for tr in td if tr.text.strip()])
#row


# #### Tranform the data into a pandas dataframe

# #### Create the dataframe

# #### The dataframe consists of three columns: PostalCode, Borough, and Neighborhood

# In[5]:


df = pd.DataFrame(data=row, columns=['PostalCode', 'Borough', 'Neighborhood'])
df.head(10)


# In[6]:


df.shape


# In[7]:


df = df.drop([0])
df.head(10)


# In[8]:


df = df[df.Borough != 'Not assigned']
df.head(10) # row 1, 2 and 10 will be removed


# More than one neighborhood can exist in one postal code area. For example, in the table on the Wikipedia page, M5A is listed twice and has two neighborhoods: Harbourfront and Regent Park. These two rows will be combined into one row with the neighborhoods separated with a comma.

# In[11]:


df = df.groupby(['PostalCode','Borough'])['Neighborhood'].apply(','.join).reset_index()
df[df.PostalCode=='M5A'] 
# check if M5A has two neighborhoods in one row


# If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough. So for the 9th cell in the table on the Wikipedia page, the value of the Borough and the Neighborhood columns will be Queen's Park.

# In[12]:


df.loc[df.Neighborhood == 'Not assigned', 'Neighborhood'] = df.Borough
df[df.Borough=='Queen\'s Park'] 
# check if the Borough and the Neighborhood columns are both Queen's Park


# In[13]:


df.shape


# In[ ]:




