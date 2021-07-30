#!/usr/bin/env python
# coding: utf-8

# # Filtering Rows in Pandas

# This article highlights various ways to filter rows in [Pandas](https://pandas.pydata.org/docs/user_guide/index.html#user-guide). The examples used here are based off the excellent [article](https://suzan.rbind.io/2018/02/dplyr-tutorial-3/) by [Susan Baert](https://twitter.com/SuzanBaert).
# 
# The data file can be accessed [here](https://github.com/samukweku/data_files/raw/master/msleep.txt)

# ## **Basic Row Filters**

# In[1]:


import pandas as pd 
import numpy as np 
import janitor


# In[2]:


file_path = "https://github.com/samukweku/data_files/raw/master/msleep.txt"

df = pd.read_csv(file_path)

df.head()


# ### Filtering Rows Based on a Numeric Variable

# You can filter numeric variables based on their values. A number of commonly used operators include: >, >=, <, <=, == and !=.

# In[3]:


df.loc[df.sleep_total > 18,  ["name", "sleep_total"]]


# Another option is to use the [query](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) method:

# In[4]:


df.filter(["name", "sleep_total"]).query('sleep_total > 18')


# Or [filter_on](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.filter_on.html#janitor.filter_on), which is just a wrapper around the [query](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) method,  from [pyjanitor](https://pyjanitor.readthedocs.io/):

# In[5]:


df.select_columns(["name", "sleep_total"]).filter_on('sleep_total > 18')


# ```{note}
# [loc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html) is significantly faster,especially when the number of rows are small
# ```

# To select a range of values, you can use two logical requirements; in the example below, only rows where `sleep_total` is greater than or equal to 16, and less than or equal to 18 are selected:

# In[6]:


df.loc[(df.sleep_total >= 16) & (df.sleep_total <= 18),  ["name", "sleep_total"]]


# An easier solution to the above is to use the [between](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.between.html) method:

# In[7]:


df.loc[df.sleep_total.between(16, 18),  ["name", "sleep_total"]]


# The [query](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) method offers a nice syntax for this as well:

# In[8]:


df.filter(["name", "sleep_total"]).query('16 <= sleep_total <= 18')


# There are scenarios where you may want to select rows where the value is nearly a given value. You may also want to specify a tolerance value to indicate how far the values can be. [numpy.isclose](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html) is a handy function for this:

# Let's say the tolerance should be within one standard deviation of 17:

# In[9]:


# calculate tolerance
tolerance = df['sleep_total'].std()

df.loc[np.isclose(df['sleep_total'], 17, atol = tolerance), ["name", "sleep_total"]]


# ### Filtering based on String Matches

# You can select on string matches as well; in the example below, the ``==`` comparison operator is used to select a specific group of animals:

# In[10]:


df.loc[df.order == "Didelphimorphia",  ["order", "name", "sleep_total"]]


# The [query](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) method works here as well:

# In[11]:


df.filter(["order", "name", "sleep_total"]).query('order == "Didelphimorphia"')


# Other operators can be used:

# In[12]:


df.loc[df.order != "Rodentia",  ['order', 'name', 'sleep_total']]


# In[13]:


df.loc[df['name'] > 'V',  ['order', 'name', 'sleep_total']]


# In the examples above, only one animal is used; to select more animals, you could pass a list of conditions, with the `|` (or) symbol:

# In[14]:


rows = (df.order == "Didelphimorphia") | (df.order == "Diprotodontia")

columns = ['order', 'name', 'sleep_total']

df.loc[rows, columns]


# However, this can become unwieldy, as the number of animals increase. The [isin](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.isin.html) method makes this easy:

# In[15]:


df.loc[df.order.isin(["Didelphimorphia", "Diprotodontia"]), ["order", "name", "sleep_total"]]


# The [query](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) method offers a nice syntax for this with python's [in](https://docs.python.org/3/reference/expressions.html#membership-test-operations) function:

# In[16]:


(df.filter(["order", "name", "sleep_total"])
   .query('order in ["Didelphimorphia", "Diprotodontia"]')
)


# You could also use the ``==`` operator:

# In[17]:


(df.filter(["order", "name", "sleep_total"])
   .query('order == ["Didelphimorphia", "Diprotodontia"]')
)


# You can also deselect certain groups using the [isin](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.isin.html) function, and combine it with the `~` symbol:

# In[18]:


(df.loc[~df.order.isin(("Rodentia", "Carnivora", "Primates")),  ['order', 'name', 'sleep_total']]
   .head(10)
)


# With the [query](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) method:

# In[19]:


(df.filter(['order', 'name', 'sleep_total'])
   .query('order not in ("Rodentia", "Carnivora", "Primates")')
   .head(10)
)


# In[20]:


(df.filter(('order', 'name', 'sleep_total'))
   .query('order != ("Rodentia", "Carnivora", "Primates")')
   .head(10)
)


# The [filter_column_isin](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.filter_column_isin.html#janitor.filter_column_isin) function from [pyjanitor](https://pyjanitor.readthedocs.io/index.html), which is just a wrapper around [isin](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.isin.html),  is an alternative:

# In[21]:


(df.filter(('order', 'name', 'sleep_total'))
   .filter_column_isin(column_name = 'order', 
                       iterable = ("Rodentia", "Carnivora", "Primates"),
                       complement = True)
   .head(10)
)


# ### Filtering Rows Based on Regex

# There are scenarios where you need to filter string columns based on partial matches; Pandas has a wealth of [string methods](https://pandas.pydata.org/pandas-docs/stable/user_guide/text.html#method-summary) that support regular expressions, and can be used in these situations.
# 
# Let's filter for rows where `mouse` can be found in the column `name`:

# In[22]:


df.loc[df['name'].str.contains('mouse', case = False), ['name', 'sleep_total']]


# ```{margin} Note: Pyjanitor Function
# [filter_string](https://pyjanitor.readthedocs.io/reference/janitor.functions/janitor.filter_string.html#janitor.filter_string) 
# is a wrapper around the [Series.str.contains](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.contains.html#pandas.Series.str.contains) method, 
# 
# and can be handy in method chaining operations.
# ```

# With the [query](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) method:

# In[23]:


df.filter(['name', 'sleep_total']).query('name.str.contains("mouse", case = False)', engine = 'python')


# ### Filtering Rows based on Multiple Conditions

# Select rows with a `bodywt` above 100 and either have a `sleep_total` above 15, or are not part of the `Carnivora` `order`:

# In[24]:


rows = (df.bodywt > 100) & ((df.sleep_total > 15) | (df.order != "Carnivora"))

columns = ["name", "order", slice("sleep_total", "bodywt")]

df.select_columns(columns).loc[rows]


# With the [query](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) method:

# In[25]:


(df.select_columns(["name", "order", slice("sleep_total", "bodywt")])
   .query('bodywt > 100 and (sleep_total > 15 or order != "Carnivora")')
)


# Return rows where `bodywt` is either greater than 100 or `brainwt` greater than 1, but not both:

# In[26]:


rows = np.logical_xor((df.bodywt > 100), (df.brainwt > 1))

columns = ["name", "bodywt", "brainwt"]

df.loc[rows, columns]


# An alternative to the solution above, using the `!=` operator:

# In[27]:


rows = (df.bodywt > 100) != (df.brainwt > 1)

columns = ["name", "bodywt", "brainwt"]

df.loc[rows, columns]


# With the [query](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) method:

# In[28]:


(df.filter(["name", "bodywt", "brainwt"])
   .query('(bodywt > 100) != (brainwt > 1)')
)


# Select all rows where `brainwt` is larger than 1, but `bodywt` does not exceed 100:

# In[29]:


rows = ~(df.bodywt > 100) & (df.brainwt > 1)

columns = ["name", "sleep_total", "brainwt", "bodywt"]

df.loc[rows, columns]


# An alternative to the solution above:

# In[30]:


rows = (df.bodywt <= 100) & (df.brainwt > 1)

columns = ["name", "sleep_total", "brainwt", "bodywt"]

df.loc[rows, columns]


# In[31]:


(df.filter(["name", "sleep_total", "brainwt", "bodywt"])
   .query('bodywt <= 100 and brainwt > 1')
)


# ### Filtering out Empty Rows

# Empty rows can be filtered out with the [notna](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.notna.html#pandas.DataFrame.notna) function:

# In[32]:


rows = df.conservation.notna()

columns = ["name", slice("conservation", "sleep_cycle")]

df.select_columns(columns).loc[rows].head(10)


# In[33]:


df.select_columns(columns).query('conservation.notna()', engine = 'python').head(10)


# ## Filtering across Multiple Columns

# ### Filter across all Columns

# It is possible to filter for rows based on values across columns.
# 
# Let's filter for rows across the selected columns, keeping only rows where any column has the pattern `Ca` inside:

# In[34]:


(df.select_columns([slice('name', 'order'), 'sleep_total'])
   .drop(columns='vore')
   .loc[lambda df: df.select_dtypes('object')
                     .transform(lambda x: x.str.contains('Ca'))
                     .any(axis = 'columns')
        ]
)


# The code above works great; however, we could abstract this further with a function:

# In[35]:


def filter_rows(df, dtype, columns, condition, any_True = True):
    temp = df.copy()
    if dtype:
        temp = df.select_dtypes(dtype)
    if columns:
        booleans = temp.loc[:, columns].transform(condition)
    else:
        booleans = temp.transform(condition)
    if any_True:
        booleans = booleans.any(axis = 1)
    else:
        booleans = booleans.all(axis = 1)
        
    return df.loc[booleans]


# In[36]:


(df.select_columns([slice('name', 'order'), 'sleep_total'])
   .drop(columns = 'vore')
   .pipe(filter_rows,
         dtype = 'object',
         columns = None,
         condition = lambda df: df.str.contains('Ca'),
         any_True = True
        )
)


# Let's look at another example, to filter for rows, across selected columns, where any column has a value less than 0.1:

# In[37]:


(df.select_columns(['name', slice('sleep_total', 'bodywt')])
   .pipe(filter_rows,
         dtype = 'number',
         columns = None,
         condition = lambda df: df < 0.1,
         any_True = True
        )
   .head(10)
)


# The above example only requires that at least one column has a value less than 0.1. What if the goal is to return only rows where all the columns have values above 1? 

# In[38]:


(df.select_columns(['name', slice('sleep_total', 'bodywt')])
   .drop(columns = 'awake')
   .pipe(filter_rows,
         dtype = 'number',
         columns = None,
         condition = lambda df: df > 1,
         any_True = False
        )
)


# Return rows where the string columns contain null values:

# In[39]:


(df.select_columns([slice('name', 'order'), slice('sleep_total', 'sleep_rem')])
   .pipe(filter_rows,
         dtype = "object",
         columns = None,
         condition = lambda df: df.isna(),
         any_True = True
        )
)


# ### Filter at

# It is also possible to filter rows based on specific columns:

# In[40]:


(df.select_columns(['name', 
                    slice('sleep_total', 'sleep_rem'), 
                    slice('brainwt', 'bodywt')]
                    )
   .loc[lambda df: df.filter(['sleep_rem', 'sleep_total'])
                     .gt(5)
                     .all(axis = 'columns')
        ]
)


# With the [query](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) method:

# In[41]:


(df.select_columns(['name', 
                    slice('sleep_total', 'sleep_rem'), 
                    slice('brainwt', 'bodywt')]
                    )
   .query('sleep_total > 5 and sleep_rem > 5')
)


# Or, using the function created earlier:

# In[42]:


(df.select_columns(['name', 
                    slice('sleep_total', 'sleep_rem'), 
                    slice('brainwt', 'bodywt')]
                    )
   .pipe(filter_rows,
         dtype = None,
         columns = ['sleep_total', 'sleep_rem'],
         condition = lambda df: df > 5,
         any_True = False
        )
)


# Another example below that uses a different option when selecting the columns to filter at:

# In[43]:


(df.select_columns(['name', 
                    slice('sleep_total', 'sleep_rem'), 
                    slice('brainwt', 'bodywt')]
                    )
   .loc[lambda df: df.filter(like='sleep')
                     .gt(5)
                     .all( axis = 'columns')
        ]
)


# In[44]:


(df.select_columns(['name', 
                    slice('sleep_total', 'sleep_rem'), 
                    slice('brainwt', 'bodywt')]
                    )
   .pipe(filter_rows,
         dtype = None,
         columns = lambda df: df.columns.str.contains('sleep'),
         condition = lambda df: df > 5,
         any_True = False
        )
)


# Resources: 
# 
# - [pandas docs](https://pandas.pydata.org/docs/user_guide/index.html#user-guide) -  version ``1.2.3``
# - [pyjanitor functions](https://pyjanitor.readthedocs.io/reference/general_functions.html) - version ``0.20.13``
# - [numpy](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html) - version ``1.20.0``
