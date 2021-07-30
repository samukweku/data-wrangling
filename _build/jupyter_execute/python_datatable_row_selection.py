#!/usr/bin/env python
# coding: utf-8

# # Filtering Rows in Datatable

# *Updated 30 July 2021*

# This article highlights various ways to filter rows in python [datatable](https://datatable.readthedocs.io/en/latest/). The examples used here are based off the excellent [article](https://suzan.rbind.io/2018/02/dplyr-tutorial-3/) by [Susan Baert](https://twitter.com/SuzanBaert).
# 
# The data file can be accessed [here](https://github.com/samukweku/data_files/raw/master/msleep.txt)

# ## **Basic Row Filters**

# In[1]:


from datatable import dt, f
from operator import and_, or_, xor, eq
from functools import reduce
import re


# In[2]:


file_path = "https://github.com/samukweku/data_files/raw/master/msleep.txt"

DT = dt.fread(file_path)

DT.head(5)


# ### Filtering Rows Based on a Numeric Variable

# You can filter numeric variables based on their values. A number of commonly used operators include: >, >=, <, <=, == and !=.
# 
# Note that in datatable, filtration occurs in the ``i`` section: 

# In[3]:


DT[f.sleep_total > 18,  ["name", "sleep_total"]]


# To select a range of values, you can use two logical requirements; in the example below, only rows where `sleep_total` is greater than or equal to 16, and less than or equal to 18 are selected:

# In[4]:


DT[(f.sleep_total >= 16) & (f.sleep_total <= 18),  ["name", "sleep_total"]]


# Note in the code above, that each condition is wrapped in parentheses; this is to ensure that the correct output is obtained.
# 
# In [Pandas](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi-ybqouovvAhWRzjgGHcYtB1sQFjAAegQIAxAD&url=https%3A%2F%2Fpandas.pydata.org%2Fpandas-docs%2Fstable%2Freference%2Fapi%2Fpandas.Series.between.html&usg=AOvVaw2JuKj72awwkzd_18ykvwPx)/[dplyr](https://dplyr.tidyverse.org/reference/between.html)/[rdatatable](https://rdatatable.gitlab.io/data.table/reference/between.html), there is a `between` function that makes selection such as the above easier; at the moment, there is no equivalent function in [datatable](https://datatable.readthedocs.io/en/latest/api/index-api.html); you can create a temporary `between` function:

# In[5]:


def between(column, left, right):
    l = f[column]>=left
    r = f[column]<=right
    return l & r

DT[between('sleep_total', 16, 18),  ['name', 'sleep_total']]


# There are scenarios where you may want to select rows where the value is nearly a given value. You may also want to specify a tolerance value to indicate how far the values can be. 
# 
# This can be replicated with the [isclose](https://datatable.readthedocs.io/en/latest/api/math/isclose.html) function in the [datatable.math](https://datatable.readthedocs.io/en/latest/api/math.html) submodule.
# 
# Let's assume that the tolerance should be within one standard deviation of 17:

# In[6]:


# calculate tolerance
tolerance = DT['sleep_total'].sd1()

DT[dt.math.isclose(f.sleep_total, 17, atol = tolerance),  ['name', 'sleep_total']]


# ### Filtering based on String Matches

# You can select on string matches as well; in the example below, the ``==`` comparison operator is used to select a specific group of animals:

# In[7]:


DT[f.order == "Didelphimorphia",  ["order", "name", "sleep_total"]]


# Other operators can be used also:

# In[8]:


DT[f.order != 'Rodentia',  ['order', 'name', 'sleep_total']]


# In[9]:


DT[f.name > 'V', ['order', 'name', 'sleep_total']]


# In the examples above, only one animal is used; to select more animals, you could pass a list of conditions, with the `|` (or) symbol:

# In[10]:


rows = (f.order == "Didelphimorphia") | (f.order == "Diprotodontia")

columns = ['order', 'name', 'sleep_total']

DT[rows, columns]


# However, this can become unwieldy, as the number of animals increase. At the moment, there is no equivalent of python's [in](https://docs.python.org/3/reference/expressions.html#membership-test-operations) operator in [datatable](https://datatable.readthedocs.io/en/latest/api/index-api.html); let's create a temporary [function](https://stackoverflow.com/a/61509482/7175713) to help with this:

# In[11]:


def isin(column, sequence_of_labels):
    func = lambda x: f[column] == x
    return reduce(or_, map(func, sequence_of_labels))


labels =  ("Didelphimorphia", "Diprotodontia")

columns = ["order", "name", "sleep_total"]

DT[isin('order', labels), columns]


# You can also deselect certain groups using the `isin` function above, and combine it with the `~` symbol:

# In[12]:


labels = ("Rodentia", "Carnivora", "Primates")

columns = ['order', 'name', 'sleep_total']

DT[~isin('order', labels), columns]


# ### Filtering Rows Based on Regex

# There are scenarios where you need to filter string columns based on partial matches; a regular expression comes in handy here.
# 
# At the moment, there are very few string functions in [datatable](https://datatable.readthedocs.io/en/latest/api/index-api.html); However, we can make do with the `re_match` function, which is similar to Python's [re.match](https://docs.python.org/3/library/re.html#re.Pattern.match) to get by.
# 
# Let's filter for rows where `mouse` can be found in the column `name`:

# In[13]:


columns = ['name', 'sleep_total']

# returns a boolean column 
row = dt.re.match(f.name, '.*mouse.*')

DT[rows, columns]


# ### Filtering Rows based on Multiple Conditions

# Select rows with a `bodywt` above 100 and either have a `sleep_total` above 15, or are not part of the `Carnivora` `order`:

# In[14]:


rows = (f.bodywt > 100) & ((f.sleep_total > 15) | (f.order != "Carnivora"))

columns = ["name", "order", slice("sleep_total", "bodywt")]

DT[rows, columns]


# Return rows where `bodywt` is either greater than 100 or `brainwt` greater than 1, but not both:

# In[15]:


rows = xor((f.bodywt > 100), (f.brainwt > 1))

columns = ["name", slice("bodywt", "brainwt")]

DT[rows, columns]


# Select all rows where `brainwt` is larger than 1, but `bodywt` does not exceed 100:

# In[16]:


rows = ~(f.bodywt > 100) & (f.brainwt > 1)

columns = ["name", "sleep_total", "brainwt", "bodywt"]

DT[rows, columns]


# ### Filtering out Empty Rows

# There are two options for filtering out empty rows; comparing with `None`, or using the `isna` function:

# In[17]:


rows = f.conservation != None 

columns = ["name", slice("conservation", "sleep_cycle")]

DT[rows, columns]


# In[18]:


rows = ~dt.isna(f.conservation) 

columns = ["name", slice("conservation", "sleep_cycle")]

DT[rows, columns]


# ## Filtering across Multiple Columns

# ### Filter across all Columns

# It is possible to filter for rows based on values across columns.
# 
# One thing to note, and be careful about, is that in [datatable](https://datatable.readthedocs.io/en/latest/start/quick-start.html), within the same bracket, operations in the `i` section, occur before any operation within the `j` section; as such, depending on the context, and to ensure the right output, it is better to select the columns first, then chain the row filtration via another bracket. The examples below should make this clearer.
# 
# Let's filter for rows across the selected columns, keeping only rows where any column has the pattern `Ca` inside:

# In[19]:


columns = f['name':'order', 'sleep_total'].remove(f.vore)

rows = dt.rowany(f[str].re_match(".*Ca.*"))

DT[rows, columns]


# Let's look at another example, to filter for rows, across selected columns, where any column has a value less than 0.1:

# 

# In[20]:


columns = f['name', 'sleep_total':'bodywt']

rows = dt.rowany(f[int, float] < 0.1)

DT[rows, columns]


# The above example only requires that at least one column has a value less than 0.1. What if the goal is to return only rows where all the columns have values above 1? 

# In[21]:


columns = f['name', 'sleep_total' : 'bodywt'].remove(f.awake)

rows = dt.rowall(f[int, float] > 1)

DT[rows, columns]


# Note the change from [rowany](https://datatable.readthedocs.io/en/latest/api/dt/rowany.html) to [rowall](https://datatable.readthedocs.io/en/latest/api/dt/rowall.html); [rowany](https://datatable.readthedocs.io/en/latest/api/dt/rowany.html) will return `True` for rows where `ANY` column matches the condition, whereas [rowall](https://datatable.readthedocs.io/en/latest/api/dt/rowall.html) will only return `True` for rows where `ALL` columns match the condition.
# 
# 
# All the examples so far combine `i` and `j` within a single bracket; so why all the noise about context and selecting columns first before rows? The next section should shed more light.

# You can also limit the filtration to columns that match a particular type; the examples above show how that can be done. This can be handy in certain situations where the target is not limited to one data type.
# 
# Consider the example below, where only rows that have nulls should be returned. Nulls can be both in numeric and string columns:

# In[22]:


columns = f['name' : 'order', 'sleep_total' : 'sleep_rem']

rows = dt.rowany(f[:] == None)

DT[:, columns][rows, :]


# However, we are only interested in rows where the string columns are null; simply modifying the selected columns in `rows` should resolve this: 

# In[23]:


rows = dt.rowany(f[str] == None)

DT[rows, columns]


# That doesn't seem right. There are no missing values in rows 0 and 1, same for rows 26 and 30. What's going on?
# 
# As mentioned earlier, operations in `i` occur before `j`; in the code above, ALL the string columns in the frame were filtered, and not restricted to the selected columns. The right way about it is to select the columns first, then chain the row filtration:

# In[24]:


DT[:, columns][rows, :]


# Again, the filtration process depend on the context, and should be adapted accordingly.

# ### Filter at

# It is also possible to filter rows based on specific columns:

# In[25]:


columns = f['name', 'sleep_total' : 'sleep_rem', 'brainwt' : 'bodywt']

rows = dt.rowall(f['sleep_total', 'sleep_rem'] > 5)

DT[rows, columns]


# Note in the example above, the `rows` and `columns` are within the same bracket, because the columns are explicitly specified; only values from those columns will be used for the filtration.
# 
# Another example below that uses a different select option:

# In[26]:


columns = f['name', 'sleep_total' : 'sleep_rem', 'brainwt' : 'bodywt']

rows = [name for name in DT[:, columns].names if 'sleep' in name]

rows = dt.rowall(f[rows]>5)

DT[rows, columns]


# Resources: 
# 
# - [datatable docs](https://datatable.readthedocs.io/en/latest/)
# - Based on datatable version ``1.1.0a0+build.1627608562``
