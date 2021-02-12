# "Data Wrangling with Python Datatable - Selecting Columns"
> "Various Ways to select Columns"

- toc: true
- branch: master
- badges: true
- hide_binder_badge: True
- hide_colab_badge: True
- comments: true
- author: Samuel Oranyeli
- categories: [python, pydatatable]
- image: images/some_folder/your_image.png
- hide: false
- search_exclude: true
- metadata_key1: "python"
- metadata_key2: "datatable"

This article highlights various ways to select columns in python datatable. The examples used here are based off the excellent [article](https://suzan.rbind.io/2018/01/dplyr-tutorial-1/) by [Susan Baert](https://twitter.com/SuzanBaert).

The data file can be accessed [here](https://github.com/samukweku/data-wrangling-blog/raw/master/_notebooks/Data_files/msleep.txt)

## **Selecting Columns**

### The Basics

from datatable import dt, f, ltype, stype
import re

file_path = "https://github.com/samukweku/data-wrangling-blog/raw/master/_notebooks/Data_files/msleep.txt"
DT = dt.fread(file_path)
DT.head(5)

You can select columns by name or position in the `j` section:

DT[:, 'genus'].head(5)

DT[:, 1].head()

DT[:, -10].head()


If you are selecting a single column, you can pass it into the brackets without specifying the `i` section:

DT['genus'].head(5)

For the rest of this article, I will be focusing on column selection by name.

You can select columns by passing a list/tuple of the column names:

columns_to_select = ["name", "genus", "sleep_total", "awake"]
DT[:, columns_to_select].head(5)

You can pass a list/tuple of booleans:

columns_to_select = [True, True, False, False, False, True,False,True,True,False,False]
DT[:, columns_to_select].head(5)

You can select chunks of columns using python's [slice](https://docs.python.org/3/library/functions.html#slice) syntax or via the ``start:end`` shortcut:

DT[:, slice("name", "order")].head(5)

DT[:, "name" : "order"].head(5)


Multiple chunk selection is possible:

columns_to_select = [slice("name", "order"), slice("sleep_total", "sleep_cycle")]
DT[:, columns_to_select].head(5)

For the shortcut notation, for multiple selections, it has to be prefixed with datatable's [f](https://datatable.readthedocs.io/en/latest/manual/f-expressions.html) symbol:

columns_to_select = [f["name" : "order", "sleep_total" : "sleep_cycle"]]
DT[:, columns_to_select].head(5)

To deselect/drop columns you can use the [remove](https://datatable.readthedocs.io/en/latest/manual/f-expressions.html#modifying-a-columnset) function:

columns_to_remove = [f["sleep_total" : "awake", "conservation"]]
DT[:, f[:].remove(columns_to_remove)].head(5)

You can deselect a whole chunk, and then re-add a column again; this combines the [remove](https://datatable.readthedocs.io/en/latest/manual/f-expressions.html#modifying-a-columnset) and [extend](https://datatable.readthedocs.io/en/latest/manual/f-expressions.html#modifying-a-columnset) functions:

DT[:, f[:].remove(f["name" : "awake"]).extend(f["conservation"])].head(5)

### Selecting Columns based on Partial Names

You can use python's string functions to filter for columns with partial matching:

columns_to_select = [name.startswith("sleep") for name in DT.names]
DT[:, columns_to_select].head(5)

columns_to_select = ["eep" in name or name.endswith("wt") for name in DT.names]
DT[:, columns_to_select].head(5)

### Selecting Columns based on Regex

Python's [re](https://docs.python.org/3/library/re.html) module can be used to select columns based on a regular expression:

# this returns a list of booleans
columns_to_select = [True if re.search(r"o.+er", name) else False for name in DT.names]
DT[:, columns_to_select].head(5)

### Selecting columns by their data type

You can pass a data type in the ``j`` section:

DT[:, str].head(5)

You can pass a list of data types:

DT[:, [int, float]].head(5)

You can also pass datatable's [stype](https://datatable.readthedocs.io/en/latest/api/stype.html#) or [ltype](https://datatable.readthedocs.io/en/latest/api/ltype.html#) data types:

DT[:, ltype.str].head(5)

DT[:, stype.float64].head(5)

You can remove columns based on their data type:

columns_to_remove = [f[int, float]]
DT[:, f[:].remove(columns_to_remove)].head(5)

An alternative is to preselect the columns you intend to keep:

# creates a list of booleans
columns_to_select = [
    dtype not in (ltype.int, ltype.real)
    for name, dtype in zip(DT.names, DT.ltypes) 
]

DT[:, columns_to_select].head(5)

You could also iterate through the frame and check each column's type, before recombining with [cbind](https://datatable.readthedocs.io/en/latest/api/dt/cbind.html):

matching_frames = [frame for frame in DT if frame.ltypes[0] not in (ltype.real, ltype.int)]
dt.cbind(matching_frames).head(5)


Each column in a frame is treated as a frame, allowing for the list comprehension above.

You could also pass the `matching frames` to the `j` section of `DT`:

DT[:, matching_frames].head(5)

### Selecting columns by logical expressions

The ideas expressed in the previous section allows for more nifty column selection. 

Say we wish to select columns that are numeric, and have a mean greater than 10:

# returns a list of booleans
columns_to_select = [
    ltype in (ltype.real, ltype.int) and DT[name].mean()[0, 0] > 10
    for name, ltype in zip(DT.names, DT.ltypes)
]
DT[:, columns_to_select].head(5)

The code above preselects the columns before passing it to datatable. Note the use of `[0,0]` to return a scalar value; this allows us to compare with the scalar value `10`.

Alternatively, in the list comprehension, instead of a list of booleans, you could return the column names:


columns_to_select = [
    name
    for name, ltype in zip(DT.names, DT.ltypes)
    if ltype in (ltype.real, ltype.int) and DT[name].mean()[0, 0] > 10
]
DT[:, columns_to_select].head(5)


You could also iterate through the frame in a list comprehension and check each column, before recombining with [cbind](https://datatable.readthedocs.io/en/latest/api/dt/cbind.html):

matching_frames = [frame for frame in DT 
                    if frame.ltypes[0] in (ltype.int, ltype.real) 
                    and frame.mean()[0,0] > 10]
dt.cbind(matching_frames).head(5)

Instead of recombining with [cbind](https://datatable.readthedocs.io/en/latest/api/dt/cbind.html), you could pass the `matching_frames` to the ``j`` section:

DT[:, matching_frames].head(5)

Let's look at another example, where we select only columns where the number of distinct values is less than 10:

# returns a list of booleans
columns_to_select = [frame.nunique()[0, 0] < 10 for frame in DT]
DT[:, columns_to_select].head(5)

matching_frames = [frame for frame in DT if frame.nunique()[0,0] < 10]
dt.cbind(matching_frames).head(5)

Or pass `matching_frames` to the `j` section in `DT`:

DT[:, matching_frames].head(5)

## **Reordering Columns**

You can select columns in the order that you want:

columns_to_select = ['conservation', 'sleep_total', 'name']
DT[:, columns_to_select].head(5)

To move some columns to the front, you could write a function to cover that:

def move_to_the_front(frame, front_columns):
    column_names = list(frame.names)
    for name in front_columns:
        column_names.remove(name)
    front_columns.extend(column_names)
    return front_columns

DT[:, move_to_the_front(DT, ['conservation', 'sleep_total'])].head(5)

## **Column Names**

### Renaming Columns

Columns with new names can be created within the `j` section by passing a dictionary:

new_names = {"animal": f.name, "extinction_threat": f.conservation}
DT[:, f.sleep_total.extend(new_names)].head(5)

You can also rename the columns via a dictionary that maps the old column name to the new column name, and assign it to ``DT.names``:

DT_copy = DT.copy()
DT_copy.names = {"name": "animal", "conservation": "extinction_threat"}
DT_copy[:, ['animal', 'sleep_total', 'extinction_threat']].head(5)


DT_copy.head(5)

### Reformatting all Column Names

You can use python's string functions to reformat column names.

Let's convert all column names to uppercase:

DT_copy.names = [name.upper() for name in DT.names] # or list(map(str.upper, DT.names))
DT_copy.head(5)

Resources: 

- [datatable docs](https://datatable.readthedocs.io/en/latest/)
- I am using the latest dev version of datatable ``1.0.0a0+build.1612992576``