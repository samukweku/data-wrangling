#!/usr/bin/env python
# coding: utf-8

# # Column Selection in Datatable

# *Updated July 30, 2021*

# This article highlights various ways to select columns in python [datatable](https://datatable.readthedocs.io/en/latest/). The examples used here are based off the excellent [article](https://suzan.rbind.io/2018/01/dplyr-tutorial-1/) by [Susan Baert](https://twitter.com/SuzanBaert).
# 
# The data file can be accessed [here](https://github.com/samukweku/data-wrangling-blog/raw/master/_notebooks/Data_files/msleep.txt)

# ## **Selecting Columns**

# ### The Basics

# In[1]:


from datatable import dt, f, Type
import re

file_path = "https://github.com/samukweku/data-wrangling-blog/raw/master/_notebooks/Data_files/msleep.txt"
DT = dt.fread(file_path)
DT.head(5)


# You can select columns by name or position in the `j` section:

# In[2]:


DT[:, 'genus'].head(5)


# In[3]:


DT[:, 1].head()


# In[4]:


DT[:, -10].head()


# If you are selecting a single column, you can pass it into the brackets without specifying the `i` section:

# In[5]:


DT['genus'].head(5)


# You can select columns by passing a list/tuple of the column names:

# In[6]:


columns_to_select = ["name", "genus", "sleep_total", "awake"]
DT[:, columns_to_select].head(5)


# You can pass a list/tuple of booleans; only the columns that pair with `True` are selected:

# In[7]:


columns_to_select = [True, True, False, False, False, True,False,True,True,False,False]
DT[:, columns_to_select].head(5)


# You can select chunks of columns using python's [slice](https://docs.python.org/3/library/functions.html#slice) syntax or via the ``start:end`` shortcut:

# In[8]:


DT[:, slice("name", "order")].head(5)


# In[9]:


DT[:, "name" : "order"].head(5)


# In[10]:


DT[:, :4].head(5)


# Multiple chunk selection is possible:

# In[11]:


columns_to_select = [slice("name", "order"), slice("sleep_total", "sleep_cycle")]
DT[:, columns_to_select].head(5)


# For the shortcut notation, for multiple selections, it has to be prefixed with datatable's [f](https://datatable.readthedocs.io/en/latest/manual/f-expressions.html) symbol:

# In[12]:


columns_to_select = f["name" : "order", "sleep_total" : "sleep_cycle"]

DT[:, columns_to_select].head(5)


# You can select columns in reverse:

# In[13]:


DT[:, "order": "name"].head(5)


# To deselect/drop columns you can use the [remove](https://datatable.readthedocs.io/en/latest/manual/f-expressions.html#modifying-a-columnset) function:

# In[14]:


columns_to_remove = f["sleep_total" : "awake", "conservation"]
DT[:, f[:].remove(columns_to_remove)].head(5)


# You can deselect a whole chunk, and then re-add a column again; this combines the [remove](https://datatable.readthedocs.io/en/latest/manual/f-expressions.html#modifying-a-columnset) and [extend](https://datatable.readthedocs.io/en/latest/manual/f-expressions.html#modifying-a-columnset) functions:

# In[15]:


DT[:, f[:].remove(f["name" : "awake"]).extend(f["conservation"])].head(5)


# ### Selecting Columns based on Partial Names

# You can use python's string functions to filter for columns with partial matching:

# In[16]:


columns_to_select = [name.startswith("sleep") for name in DT.names]
DT[:, columns_to_select].head(5)


# In[17]:


columns_to_select = ["eep" in name or name.endswith("wt") for name in DT.names]
DT[:, columns_to_select].head(5)


# ### Selecting Columns based on Regex

# Python's [re](https://docs.python.org/3/library/re.html) module can be used to select columns based on a regular expression:

# In[18]:


# this returns a list of booleans
columns_to_select = [True if re.search(r"o.+er", name) else False for name in DT.names]
DT[:, columns_to_select].head(5)


# ### Selecting columns by their data type

# You can pass a data type in the ``j`` section:

# In[19]:


DT[:, str].head(5)


# You can pass a list of data types:

# In[20]:


DT[:, [int, float]].head(5)


# You can also pass datatable's [Type](https://datatable.readthedocs.io/en/latest/api/type.html):

# In[21]:


DT[:, Type.str32].head(5)


# In[22]:


DT[:, Type.float64].head(5)


# You can remove columns based on their data type:

# In[23]:


columns_to_remove = f[int, float]
DT[:, f[:].remove(columns_to_remove)].head(5)


# An alternative is to preselect the columns you intend to keep, by using the Type [properties](https://datatable.readthedocs.io/en/latest/api/type.html#properties)::

# In[24]:


# creates a sequence of booleans
columns_to_select = [not dtype.is_numeric for dtype in DT.types]

DT[:, columns_to_select].head(5)


# You could also iterate through the frame and check each column's type, before recombining with [cbind](https://datatable.readthedocs.io/en/latest/api/dt/cbind.html):

# In[25]:


matching_frames = [frame for frame in DT 
                   if not frame.type.is_numeric]
                   
dt.cbind(matching_frames).head(5)


# Each column in a frame is treated as a frame, allowing for the list comprehension above.
# 
# You could also pass the `matching frames` to the `j` section of `DT`:

# In[26]:


DT[:, matching_frames].head(5)


# ### Selecting columns by logical expressions

# The ideas expressed in the previous section allows for more nifty column selection. 
# 
# Say we wish to select columns that are numeric, and have a mean greater than 10:

# In[27]:


# returns a list of booleans
columns_to_select = [dtype.is_numeric 
                     and DT[name].mean1() > 10
                     for name, dtype in zip(DT.names, DT.types)]
                     
DT[:, columns_to_select].head(5)


# The code above preselects the columns before passing it to datatable. `mean1` returns a scalar value; this allows us to compare with the scalar value `10`.
# 
# Alternatively, in the list comprehension, instead of a list of booleans, you could return the column names:
# 

# In[28]:


columns_to_select = [name
                     for name, dtype in zip(DT.names, DT.types)
                     if dtype.is_numeric
                     and DT[name].mean1() > 10]
                     
DT[:, columns_to_select].head(5)


# 
# You could also iterate through the frame in a list comprehension and check each column, before recombining with [cbind](https://datatable.readthedocs.io/en/latest/api/dt/cbind.html):

# In[29]:


matching_frames = [frame for frame in DT 
                   if frame.type.is_numeric 
                   and frame.mean1() > 10]
                   
dt.cbind(matching_frames).head(5)


# Instead of recombining with [cbind](https://datatable.readthedocs.io/en/latest/api/dt/cbind.html), you could pass the `matching_frames` to the ``j`` section:

# In[30]:


DT[:, matching_frames].head(5)


# Let's look at another example, where we select only columns where the number of distinct values is less than 10:

# In[31]:


# returns a list of booleans
columns_to_select = [frame.nunique1() < 10 for frame in DT]

DT[:, columns_to_select].head(5)


# In[32]:


matching_frames = [frame for frame in DT 
                   if frame.nunique1() < 10]
                   
dt.cbind(matching_frames).head(5)


# Or pass `matching_frames` to the `j` section in `DT`:

# In[33]:


DT[:, matching_frames].head(5)


# ## **Reordering Columns**

# You can select columns in the order that you want:

# In[34]:


columns_to_select = ['conservation', 'sleep_total', 'name']

DT[:, columns_to_select].head(5)


# To move some columns to the front, you could write a function to cover that:

# In[35]:


def move_to_the_front(frame, front_columns):
    column_names = list(frame.names)
    for name in front_columns:
        column_names.remove(name)
    front_columns.extend(column_names)
    return front_columns


# In[36]:


DT[:, move_to_the_front(DT, ['conservation', 'sleep_total'])].head(5)


# ## **Column Names**

# ### Renaming Columns

# Columns with new names can be created within the `j` section by passing a dictionary:

# In[37]:


new_names = {"animal": f.name, "extinction_threat": f.conservation}

DT[:, f.sleep_total.extend(new_names)].head(5)


# You can also rename the columns via a dictionary that maps the old column name to the new column name, and assign it to ``DT.names``:

# In[38]:


DT_copy = DT.copy()

DT_copy.names = {"name": "animal", "conservation": "extinction_threat"}

DT_copy[:, ['animal', 'sleep_total', 'extinction_threat']].head(5)


# In[39]:


DT_copy.head(5)


# ### Reformatting all Column Names

# You can use python's string functions to reformat column names.
# 
# Let's convert all column names to uppercase:

# In[40]:


DT_copy.names = [name.upper() for name in DT.names] # or list(map(str.upper, DT.names))

DT_copy.head(5)


# Resources: 
# 
# - [datatable docs](https://datatable.readthedocs.io/en/latest/)
# - Based on datatable version ``1.1.0a0+build.1627608562``
