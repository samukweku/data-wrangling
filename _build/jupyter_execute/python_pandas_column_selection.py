#!/usr/bin/env python
# coding: utf-8

# # Column Selection in Pandas - and Pyjanitor

# *Updated July 30 2021*

# This article highlights various ways to select columns using [Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html#user-guide) and [Pyjanitor](https://pyjanitor.readthedocs.io/). 
# 
# [Pyjanitor](https://pyjanitor.readthedocs.io/) is an open-source project that extends Pandas chaining methods with a verb-based API.
# 
# The examples used here are based off the excellent [article](https://suzan.rbind.io/2018/01/dplyr-tutorial-1/) by [Susan Baert](https://twitter.com/SuzanBaert).
# 
# The data file can be accessed [here](https://github.com/samukweku/data_files/raw/master/msleep.txt)

# ## **Selecting Columns**

# In[1]:


import pandas as pd
import re
import janitor

file_path = "https://github.com/samukweku/data_files/raw/master/msleep.txt"
df = pd.read_csv(file_path)
df.head(5)


# In Pandas, you can select columns by label with [loc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html) or position with [iloc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html#pandas.DataFrame.iloc):

# In[2]:


# selecting a single label returns a Series

df.loc[:, 'genus'].head()


# In[3]:


# Selecting a single position returns a Series

df.iloc[:, 1].head()


# In[4]:


df.iloc[:, -10].head()


# In[5]:


# Selecting a list returns a DataFrame

df.loc[:, ['genus']].head()


# In[6]:


df.iloc[:, [-10]].head()


# You can also select single columns with Pyjanitor's [select_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.select_columns.html#janitor.select_columns); a dataframe is always returned:

# In[7]:


df.select_columns('genus').head()


# **Note:** [select_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.select_columns.html#janitor.select_columns) only works with labels, and accepts a string, a regular expression, a slice, a function, or a combination of any of the previous options. If a function is provided, the function should be applicable to every series in the dataframe.

# You can select columns by passing a list of the column names:

# In[8]:


columns_to_select = ["name", "genus", "sleep_total", "awake"]

df.loc[:, columns_to_select].head()


# Same applies with Pyjanitor's [select_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.select_columns.html#janitor.select_columns):

# In[9]:


df.select_columns(columns_to_select).head()


# You can pass a list/tuple of booleans; only the columns that pair with `True` are selected:

# In[10]:


columns_to_select = [True, True, False, False, False, True,False,True,True,False,False]

df.loc[:, columns_to_select].head()


# You can select chunks of columns using python's [slice](https://docs.python.org/3/library/functions.html#slice) syntax or via the ``start:end`` shortcut:

# In[11]:


df.loc[:, slice("name", "order")].head()


# In[12]:


df.loc[:, "name" : "order"].head()


# In[13]:


df.iloc[:, :4].head()


# Pyjanitor's [select_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.select_columns.html#janitor.select_columns) does not support the slice shortcut syntax, you have to use the [slice](https://docs.python.org/3/library/functions.html#slice) function:

# In[14]:


df.select_columns(slice("name", "order")).head()


# Pandas accepts a single slice object in column selection; for multiple slice selections, Pyjanitor's [select_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.select_columns.html#janitor.select_columns) comes in handy:

# In[15]:


df.select_columns(slice("name", "order"), slice("sleep_total", "sleep_cycle")).head()


# To deselect/drop a chunk of columns you can set `invert=True` in Pyjanitor's [select_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.select_columns.html#janitor.select_columns) :

# In[16]:


df.select_columns(slice("sleep_total", "awake"), "conservation", invert = True).head()


# ### Selecting Columns based on Partial Names

# Pandas has a [filter](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.filter.html) function that makes column selection with partial matching easy:

# In[17]:


df.filter(like = 'sleep').head()


# Of course, you can select with Pandas [loc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html) or Pyjanitor's [select_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.select_columns.html#janitor.select_columns), in combination with Pandas' [string methods](https://pandas.pydata.org/pandas-docs/stable/user_guide/text.html):

# In[18]:


# this returns a list of booleans
columns_to_select = df.columns.str.contains('sleep')

df.loc[:, columns_to_select].head()


# With Pyjanitor's [select_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.select_columns.html#janitor.select_columns), you can pass a function that targets each individual Series in the dataframe:

# In[19]:


# this searches through each Series' name for matches
columns_to_select = lambda df: 'sleep' in df.name

df.select_columns(columns_to_select).head()


# Pyjanitor's [select_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.select_columns.html#janitor.select_columns) supports shell-like glob strings(`*`) for column selection, which can come in handy for easy column selection:

# In[20]:


df.select_columns('*sleep*').head()


# Let's look at some more examples:

# In[21]:


columns_to_select = df.columns.str.contains("eep") | (df.columns.str.endswith('wt'))

df.loc[:, columns_to_select].head()


# In[22]:


columns_to_select = lambda df: 'eep' in df.name or df.name.endswith('wt')

df.select_columns(columns_to_select).head()


# In[23]:


# shell-like glob strings
df.select_columns("*eep*", "*wt").head()


# ### Selecting Columns based on Regex

# Pandas' [filter](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.filter.html) also accepts a regular expression:

# In[24]:


df.filter(regex = 'eep|wt$').head()


# You can also pass a regular expression to Pandas [loc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html) or Pyjanitor's [select_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.select_columns.html#janitor.select_columns):

# In[25]:


columns_to_select = df.columns.str.contains("eep|wt$")

df.loc[:, columns_to_select].head()


# Selection with Pyjanitor's [select_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.select_columns.html#janitor.select_columns) requires the use of [re.compile](https://docs.python.org/3/library/re.html#re.compile); underneath the hood, [re.search](https://docs.python.org/3/library/re.html#re.search) is used:

