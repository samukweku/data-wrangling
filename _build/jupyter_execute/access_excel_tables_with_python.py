#!/usr/bin/env python
# coding: utf-8

# # **Access Excel Tables with Python**

# This post is about extracting data from Excel tables into Python. Source data is with permission from [ExcelisFun](https://www.youtube.com/watch?v=nBu1Bqa1jjs&t=1780s)

# Excel Tables are a great way of grouping related data, as it makes analysis easier. Usually,these tables will have names to identify them, as well as some other cool features. An example image is shown below:

# ![ExcelTables.png](images/xlsx_table.png)<br><br>
# 
# 
# Source : [support.office.com](https://support.office.com/en-us/article/overview-of-excel-tables-7ab0bb7d-3a9e-4b56-a3c9-6c94334e492c)

# ![ExcelTables.png](images/excelisfun_image.png)<br><br>
# 
# 
# Data Source : [ExcelisFun](https://www.youtube.com/watch?v=nBu1Bqa1jjs&t=1780s)

# In the image above, there are a couple of Excel tables, with defined names - SalesRep, Products, Category, and Supplier tables. How do we read this into Python?

# ### **Option 1 - The Naive way:**

# Let's read it into pandas

# In[1]:


import pandas as pd


# In[2]:


filename = "data/016-MSPTDA-Excel.xlsx"


# In[3]:


df = pd.read_excel(filename, sheet_name = "Tables", engine='openpyxl')

df.head()


# Notice how Pandas did not identify the tables - it just pulled in everything, even the empty columns. Also note the mangling of column names(*SupplierID.1*, *CategoryID.1*). This is not good enough. Yes, we could fix it, probably use the empty rows as a means of splitting the dataframe into new dataframes, but that is not wise. How do we truly know where one table starts and the other ends? Surely there has to be a better way. Thankfully there is.

# ## **Option 2 - The better way :**

# [pyjanitor](https://pyjanitor-devs.github.io/pyjanitor/) has a [xlsx_table](https://pyjanitor-devs.github.io/pyjanitor/api/io/#janitor.io.xlsx_table) functions that allows easy extraction of excel tables:

# In[4]:


# pip install git+https://github.com/pyjanitor-devs/pyjanitor.git
from janitor import xlsx_table

xlsx_table(filename, sheetname = 'Tables', table = 'dCategory')


# All the tables can also be read once, into a dictionary:

# In[5]:


out = xlsx_table(filename, 'Tables')


# In[6]:


out.keys()


# In[7]:


out['dSupplier']


# In[8]:


out['dProduct']


# In[9]:


out['dSalesReps']


# In[ ]:




