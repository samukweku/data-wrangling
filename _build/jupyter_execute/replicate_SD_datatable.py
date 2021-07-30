#!/usr/bin/env python
# coding: utf-8

# # Replicating .SD in Python Datatable

# ## **.SD - Subset of Data**

# I will be using [Jose Morales](https://twitter.com/jmrlsz) excellent [post](https://rpubs.com/josemz/SDbf) to show how .SD's functionality can be replicated in  python's [datatable](https://datatable.readthedocs.io/en/latest/index.html).
# 
#  Not all functions can be replicated; R [data.table](https://github.com/Rdatatable/data.table) has a whole lot more functions and features that are not yet implemented in [datatable](https://datatable.readthedocs.io/en/latest/index.html).
# 
# 
# The data file can be accessed [here](https://github.com/samukweku/data_files/raw/master/iris.csv)

# In[1]:


from datatable import dt, by, f, update, sort


# In[2]:


DT = dt.fread('https://github.com/samukweku/data_files/raw/master/iris.csv')
DT.head()


# ####  Number of unique observations per column

# In[3]:


# DT[, lapply(.SD, uniqueN)] --> Rdatatable

DT.nunique()


# #### Mean of all columns by `species`

# In[4]:


# DT[, lapply(.SD, mean), by = species] --> Rdatatable

DT[:, dt.mean(f[:]), by('species')]


# ### __Filtering__

# #### First two observations by species

# In[5]:


# DT[, .SD[1:2], by = species]

DT[:2, :, by('species')]


# In [datatable](https://datatable.readthedocs.io/en/latest/index.html), rows are selected in the `i` section after the grouping, unlike in R's [data.table](https://github.com/Rdatatable/data.table), where rows are selected in `i` before grouping, and rows selected in the `.SD` after grouping.

# #### Last two observations by `species`

# In[6]:


# DT[, tail(.SD, 2), by = species] 

DT[-2:, :, by('species')]


# Again, the rows are selected after grouping by using Python's negative index slicing.

# #### Select the top two sorted by `sepal length` in descending order

# In[7]:


# DT[order(-sepal_length), head(.SD, 2), by = species] 

DT[:2, :, by('species'), sort(-f.sepal_length)]


# In [datatable](https://datatable.readthedocs.io/en/latest/index.html), the [sort](https://datatable.readthedocs.io/en/latest/api/dt/sort.html#) function replicates the `order` function in R's [data.table](https://github.com/Rdatatable/data.table). Note the `-` symbol before the sepal_length *f-expression*; this instructs the dataframe to sort in descending order.

# #### Select the top two sorted by the difference between the `sepal length` and `sepal width`

# In[8]:


# DT[order(sepal_length - sepal_width), head(.SD, 2), by = species] 

DT[:2, :, by('species'), sort(f.sepal_length - f.sepal_width)]


# Just like in R's [data.table](https://github.com/Rdatatable/data.table), boolean expressions can be passed to the [sort](https://datatable.readthedocs.io/en/latest/api/dt/sort.html#) function.

# #### Filter observations above the mean of `sepal_length` by species

# In[9]:


# DT[, .SD[sepal_length > mean(sepal_length)], by = species] 

DT[:, update(temp = f.sepal_length > dt.mean(f.sepal_length)), by('species')]

DT[f.temp == 1, :-1]


# Unlike in R's [data.table](https://github.com/Rdatatable/data.table), boolean expressions can not be applied within the `i` section, in the presence of `by`. The next best thing is to break it down into two steps - create a temporary column to hold the boolean value, and then filter on that column.

# #### Filter rows with group size greater than 10 

# In[10]:


# DT[, .SD[.N > 10], keyby = .(species, petal_width)] 

DT[:, update(temp = dt.count() > 10), by('species', 'petal_width')]

DT[f.temp == 1, :-1]


# #### Get the row with the max petal_length by species.

# In[11]:


# DT[, .SD[which.max(petal_length)], by = species] OR 
# DT[, .SD[petal_length == max(petal_length)], by = species]  

# get rid of temp column
del DT['temp']

DT[0, :, by('species'), sort(-f.petal_length)]


# In the above code, we take advantage of the fact that sorting is done within each group; this allows us to pick the first row per group when `petal_length` is sorted in descending order.

# ### __.SDCols__

# #### Including columns in `.SD`

# In[12]:


# col_idx <- grep("^sepal", names(DT)) --> filter for the specicfic columns
# DT[, lapply(.SD, mean), .SDcols = col_idx]

# filter for the specific columns with a list comprehension
names = [name for name in DT.names
         if name.startswith('sepal')]

DT[:, dt.mean(f[names])]


# Alternatively, you can apply the mean as a method to the Frame:

# In[13]:


DT[:, names].mean()


# #### Removing columns from `.SD`

# In[14]:


# col_idx <- grep("^(petal|species)", names(DT))
# DT[, lapply(.SD, mean), .SDcols = -col_idx] --> exclusion occurs within .SDcols

# here, exclusion occurs within the list comprehension
names = [name for name in DT.names 
         if not name.startswith(('petal', 'species'))] 

DT[:, dt.mean(f[names])]


# Just like in the previous example, you can apply the `mean` as a method to the Frame:

# In[15]:


DT[:, names].mean()


# #### Column ranges

# In[16]:


# DT[, lapply(.SD, mean), .SDcols = sepal_length:sepal_width]

DT[:, dt.mean(f['sepal_length' : 'sepal_width'])]


# In[17]:


DT[:, 'sepal_length': 'sepal_width'].mean()


# ### __Summary__

# We've seen how to replicate `.SD` in [datatable](https://datatable.readthedocs.io/en/latest/index.html). There are other functionalities in `.SD` that are not presently possible in Python's [datatable](https://datatable.readthedocs.io/en/latest/index.html). It is possible that in the future, `.SD` will be implemented to allow for custom aggregation functions. That would be truly awesome, as it would allow [numpy](https://numpy.org/doc/stable/index.html) functions and functions from other Python libraries into [datatable](https://datatable.readthedocs.io/en/latest/index.html).