# In[26]:


df.select_columns(re.compile(r"eep|wt$")).head()


# The code samples below will select any column that contains an ‘o’, followed by one or more other letters, and ‘er’.

# In[27]:


columns_to_select = df.columns.str.contains(r"o.+er")

df.loc[:, columns_to_select].head()


# In[28]:


df.select_columns(re.compile(r"o.+er")).head()


# In[29]:


df.filter(regex = r"o.+er").head()


# ### Selecting columns by their data type

# You can select columns by data type with Pandas' [select_dtypes](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjRwOK57ObuAhXPIbcAHRQNCQgQFjAAegQIARAC&url=https%3A%2F%2Fpandas.pydata.org%2Fpandas-docs%2Fstable%2Freference%2Fapi%2Fpandas.DataFrame.select_dtypes.html&usg=AOvVaw2R15nQ5DZFz9MUIUyQoM_u):

# In[30]:


# you have to use 'object' to select strings

df.select_dtypes('object').head()


# You can also select dtypes with Pyjanitor's [select_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.select_columns.html#janitor.select_columns), in conjunction with Pandas' [api types](https://pandas.pydata.org/pandas-docs/stable/reference/general_utility_functions.html#dtype-introspection) functions:

# In[31]:


# The function is applied to each Series in the DataFrame
df.select_columns(pd.api.types.is_string_dtype).head()


# You can select multiple data types:

# In[32]:


df.select_dtypes('number').head()


# In[33]:


df.select_columns(pd.api.types.is_numeric_dtype).head()


# You can remove columns based on their data type:

# In[34]:


df.select_dtypes(exclude = 'number').head()


# In[35]:


df.select_columns(pd.api.types.is_numeric_dtype, invert = True).head()


# ### Selecting columns by logical expressions

# The ideas expressed in the previous sections can be combined for some nifty column selection. 
# 
# Say we wish to select columns that are numeric, and have a mean greater than 10:

# In[36]:


# first select only numeric columns
# then select columns where the mean is greater than 10
(df
 .select_dtypes('number')
 .loc[:, lambda df: df.mean()>10]
 .head()
 )


# Alternatively, we can just get the column names and pass them directly to [loc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)

# In[37]:


columns_to_select = df.mean(numeric_only=True).loc[lambda s: s > 10].index

df.loc[:, columns_to_select].head()


# The same steps are possible with Pyjanitor's [select_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.select_columns.html#janitor.select_columns):

# In[38]:


(df
 .select_columns(pd.api.types.is_numeric_dtype)
 .select_columns(lambda df: df.mean() > 10)
 .head()
 )


# In[39]:


df.select_columns(columns_to_select).head()


# Let's look at another example, where we select only columns where the number of distinct values is less than 10; this uses booleans to select the relevant columns:

# In[40]:


df.loc[:, df.nunique() < 10].head()


# In[41]:


df.select_columns(df.nunique() < 10).head()


# ## **Reordering Columns**

# You can select columns in the order that you want:

# In[42]:


columns_to_select = ['conservation', 'sleep_total', 'name']

df.loc[:, columns_to_select].head()


# In[43]:


df.select_columns(columns_to_select).head()


# To move some columns to the front, you could use Pyjanitor's [reorder](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.reorder_columns.html#janitor.reorder_columns) function:

# In[44]:


df.reorder_columns(['conservation', 'sleep_total']).head()


# Or, you could write a function and use within Pandas:

# In[45]:


def move_to_the_front(frame, front_columns):
    column_names = list(frame.columns)
    for name in front_columns:
        column_names.remove(name)
    front_columns.extend(column_names)
    return front_columns


# In[46]:


df.loc[:, move_to_the_front(df, ['conservation', 'sleep_total'])].head()


# ## **Column Names**

# ### Renaming Columns

# Columns can be renamed with Pandas' [rename](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html) method and a dictionary, where you map the old column name to the new column name:

# In[47]:


(df
 .loc[:, ['name', 'sleep_total', 'conservation']]
 .rename(columns = {"name": "animal", "conservation": "extinction_threat"})
 .head()
 )


# Pyjanitor has a [rename_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.rename_columns.html#janitor.rename_columns) function, which is just syntactic sugar for Pandas' [rename](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html):

# In[48]:


(df
 .select_columns(['name', 'sleep_total', 'conservation'])
 .rename_columns({"name": "animal", "conservation": "extinction_threat"})
 .head()
 )


# If you are retaining all columns, then Pandas' [rename](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html) or Pyjanitor's [rename_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.rename_columns.html#janitor.rename_columns) is sufficient:

# In[49]:


df.rename(columns = {"name": "animal", "conservation": "extinction_threat"}).head()


# In[50]:


df.rename_columns({"name": "animal", "conservation": "extinction_threat"}).head()


# ### Reformatting all Column Names

# You can use python's string functions to reformat column names within Pandas' [rename](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html) function.
# 
# Let's convert all column names to uppercase:

# In[51]:


df.rename(columns = str.upper).head()


# Resources: 
# 
# - [Pandas loc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
# - [Pandas iloc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html#pandas.DataFrame.iloc)
# - [Pandas rename](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html)
# - [Pandas select_dtypes](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.select_dtypes.html)
# - [Pandas api types](https://pandas.pydata.org/pandas-docs/stable/reference/general_utility_functions.html#dtype-introspection)
# - [Pyjanitor select_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.select_columns.html#janitor.select_columns)
# - [Pyjanitor rename_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.rename_columns.html#janitor.rename_columns)
# - [Pyjanitor reorder_columns](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.reorder_columns.html)
# 
# - Based on Pandas 1.2.2 and Pyjanitor's latest dev version 0.21.0
