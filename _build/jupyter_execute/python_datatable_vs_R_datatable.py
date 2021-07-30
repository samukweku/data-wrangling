#!/usr/bin/env python
# coding: utf-8

# # Python datatable vs R data.table comparison

# Python's [datatable](https://datatable.readthedocs.io/en/latest/) is closely related to R's [data.table](https://rdatatable.gitlab.io/data.table/), uses the same `DT[i, j, ...]` syntax, and attempts to mimic its core algorithms and API. There are a number of differences though, some due to language differences. There are also a lot more functions in R's [data.table](https://rdatatable.gitlab.io/data.table/) that do not have equivalents in [datatable](https://datatable.readthedocs.io/en/latest/) yet; hopefully, with time these functions will be added.
# 
# It also helps to keep in mind that in [Python](https://docs.python.org/3/), indexing starts at 0, while in [R](https://www.r-project.org/other-docs.html), indexing starts at 1.
# 
# I am using [atrebas'](https://twitter.com/atrebas/status/1287435078247813121) excellent [guide](https://atrebas.github.io/post/2020-06-14-datatable-pandas/) for this; as more functions are added to [datatable](https://datatable.readthedocs.io/en/latest/), this comparison will be updated.
# 
# No changes were made to the R code; I just copied as-is from atrebas' [guide](https://atrebas.github.io/post/2020-06-14-datatable-pandas/); the python code is the main addition, showing equivalents (where possible) to the R code.
# 
# Also, the same example data used in the [guide](https://atrebas.github.io/post/2020-06-14-datatable-pandas/) is used here.
# 
# [data.table](https://rdatatable.gitlab.io/data.table/) uses `DT` as the name of the frame, while [datatable](https://datatable.readthedocs.io/en/latest/) uses `DF`.

# ```{note}
# The datatable [docs](https://datatable.readthedocs.io/en/latest/index.html) has a [data.table vs datatable](https://datatable.readthedocs.io/en/latest/manual/comparison_with_rdatatable.html) comparison page.
# ```

# ```{tip}
# Click on the arrow at the top (pointing to the left), to hide the table of contents on the left; that way the code will fill up the width of the screen and should be easier to view.
# ```

# ### Example Data

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# **data.table**
# ^^^
# 
# ```R
#     library(data.table)
#     set.seed(1L)
# 
#     ## Create a data table
#     DT <- data.table(V1 = rep(c(1L, 2L), 5)[-10],
#                     V2 = 1:9,
#                     V3 = c(0.5, 1.0, 1.5),
#                     V4 = rep(LETTERS[1:3], 3))
# 
#     > class(DT)
#     [1] "data.table" "data.frame"
#     
#     > DT
#        V1 V2  V3 V4
#     1:  1  1 0.5  A
#     2:  2  2 1.0  B
#     3:  1  3 1.5  C
#     4:  2  4 0.5  A
#     5:  1  5 1.0  B
#     6:  2  6 1.5  C
#     7:  1  7 0.5  A
#     8:  2  8 1.0  B
#     9:  1  9 1.5  C
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
#     from datatable import dt, f, by, update, ltype
#     import numpy as np
#     import re
# 
# 
#     DF = dt.Frame(
#     {"V1" : [1, 2, 1, 2, 1, 2, 1, 2, 1],
#     "V2" : [1, 2, 3, 4, 5, 6, 7, 8, 9], 
#     "V3" : [0.5, 1.0, 1.5] * 3, 
#     "V4" : ['A', 'B', 'C'] * 3}) 
# 
#     type(DF)
#     datatable.Frame
# 
#     DF     
#        |    V1     V2       V3  V4   
#        | int32  int32  float64  str32
#     -- + -----  -----  -------  -----
#      0 |     1      1      0.5  A    
#      1 |     2      2      1    B    
#      2 |     1      3      1.5  C    
#      3 |     2      4      0.5  A    
#      4 |     1      5      1    B    
#      5 |     2      6      1.5  C    
#      6 |     1      7      0.5  A    
#      7 |     2      8      1    B    
#      8 |     1      9      1.5  C    
#     [9 rows x 4 columns]
# ```
# 
# 
# ````

# ## **Basic Operations**

# ### Filter Rows

# <p align="center">  Filter Rows by Position </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
#     > DT[3:4, ]
#     
#        V1 V2  V3 V4
#     1:  1  3 1.5  C
#     2:  2  4 0.5  A
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
#     DF[1:3, :]
# 
#        |    V1     V2       V3  V4   
#        | int32  int32  float64  str32
#     -- + -----  -----  -------  -----
#      0 |     2      2      1    B    
#      1 |     1      3      1.5  C    
#     [2 rows x 4 columns]
# ```
# 
# 
# ````

# <p align="center">  Remove Rows by Position </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
#     > DT[!3:7, ]
# 
#     > DT[-(3:7)] # same
#     
#        V1 V2  V3 V4
#     1:  1  1 0.5  A
#     2:  2  2 1.0  B
#     3:  2  8 1.0  B
#     4:  1  9 1.5  C
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
#     DF[[slice(None, 2), slice(7, None)], :]
# 
#     DF[[num for num in range(DF.nrows) 
#         if num not in range(2, 7)], :] # same
# 
#     DF[np.setdiff1d(range(DF.nrows), 
#                     range(2, 7)), :] # same
#                     
#      |    V1     V2       V3  V4   
#      | int32  int32  float64  str32
#   -- + -----  -----  -------  -----
#    0 |     1      1      0.5  A    
#    1 |     2      2      1    B    
#    2 |     2      8      1    B    
#    3 |     1      9      1.5  C    
#   [4 rows x 4 columns]
#                 
#  
#      
# ```
# 
# 
# ````

# <p align="center">  Filter Rows using a Logical Expression </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
#  > DT[V2 > 5]
# 
#        V1 V2  V3 V4
#     1:  2  6 1.5  C
#     2:  1  7 0.5  A
#     3:  2  8 1.0  B
#     4:  1  9 1.5  C
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
#     DF[f.V2 > 5, :]
# 
#        |    V1     V2       V3  V4   
#        | int32  int32  float64  str32
#     -- + -----  -----  -------  -----
#      0 |     2      6      1.5  C    
#      1 |     1      7      0.5  A    
#      2 |     2      8      1    B    
#      3 |     1      9      1.5  C    
#     [4 rows x 4 columns]
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > DT[V4 %chin% c("A", "C")] # fast %in% for character
# 
#        V1 V2  V3 V4
#     1:  1  1 0.5  A
#     2:  1  3 1.5  C
#     3:  2  4 0.5  A
#     4:  2  6 1.5  C
#     5:  1  7 0.5  A
#     6:  1  9 1.5  C
# 
# 
# ```
# ---
# 
# ```python
# 
#     # no equivalent `in` in datatable
#     # temporary workaround
#     
#     from functools import reduce
#     from operator import or_
# 
#     def isin(column, iterable):
#         content = [f[column] == entry 
#                    for entry in iterable]
#         return reduce(or_, content)
# 
#     DF[isin('V4', ('A', 'C')), :]
# 
#        |    V1     V2       V3  V4   
#        | int32  int32  float64  str32
#     -- + -----  -----  -------  -----
#      0 |     1      1      0.5  A    
#      1 |     1      3      1.5  C    
#      2 |     2      4      0.5  A    
#      3 |     2      6      1.5  C    
#      4 |     1      7      0.5  A    
#      5 |     1      9      1.5  C    
#     [6 rows x 4 columns]
# 
# ```
# 
# ````

# <p align="center">  Filter Rows using Multiple Conditions </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[V1 == 1 & V4 == "A"]
# 
#    V1 V2  V3 V4
# 1:  1  1 0.5  A
# 2:  1  7 0.5  A
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
#     DF[(f.V1==1) & (f.V4=="A"), :]
# 
#       |    V1     V2       V3  V4   
#       | int32  int32  float64  str32
#    -- + -----  -----  -------  -----
#     0 |     1      1      0.5  A    
#     1 |     1      7      0.5  A    
#    [2 rows x 4 columns]
# 
# 
# ```
# 
# ````

# <p align="center">  Filter Unique Rows </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > unique(DT)
# 
#    V1 V2  V3 V4
# 1:  1  1 0.5  A
# 2:  2  2 1.0  B
# 3:  1  3 1.5  C
# 4:  2  4 0.5  A
# 5:  1  5 1.0  B
# 6:  2  6 1.5  C
# 7:  1  7 0.5  A
# 8:  2  8 1.0  B
# 9:  1  9 1.5  C
# 
# > unique(DT, by = c("V1", "V4")) # returns all cols
# 
#    V1 V2  V3 V4
# 1:  1  1 0.5  A
# 2:  2  2 1.0  B
# 3:  1  3 1.5  C
# 4:  2  4 0.5  A
# 5:  1  5 1.0  B
# 6:  2  6 1.5  C
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# # no equivalent yet
# # dt.unique() returns unique values
# # in the entire frame, 
# # not unique rows
# # a groupby could work,
# # but my attempts so far
# # do not look clean/efficient/simple enough
# # to warrant posting a workaround
# 
# ```
# 
# ````

# <p align="center">  Discard Rows with Missing Values </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# # fast S3 method with cols argument
# > na.omit(DT, cols = 1:4)  
# 
#    V1 V2  V3 V4
# 1:  1  1 0.5  A
# 2:  2  2 1.0  B
# 3:  1  3 1.5  C
# 4:  2  4 0.5  A
# 5:  1  5 1.0  B
# 6:  2  6 1.5  C
# 7:  1  7 0.5  A
# 8:  2  8 1.0  B
# 9:  1  9 1.5  C
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[~dt.rowany(f[:] == None), :]
# 
# DF[~dt.rowany(dt.isna(f[:])), :] # same
# 
#    |    V1     V2       V3  V4   
#    | int32  int32  float64  str32
# -- + -----  -----  -------  -----
#  0 |     1      1      0.5  A    
#  1 |     2      2      1    B    
#  2 |     1      3      1.5  C    
#  3 |     2      4      0.5  A    
#  4 |     1      5      1    B    
#  5 |     2      6      1.5  C    
#  6 |     1      7      0.5  A    
#  7 |     2      8      1    B    
#  8 |     1      9      1.5  C    
# [9 rows x 4 columns]
# 
# 
# ```
# 
# ````

# <p align="center">  Other Filters </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[sample(.N, 3)] # .N = nb of rows in DT
# 
#    V1 V2  V3 V4
# 1:  1  9 1.5  C
# 2:  2  4 0.5  A
# 3:  1  7 0.5  A
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[np.random.choice(DF.nrows, 3), :]
# 
#    |    V1     V2       V3  V4   
#    | int32  int32  float64  str32
# -- + -----  -----  -------  -----
#  0 |     1      9      1.5  C    
#  1 |     1      1      0.5  A    
#  2 |     1      9      1.5  C    
# [3 rows x 4 columns]
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > DT[sample(.N, .N / 2)]
# 
#    V1 V2  V3 V4
# 1:  1  1 0.5  A
# 2:  2  2 1.0  B
# 3:  1  5 1.0  B
# 4:  1  3 1.5  C
# 
# ```
# ---
# 
# 
# 
# ```python
#    
# DF[np.random.choice(DF.nrows, DF.nrows//2), :]
# 
#    |    V1     V2       V3  V4   
#    | int32  int32  float64  str32
# -- + -----  -----  -------  -----
#  0 |     1      9      1.5  C    
#  1 |     2      8      1    B    
#  2 |     1      1      0.5  A    
#  3 |     1      3      1.5  C    
# [4 rows x 4 columns]
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > DT[frankv(-V1, ties.method = "dense") < 2]
# 
#    V1 V2  V3 V4
# 1:  2  2 1.0  B
# 2:  2  4 0.5  A
# 3:  2  6 1.5  C
# 4:  2  8 1.0  B
# 
# 
# 
# ```
# ---
# 
# ```python
# 
# # no rank function in datatable
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > DT[V4 %like% "^B"]
# 
#    V1 V2 V3 V4
# 1:  2  2  1  B
# 2:  1  5  1  B
# 3:  2  8  1  B
# 
# ```
# ---
# 
# ```python
#    
# # very sparse string functions in datatable
# # `re_match` and `len` are the only functions 
# # currently available
# 
# DF[f.V4.re_match("^B"), :]
# 
#    |    V1     V2       V3  V4   
#    | int32  int32  float64  str32
# -- + -----  -----  -------  -----
#  0 |     2      2        1  B    
#  1 |     1      5        1  B    
#  2 |     2      8        1  B    
# [3 rows x 4 columns]
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# 
# > DT[V2 %between% c(3, 5)]
# 
#    V1 V2  V3 V4
# 1:  1  3 1.5  C
# 2:  2  4 0.5  A
# 3:  1  5 1.0  B
# 
# 
# ```
# ---
# 
# 
# ```python
#    
# # no `between` equivalent 
# # temporary workaround
# 
# def between(column, left, right, bounds = True):
#     if bounds:
#          l = f[column]>=left
#          r = f[column]<=right
#     else:
#         l = f[column]>left
#         r = f[column]<right
#     return l & r
# 
# 
# DF[between('V2', 3, 5), :]
# 
#    |    V1     V2       V3  V4   
#    | int32  int32  float64  str32
# -- + -----  -----  -------  -----
#  0 |     1      3      1.5  C    
#  1 |     2      4      0.5  A    
#  2 |     1      5      1    B    
# [3 rows x 4 columns]
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > DT[data.table::between(V2, 3, 5, incbounds = FALSE)]
# 
#    V1 V2  V3 V4
# 1:  2  4 0.5  A
# 
# 
# ```
# ---
# 
# 
# ```python   
# 
# DF[between('V2', 3, 5, False), :]
# 
#    |    V1     V2       V3  V4   
#    | int32  int32  float64  str32
# -- + -----  -----  -------  -----
#  0 |     2      4      0.5  A    
# [1 row x 4 columns]
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > DT[V2 %inrange% list(-1:1, 1:3)] # see also ?inrange
# 
#    V1 V2  V3 V4
# 1:  1  1 0.5  A
# 2:  2  2 1.0  B
# 3:  1  3 1.5  C
# 
# 
# 
# ```
# ---
# 
# 
# ```python
#    
# # no equivalent for `inrange`
# # plus I dont think I fully grok the function
# ```
# 
# ````

# ### Sort Rows

# <p align="center">  Sort Rows by Column </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[order(V3)]  # see also setorder
# 
#    V1 V2  V3 V4
# 1:  1  1 0.5  A
# 2:  2  4 0.5  A
# 3:  1  7 0.5  A
# 4:  2  2 1.0  B
# 5:  1  5 1.0  B
# 6:  2  8 1.0  B
# 7:  1  3 1.5  C
# 8:  2  6 1.5  C
# 9:  1  9 1.5  C
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, :, dt.sort('V3')]
# 
# DF.sort('V3') # same
# 
#    |    V1     V2       V3  V4   
#    | int32  int32  float64  str32
# -- + -----  -----  -------  -----
#  0 |     1      1      0.5  A    
#  1 |     2      4      0.5  A    
#  2 |     1      7      0.5  A    
#  3 |     2      2      1    B    
#  4 |     1      5      1    B    
#  5 |     2      8      1    B    
#  6 |     1      3      1.5  C    
#  7 |     2      6      1.5  C    
#  8 |     1      9      1.5  C   
# [9 rows x 4 columns]
# 
# ```
# 
# ````

# <p align="center">  Sort Rows in decreasing Order </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[order(-V3)]
# 
#    V1 V2  V3 V4
# 1:  1  3 1.5  C
# 2:  2  6 1.5  C
# 3:  1  9 1.5  C
# 4:  2  2 1.0  B
# 5:  1  5 1.0  B
# 6:  2  8 1.0  B
# 7:  1  1 0.5  A
# 8:  2  4 0.5  A
# 9:  1  7 0.5  A
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, :, dt.sort(-f.V3)]
# 
# DF.sort(-f.V3) # same
# 
#    |    V1     V2       V3  V4   
#    | int32  int32  float64  str32
# -- + -----  -----  -------  -----
#  0 |     1      3      1.5  C    
#  1 |     2      6      1.5  C    
#  2 |     1      9      1.5  C    
#  3 |     2      2      1    B    
#  4 |     1      5      1    B    
#  5 |     2      8      1    B    
#  6 |     1      1      0.5  A    
#  7 |     2      4      0.5  A    
#  8 |     1      7      0.5  A    
# [9 rows x 4 columns]
# 
# 
# ```
# 
# ````

# <p align="center">  Sort Rows based on Several Columns </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[order(V1, -V2)]
# 
#    V1 V2  V3 V4
# 1:  1  9 1.5  C
# 2:  1  7 0.5  A
# 3:  1  5 1.0  B
# 4:  1  3 1.5  C
# 5:  1  1 0.5  A
# 6:  2  8 1.0  B
# 7:  2  6 1.5  C
# 8:  2  4 0.5  A
# 9:  2  2 1.0  B
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, : , dt.sort(f.V1, -f.V2)]
# 
# DF.sort(f.V1, -f.V2) # same
# 
#    |    V1     V2       V3  V4   
#    | int32  int32  float64  str32
# -- + -----  -----  -------  -----
#  0 |     1      9      1.5  C    
#  1 |     1      7      0.5  A    
#  2 |     1      5      1    B    
#  3 |     1      3      1.5  C    
#  4 |     1      1      0.5  A    
#  5 |     2      8      1    B    
#  6 |     2      6      1.5  C    
#  7 |     2      4      0.5  A    
#  8 |     2      2      1    B    
# [9 rows x 4 columns]
# 
# 
# ```
# 
# ````

# ```{note}
# datatable's [sort](https://datatable.readthedocs.io/en/latest/api/dt/sort.html) function has a `reverse` parameter, which can be used in place of the negation, for sorting in ascending/descending order. As at the time of writing this, it is a bit [buggy](https://github.com/h2oai/datatable/issues/2838), especially when sorting on multiple columns.
# ```

# ### Select Columns

# <p align="center"> Select One Column using an Index </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[[3]] # returns a vector
# 
# [1] 0.5 1.0 1.5 0.5 1.0 1.5 0.5 1.0 1.5
# 
# > DT[, 3]  # returns a data.table
# 
#     V3
# 1: 0.5
# 2: 1.0
# 3: 1.5
# 4: 0.5
# 5: 1.0
# 6: 1.5
# 7: 0.5
# 8: 1.0
# 9: 1.5
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, 2] # returns a frame
# 
# DF[:, [2]] # same
# 
# DF[2] # selecting a single column this way is allowed
# 
#    |      V3
#    | float64
# -- + -------
#  0 |     0.5
#  1 |     1  
#  2 |     1.5
#  3 |     0.5
#  4 |     1  
#  5 |     1.5
#  6 |     0.5
#  7 |     1  
#  8 |     1.5
# [9 rows x 1 column]
# 
# 
# ```
# 
# ````

# <p align="center">  Select One Column using Column Name </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, list(V2)] # returns a data.table
# 
# # . is an alias for list
# > DT[, .(V2)]    # returns a data.table
# 
# > DT[, "V2"]     # returns a data.table
# 
#    V2
# 1:  1
# 2:  2
# 3:  3
# 4:  4
# 5:  5
# 6:  6
# 7:  7
# 8:  8
# 9:  9
# 
# > DT[, V2]       # returns a vector
# 
# [1] 1 2 3 4 5 6 7 8 9
# 
# > DT[["V2"]]     # returns a vector
# 
# [1] 1 2 3 4 5 6 7 8 9
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, 'V2'] # always returns a frame
# 
# DF[:, f.V2] # same
# 
# DF[:, ['V2']] # same
# 
# DF['V2'] # a single column can be selected this way
# 
#    |    V2
#    | int32
# -- + -----
#  0 |     1
#  1 |     2
#  2 |     3
#  3 |     4
#  4 |     5
#  5 |     6
#  6 |     7
#  7 |     8
#  8 |     9
# [9 rows x 1 column]
# 
# ```
# 
# ````

# <p align="center">  Select Several Columns </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, .(V2, V3, V4)]
# 
# > DT[, list(V2, V3, V4)] # same
# 
# > DT[, V2:V4] # select columns between V2 and V4
# 
#    V2  V3 V4
# 1:  1 0.5  A
# 2:  2 1.0  B
# 3:  3 1.5  C
# 4:  4 0.5  A
# 5:  5 1.0  B
# 6:  6 1.5  C
# 7:  7 0.5  A
# 8:  8 1.0  B
# 9:  9 1.5  C
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, ['V2', 'V3', 'V4']]
# 
# DF[:, slice('V2', 'V4')] # same
# 
# DF[:, 'V2':'V4'] # shortcut for slice
# 
#    |    V2       V3  V4   
#    | int32  float64  str32
# -- + -----  -------  -----
#  0 |     1      0.5  A    
#  1 |     2      1    B    
#  2 |     3      1.5  C    
#  3 |     4      0.5  A    
#  4 |     5      1    B    
#  5 |     6      1.5  C    
#  6 |     7      0.5  A    
#  7 |     8      1    B    
#  8 |     9      1.5  C    
# [9 rows x 3 columns]
# 
# ```
# 
# ````

# <p align="center">  Exclude Columns </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, !c("V2", "V3")]
# 
#    V1 V4
# 1:  1  A
# 2:  2  B
# 3:  1  C
# 4:  2  A
# 5:  1  B
# 6:  2  C
# 7:  1  A
# 8:  2  B
# 9:  1  C
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, f[:].remove(f['V2', 'V3'])]
# 
# # more verbose
# DF[:, [name for name in DF.names 
#        if name not in ('V2', 'V3')]]
# 
# # same list comprehension idea
# # returns a list of booleans 
# # to select the columns
# DF[:, [name not in ('V2', 'V3') 
#        for name in DF.names]]
# 
#    |    V1  V4   
#    | int32  str32
# -- + -----  -----
#  0 |     1  A    
#  1 |     2  B    
#  2 |     1  C    
#  3 |     2  A    
#  4 |     1  B    
#  5 |     2  C    
#  6 |     1  A    
#  7 |     2  B    
#  8 |     1  C    
# [9 rows x 2 columns]
# 
# ```
# 
# ````

# <p align="center">  Select/Exclude columns via a Variable</p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > cols <- c("V2", "V3")
# 
# > DT[, ..cols] # .. prefix means 'one-level up'
# 
#    V2  V3
# 1:  1 0.5
# 2:  2 1.0
# 3:  3 1.5
# 4:  4 0.5
# 5:  5 1.0
# 6:  6 1.5
# 7:  7 0.5
# 8:  8 1.0
# 9:  9 1.5
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# cols = ('V2', 'V3')
# 
# DF[:, cols]
# 
#    |    V2       V3
#    | int32  float64
# -- + -----  -------
#  0 |     1      0.5
#  1 |     2      1  
#  2 |     3      1.5
#  3 |     4      0.5
#  4 |     5      1  
#  5 |     6      1.5
#  6 |     7      0.5
#  7 |     8      1  
#  8 |     9      1.5
# [9 rows x 2 columns]
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > cols <- c("V2", "V3")
# 
# > DT[, !..cols] # or DT[, -..cols]
# 
#    V1 V4
# 1:  1  A
# 2:  2  B
# 3:  1  C
# 4:  2  A
# 5:  1  B
# 6:  2  C
# 7:  1  A
# 8:  2  B
# 9:  1  C
# 
# 
# ```
# ---
# 
# 
# ```python
#    
# DF[:, f[:].remove(f[cols])]
# 
# # list comprehension
# DF[:, [name not in cols 
#        for name in DF.names]]
# 
#    |    V1  V4   
#    | int32  str32
# -- + -----  -----
#  0 |     1  A    
#  1 |     2  B    
#  2 |     1  C    
#  3 |     2  A    
#  4 |     1  B    
#  5 |     2  C    
#  6 |     1  A    
#  7 |     2  B    
#  8 |     1  C    
# [9 rows x 2 columns]
# 
# 
# ```
# 
# ````

# <p align="center">  Other Selections </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > cols <- paste0("V", 1:2)
# 
# > DT[, ..cols]
# 
#    V1 V2
# 1:  1  1
# 2:  2  2
# 3:  1  3
# 4:  2  4
# 5:  1  5
# 6:  2  6
# 7:  1  7
# 8:  2  8
# 9:  1  9
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # f-strings
# cols = [f"V{num}" for num in (1, 2)]
# 
# cols
# ['V1', 'V2']
# 
# DF[:, cols]
# 
#    |    V1     V2
#    | int32  int32
# -- + -----  -----
#  0 |     1      1
#  1 |     2      2
#  2 |     1      3
#  3 |     2      4
#  4 |     1      5
#  5 |     2      6
#  6 |     1      7
#  7 |     2      8
#  8 |     1      9
# [9 rows x 2 columns]
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > cols <- union("V4", names(DT))
# 
# > DT[, ..cols]
# 
#    V4 V1 V2  V3
# 1:  A  1  1 0.5
# 2:  B  2  2 1.0
# 3:  C  1  3 1.5
# 4:  A  2  4 0.5
# 5:  B  1  5 1.0
# 6:  C  2  6 1.5
# 7:  A  1  7 0.5
# 8:  B  2  8 1.0
# 9:  C  1  9 1.5
# 
# 
# 
# ```
# ---
# 
# 
# ```python
#    
# cols = set(["V4"]).union(DF.names)
# 
# 
# cols
# {'V3', 'V2', 'V4', 'V1'}
# 
# # sets not accepted in the `j` section
# DF[:, tuple(cols)]
# 
#    |      V3     V2  V4        V1
#    | float64  int32  str32  int32
# -- + -------  -----  -----  -----
#  0 |     0.5      1  A          1
#  1 |     1        2  B          2
#  2 |     1.5      3  C          1
#  3 |     0.5      4  A          2
#  4 |     1        5  B          1
#  5 |     1.5      6  C          2
#  6 |     0.5      7  A          1
#  7 |     1        8  B          2
#  8 |     1.5      9  C          1
# [9 rows x 4 columns]
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > cols <- grep("V",   names(DT))
# 
# > DT[, ..cols]
# 
#    V1 V2  V3 V4
# 1:  1  1 0.5  A
# 2:  2  2 1.0  B
# 3:  1  3 1.5  C
# 4:  2  4 0.5  A
# 5:  1  5 1.0  B
# 6:  2  6 1.5  C
# 7:  1  7 0.5  A
# 8:  2  8 1.0  B
# 9:  1  9 1.5  C
# 
# ```
# ---
# 
# 
# 
# ```python
# 
# # returns a list of booleans
# cols = ["V" in name for name in DF.names]
# 
# cols
# [True, True, True, True]
# 
# DF[:, cols]
# 
#    |    V1     V2       V3  V4   
#    | int32  int32  float64  str32
# -- + -----  -----  -------  -----
#  0 |     1      1      0.5  A    
#  1 |     2      2      1    B    
#  2 |     1      3      1.5  C    
#  3 |     2      4      0.5  A    
#  4 |     1      5      1    B    
#  5 |     2      6      1.5  C    
#  6 |     1      7      0.5  A    
#  7 |     2      8      1    B    
#  8 |     1      9      1.5  C    
# [9 rows x 4 columns]
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > cols <- grep("3$",  names(DT))
# 
# > DT[, ..cols]
# 
#     V3
# 1: 0.5
# 2: 1.0
# 3: 1.5
# 4: 0.5
# 5: 1.0
# 6: 1.5
# 7: 0.5
# 8: 1.0
# 9: 1.5
# 
# 
# ```
# 
# ---
# 
# 
# 
# ```python
#    
# cols = [name.endswith("3") for name in DF.names]
# 
# cols
# [False, False, True, False]
# 
# 
# DF[:, cols]
# 
#    |      V3
#    | float64
# -- + -------
#  0 |     0.5
#  1 |     1  
#  2 |     1.5
#  3 |     0.5
#  4 |     1  
#  5 |     1.5
#  6 |     0.5
#  7 |     1  
#  8 |     1.5
# [9 rows x 1 column]
# 
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > cols <- grep(".2",  names(DT))
# 
# > DT[, ..cols]
# 
#    V2
# 1:  1
# 2:  2
# 3:  3
# 4:  4
# 5:  5
# 6:  6
# 7:  7
# 8:  8
# 9:  9
# 
# 
# 
# ```
# ---
# 
# 
# ```python
#    
# cols = [name for name in DF.names 
#         if re.search(".2", name)]
# 
# cols
# ['V2']
# 
# DF[:, cols]
# 
#    |    V2
#    | int32
# -- + -----
#  0 |     1
#  1 |     2
#  2 |     3
#  3 |     4
#  4 |     5
#  5 |     6
#  6 |     7
#  7 |     8
#  8 |     9
# [9 rows x 1 column]
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > cols <- grep("^V1|X$",  names(DT))
# 
# > DT[, ..cols]
# 
#    V1
# 1:  1
# 2:  2
# 3:  1
# 4:  2
# 5:  1
# 6:  2
# 7:  1
# 8:  2
# 9:  1
# 
# 
# ```
# ---
# 
# 
# ```python
#    
# cols = [name for name in DF.names 
#         if re.search("^V1|X", name)]
# 
# cols
# ['V1']
# 
# 
# DF[:, cols]
# 
#    |    V1
#    | int32
# -- + -----
#  0 |     1
#  1 |     2
#  2 |     1
#  3 |     2
#  4 |     1
#  5 |     2
#  6 |     1
#  7 |     2
#  8 |     1
# [9 rows x 1 column]
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > cols <- grep("^(?!V2)", names(DT), perl = TRUE)
# 
# > DT[, ..cols]
# 
#    V1  V3 V4
# 1:  1 0.5  A
# 2:  2 1.0  B
# 3:  1 1.5  C
# 4:  2 0.5  A
# 5:  1 1.0  B
# 6:  2 1.5  C
# 7:  1 0.5  A
# 8:  2 1.0  B
# 9:  1 1.5  C
# 
# 
# 
# ```
# ---
# 
# 
# ```python
#    
# cols = [name for name in DF.names 
#         if re.search("^(?!V2)", name)]
# 
# cols
# ['V1', 'V3', 'V4']
# 
# 
# DF[:, cols]
# 
#    |    V1       V3  V4   
#    | int32  float64  str32
# -- + -----  -------  -----
#  0 |     1      0.5  A    
#  1 |     2      1    B    
#  2 |     1      1.5  C    
#  3 |     2      0.5  A    
#  4 |     1      1    B    
#  5 |     2      1.5  C    
#  6 |     1      0.5  A    
#  7 |     2      1    B    
#  8 |     1      1.5  C    
# [9 rows x 3 columns]
# 
# 
# ```
# 
# ````

# ### Summarise Data

# <p align="center"> Summarise One Column </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, sum(V1)]    # returns a vector
# [1] 13
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF['V1'].sum1() # returns a scalar
# 13.0
# 
# #similar to above
# DF[:, dt.sum(f.V1)][0, 0]
# 13
# 
# DF['V1'].sum()[0, 0] # same
# 13.0
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > DT[, .(sum(V1))] # returns a data.table
# 
#    V1
# 1: 13
# 
# ```
# ---
# 
# 
# ```python
#    
# DF['V1'].sum()
# 
#    |      V1
#    | float64
# -- + -------
#  0 |      13
# [1 row x 1 column]
# 
# 
# DF[:, dt.sum(f.V1)]
# 
#    |    V1
#    | int64
# -- + -----
#  0 |    13
# [1 row x 1 column]
# 
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > DT[, .(sumV1 = sum(V1))] # returns a data.table
# 
#    sumV1
# 1:    13
# 
# ```
# ---
# 
# 
# ```python
#    
# DF[:, {"sumV1" : dt.sum(f.V1)}]
# 
#    | sumV1
#    | int64
# -- + -----
#  0 |    13
# [1 row x 1 column]
# 
# 
# DF[:, {"sumV1" : f.V1}].sum()
# 
#    |   sumV1
#    | float64
# -- + -------
#  0 |      13
# [1 row x 1 column]
# 
# 
# ```
# 
# ````

# <p align="center"> Summarise Several Columns </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, .(sum(V1), sd(V3))]
# 
#    V1        V2
# 1: 13 0.4330127
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, [dt.sum(f.V1), dt.sd(f.V3)]]
# 
#    |    V1        V3
#    | int64   float64
# -- + -----  --------
#  0 |    13  0.433013
# [1 row x 2 columns]
# 
# 
# 
# ```
# 
# ````

# <p align="center"> Summarise Several Columns and Assign Column Names </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, .(sumv1 = sum(V1),
#          sdv3  = sd(V3))]
#          
#    sumv1      sdv3
# 1:    13 0.4330127
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, {"sumV1" : dt.sum(f.V1), 
#        "sdv3" : dt.sd(f.V3)}]
# 
#    | sumV1      sdv3
#    | int64   float64
# -- + -----  --------
#  0 |    13  0.433013
# [1 row x 2 columns]
# 
# 
# 
# ```
# 
# ````

# <p align="center"> Summarise a Subset of Rows </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[1:4, sum(V1)]
# 
# [1] 6
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:4, dt.sum(f.V1)]
# 
#    |    V1
#    | int64
# -- + -----
#  0 |     6
# [1 row x 1 column]
# 
# DF[:4, 'V1'].sum()
# 
#    |      V1
#    | float64
# -- + -------
#  0 |       6
# [1 row x 1 column]
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > DT[, data.table::first(V3)]
# [1] 0.5
# 
# 
# ```
# ---
# 
# 
# 
# ```python
#    
# DF[0, 'V3'] # returns a scalar
# 
# 0.5
# 
# DF[:, dt.first(f.V3)] # returns a frame
# 
#    |      V3
#    | float64
# -- + -------
#  0 |     0.5
# [1 row x 1 column]
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > DT[, data.table::last(V3)]
# [1] 1.5
# 
# 
# ```
# ---
# 
# 
# 
# ```python
#    
# DF[-1, 'V3'] # returns a scalar
# 
# 1.5
# 
# DF[:, dt.last(f.V3)] # returns a frame
# 
#    |      V3
#    | float64
# -- + -------
#  0 |     1.5
# [1 row x 1 column]
# 
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > DT[5, V3]
# 
# [1] 1
# 
# ```
# ---
# 
# 
# 
# ```python
#    
# DF[4, 'V3']
# 
# 1.0
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > DT[, uniqueN(V4)]
# 
# [1] 3
# 
# 
# ```
# ---
# 
# 
# ```python
# 
# DF['V4'].nunique1() # returns a scalar
# 
# 3
# 
#    
# DF['V4'].nunique() # returns a frame
# 
#    |    V4
#    | int64
# -- + -----
#  0 |     3
# [1 row x 1 column]
# 
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > uniqueN(DT)
# 
# [1] 9
# 
# 
# ```
# ---
# 
# 
# ```python
#    
# # nunique() returns number of unique values per column
# # not the number of unique rows in the frame
# DF.nunique()
# 
#    |    V1     V2     V3     V4
#    | int64  int64  int64  int64
# -- + -----  -----  -----  -----
#  0 |     2      9      3      3
# [1 row x 4 columns]
# 
# # possible solution
# max(frame.nunique1() for frame in DF)
# 
# 9
# 
# 
# ```
# 
# ````

# ### Add/Update/Delete Columns

# <p align="center"> Modify a Column </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, V1 := V1^2]
# 
# > DT
# 
#    V1 V2  V3 V4
# 1:  1  1 0.5  A
# 2:  4  2 1.0  B
# 3:  1  3 1.5  C
# 4:  4  4 0.5  A
# 5:  1  5 1.0  B
# 6:  4  6 1.5  C
# 7:  1  7 0.5  A
# 8:  4  8 1.0  B
# 9:  1  9 1.5  C
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF['V1'] = DF[:, f.V1**2]
# 
# # same
# # in place operation, 
# # no need for reassignment
# DF[:, update(V1 = f.V1 **2)] 
# 
# DF
# 
#    |      V1     V2       V3  V4   
#    | float64  int32  float64  str32
# -- + -------  -----  -------  -----
#  0 |       1      1      0.5  A    
#  1 |       4      2      1    B    
#  2 |       1      3      1.5  C    
#  3 |       4      4      0.5  A    
#  4 |       1      5      1    B    
#  5 |       4      6      1.5  C    
#  6 |       1      7      0.5  A    
#  7 |       4      8      1    B    
#  8 |       1      9      1.5  C    
# [9 rows x 4 columns]
# 
# 
# 
# ```
# 
# ````

# <p align="center"> Add One Column </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
#  # adding [] prints the result
# > DT[, v5 := log(V1)][]
# 
#    V1 V2  V3 V4       v5
# 1:  1  1 0.5  A 0.000000
# 2:  4  2 1.0  B 1.386294
# 3:  1  3 1.5  C 0.000000
# 4:  4  4 0.5  A 1.386294
# 5:  1  5 1.0  B 0.000000
# 6:  4  6 1.5  C 1.386294
# 7:  1  7 0.5  A 0.000000
# 8:  4  8 1.0  B 1.386294
# 9:  1  9 1.5  C 0.000000
# > 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF = DF[:, f[:].extend({"v5" : dt.log(f.V1)})]
# 
# DF['v5'] = DF[:, dt.log(f.V1)] # same
# 
# DF[:, update(v5 = dt.log(f.V1))] # same
# 
#    |      V1     V2       V3  V4          v5
#    | float64  int32  float64  str32  float64
# -- + -------  -----  -------  -----  -------
#  0 |       1      1      0.5  A      0      
#  1 |       4      2      1    B      1.38629
#  2 |       1      3      1.5  C      0      
#  3 |       4      4      0.5  A      1.38629
#  4 |       1      5      1    B      0      
#  5 |       4      6      1.5  C      1.38629
#  6 |       1      7      0.5  A      0      
#  7 |       4      8      1    B      1.38629
#  8 |       1      9      1.5  C      0      
# [9 rows x 5 columns]
# 
# 
# ```
# 
# ````

# <p align="center"> Add Several Columns </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, c("v6", "v7") := .(sqrt(V1), "X")]
# 
# # same, functional form
# > DT[, ':='(v6 = sqrt(V1),
#             v7 = "X")]  
#  
# > DT
#    V1 V2  V3 V4       v5 v6 v7
# 1:  1  1 0.5  A 0.000000  1  X
# 2:  4  2 1.0  B 1.386294  2  X
# 3:  1  3 1.5  C 0.000000  1  X
# 4:  4  4 0.5  A 1.386294  2  X
# 5:  1  5 1.0  B 0.000000  1  X
# 6:  4  6 1.5  C 1.386294  2  X
# 7:  1  7 0.5  A 0.000000  1  X
# 8:  4  8 1.0  B 1.386294  2  X
# 9:  1  9 1.5  C 0.000000  1  X
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF = DF[:, f[:].extend({"v6" : f.V1 ** 0.5, 
#                         "v7" : "X"})]
# 
# DF[:, update(v6 = f.V1 ** 0.5, 
#              v7 = "X")] # same
# 
# DF
# 
#    |      V1     V2       V3  V4          v5       v6  v7   
#    | float64  int32  float64  str32  float64  float64  str32
# -- + -------  -----  -------  -----  -------  -------  -----
#  0 |       1      1      0.5  A      0              1  X    
#  1 |       4      2      1    B      1.38629        2  X    
#  2 |       1      3      1.5  C      0              1  X    
#  3 |       4      4      0.5  A      1.38629        2  X    
#  4 |       1      5      1    B      0              1  X    
#  5 |       4      6      1.5  C      1.38629        2  X    
#  6 |       1      7      0.5  A      0              1  X    
#  7 |       4      8      1    B      1.38629        2  X    
#  8 |       1      9      1.5  C      0              1  X    
# [9 rows x 7 columns]
# 
# 
# 
# ```
# 
# ````

# <p align="center"> Create One Column and Remove the Others </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, .(v8 = V3 + 1)]
# 
#     v8
# 1: 1.5
# 2: 2.0
# 3: 2.5
# 4: 1.5
# 5: 2.0
# 6: 2.5
# 7: 1.5
# 8: 2.0
# 9: 2.5
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, {"v8" : f.V3 + 1}]
# 
# DF[:, dict(v8 = 1 + f.V3)] # same
# 
#    |      v8
#    | float64
# -- + -------
#  0 |     1.5
#  1 |     2  
#  2 |     2.5
#  3 |     1.5
#  4 |     2  
#  5 |     2.5
#  6 |     1.5
#  7 |     2  
#  8 |     2.5
# [9 rows x 1 column]
# 
# 
# ```
# 
# ````

# <p align="center"> Remove One Column </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, v5 := NULL]
# 
# > DT
# 
#    V1 V2  V3 V4 v6 v7
# 1:  1  1 0.5  A  1  X
# 2:  4  2 1.0  B  2  X
# 3:  1  3 1.5  C  1  X
# 4:  4  4 0.5  A  2  X
# 5:  1  5 1.0  B  1  X
# 6:  4  6 1.5  C  2  X
# 7:  1  7 0.5  A  1  X
# 8:  4  8 1.0  B  2  X
# 9:  1  9 1.5  C  1  X
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# del DF['v5']
# 
# DF
# 
#    |      V1     V2       V3  V4          v6  v7   
#    | float64  int32  float64  str32  float64  str32
# -- + -------  -----  -------  -----  -------  -----
#  0 |       1      1      0.5  A            1  X    
#  1 |       4      2      1    B            2  X    
#  2 |       1      3      1.5  C            1  X    
#  3 |       4      4      0.5  A            2  X    
#  4 |       1      5      1    B            1  X    
#  5 |       4      6      1.5  C            2  X    
#  6 |       1      7      0.5  A            1  X    
#  7 |       4      8      1    B            2  X    
#  8 |       1      9      1.5  C            1  X    
# [9 rows x 6 columns]
# 
# 
# 
# ```
# 
# ````

# <p align="center"> Remove Several Columns </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, c("v6", "v7") := NULL]
# 
# > DT
# 
#    V1 V2  V3 V4
# 1:  1  1 0.5  A
# 2:  4  2 1.0  B
# 3:  1  3 1.5  C
# 4:  4  4 0.5  A
# 5:  1  5 1.0  B
# 6:  4  6 1.5  C
# 7:  1  7 0.5  A
# 8:  4  8 1.0  B
# 9:  1  9 1.5  C
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# del DF[:, ['v6', 'v7']]
# 
# DF
# 
#    |      V1     V2       V3  V4   
#    | float64  int32  float64  str32
# -- + -------  -----  -------  -----
#  0 |       1      1      0.5  A    
#  1 |       4      2      1    B    
#  2 |       1      3      1.5  C    
#  3 |       4      4      0.5  A    
#  4 |       1      5      1    B    
#  5 |       4      6      1.5  C    
#  6 |       1      7      0.5  A    
#  7 |       4      8      1    B    
#  8 |       1      9      1.5  C    
# [9 rows x 4 columns]
# 
# 
# 
# ```
# 
# ````

# <p align="center"> Remove Columns using a Vector of Colnames </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > cols <- c("V3")
# 
# > DT[, (cols) := NULL] # ! not DT[, cols := NULL]
# 
# > DT
# 
#    V1 V2 V4
# 1:  1  1  A
# 2:  4  2  B
# 3:  1  3  C
# 4:  4  4  A
# 5:  1  5  B
# 6:  4  6  C
# 7:  1  7  A
# 8:  4  8  B
# 9:  1  9  C
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# cols = 'V3'
# 
# del DF[cols]
# 
# DF
# 
#    |      V1     V2  V4   
#    | float64  int32  str32
# -- + -------  -----  -----
#  0 |       1      1  A    
#  1 |       4      2  B    
#  2 |       1      3  C    
#  3 |       4      4  A    
#  4 |       1      5  B    
#  5 |       4      6  C    
#  6 |       1      7  A    
#  7 |       4      8  B    
#  8 |       1      9  C    
# [9 rows x 3 columns]
# 
# 
# ```
# 
# ````

# <p align="center"> Replace Values for Rows Matching a Condition </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[V2 < 4, V2 := 0L]
# 
# > DT
# 
#    V1 V2 V4
# 1:  1  0  A
# 2:  4  0  B
# 3:  1  0  C
# 4:  4  4  A
# 5:  1  5  B
# 6:  4  6  C
# 7:  1  7  A
# 8:  4  8  B
# 9:  1  9  C
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[f.V2 < 4, update(V2 = 0)]
# 
# DF[f.V2 < 4, 'V2'] = 0 # same
# 
# DF
# 
#    |      V1     V2  V4   
#    | float64  int32  str32
# -- + -------  -----  -----
#  0 |       1      0  A    
#  1 |       4      0  B    
#  2 |       1      0  C    
#  3 |       4      4  A    
#  4 |       1      5  B    
#  5 |       4      6  C    
#  6 |       1      7  A    
#  7 |       4      8  B    
#  8 |       1      9  C    
# [9 rows x 3 columns]
# 
# 
# 
# ```
# 
# ````

# ### By

# <p align="center"> By Group </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > # one-liner:
# > DT[, .(sumV2 = sum(V2)), by = "V4"]
# 
#    V4 sumV2
# 1:  A    11
# 2:  B    13
# 3:  C    15
# 
# > # reordered and indented:
# > DT[, by = V4,
#        .(sumV2 = sum(V2))]
# 
#    V4 sumV2
# 1:  A    11
# 2:  B    13
# 3:  C    15
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, {"sumV2" : dt.sum(f.V2)}, by('V4')]
# 
#    | V4     sumV2
#    | str32  int64
# -- + -----  -----
#  0 | A         11
#  1 | B         13
#  2 | C         15
# [3 rows x 2 columns]
# 
# 
# ```
# 
# ````

# <p align="center"> By Several Groups </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, keyby = .(V4, V1),
#        .(sumV2 = sum(V2))]
#        
#    V4 V1 sumV2
# 1:  A  1     7
# 2:  A  4     4
# 3:  B  1     5
# 4:  B  4     8
# 5:  C  1     9
# 6:  C  4     6
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, {"sumV2" : dt.sum(f.V2)}, by('V4', 'V1')]
# 
#    | V4          V1  sumV2
#    | str32  float64  int64
# -- + -----  -------  -----
#  0 | A            1      7
#  1 | A            4      4
#  2 | B            1      5
#  3 | B            4      8
#  4 | C            1      9
#  5 | C            4      6
# [6 rows x 3 columns]
# 
# 
# 
# ```
# 
# ````

# <p align="center"> Calling Function in By </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, by = tolower(V4),
#        .(sumV1 = sum(V1))]
#        
#    tolower sumV1
# 1:       a     6
# 2:       b     9
# 3:       c     6
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# # no equivalent string function
# 
# 
# ```
# 
# ````

# <p align="center"> Assigning Column Name in By </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, keyby = .(abc = tolower(V4)),
#        .(sumV1 = sum(V1))]
#        
#    abc sumV1
# 1:   a     6
# 2:   b     9
# 3:   c     6
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# # assigning column names in `by`
# # is not possible in datatable
# 
# 
# ```
# 
# ````

# <p align="center"> Using a Condition in By </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, keyby = V4 == "A",
#        sum(V1)]
# 
#       V4 V1
# 1: FALSE 15
# 2:  TRUE  6
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, dt.sum(f.V1), by(f.V4 == "A")]
# 
#    |    C0       V1
#    | bool8  float64
# -- + -----  -------
#  0 |     0       15
#  1 |     1        6
# [2 rows x 2 columns]
# 
# 
# 
# ```
# 
# ````

# <p align="center"> By on a Subset of Rows </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[1:5,                # i
#      .(sumV1 = sum(V1)), # j
#      by = V4]            # by
# 
#    V4 sumV1
# 1:  A     5
# 2:  B     5
# 3:  C     1
# ## complete DT[i, j, by] expression!
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# # in datatable computation occurs in `by`
# # before `i`,
# # unlike in `data.table`, where computation in `i`
# # comes before `by`
# DF[:5, dt.sum(f.V1), 'V4'] # wrong output
# 
#    | V4          V1
#    | str32  float64
# -- + -----  -------
#  0 | A            6
#  1 | B            9
#  2 | C            6
# [3 rows x 2 columns]
# 
# # to get the right result, filter in `i`
# # then chain the `by` computation
# 
# DF[:5, :][:, dict(sumV1 = dt.sum(f.V1)), by('V4')]
# 
#    | V4       sumV1
#    | str32  float64
# -- + -----  -------
#  0 | A            5
#  1 | B            5
#  2 | C            1
# [3 rows x 2 columns]
# 
# ```
# 
# ````

# <p align="center"> Count Number of Observations for each Group </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, .N, by = V4]
# 
#    V4 N
# 1:  A 3
# 2:  B 3
# 3:  C 3
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, dt.count(), by('V4')]
# 
#    | V4     count
#    | str32  int64
# -- + -----  -----
#  0 | A          3
#  1 | B          3
#  2 | C          3
# [3 rows x 2 columns]
# 
# 
# 
# ```
# 
# ````

# <p align="center"> Add a Column with Number of Observations for each Group </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, n := .N, by = V1][]
# 
#    V1 V2 V4 n
# 1:  1  0  A 5
# 2:  4  0  B 4
# 3:  1  0  C 5
# 4:  4  4  A 4
# 5:  1  5  B 5
# 6:  4  6  C 4
# 7:  1  7  A 5
# 8:  4  8  B 4
# 9:  1  9  C 5
# 
# > DT[, n := NULL] # rm column for consistency
# 
# > DT
# 
#    V1 V2 V4
# 1:  1  0  A
# 2:  4  0  B
# 3:  1  0  C
# 4:  4  4  A
# 5:  1  5  B
# 6:  4  6  C
# 7:  1  7  A
# 8:  4  8  B
# 9:  1  9  C
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[:, f[:].extend({"n" : dt.count()}), "V1"]
# 
#    |      V1     V2  V4         n
#    | float64  int32  str32  int64
# -- + -------  -----  -----  -----
#  0 |       1      0  A          5
#  1 |       1      0  C          5
#  2 |       1      5  B          5
#  3 |       1      7  A          5
#  4 |       1      9  C          5
#  5 |       4      0  B          4
#  6 |       4      4  A          4
#  7 |       4      6  C          4
#  8 |       4      8  B          4
# [9 rows x 4 columns]
# 
# # note how `update` maintains the original data form
# DF[:, update(n = dt.count()), "V1"]
# 
# DF
# 
#    |      V1     V2  V4         n
#    | float64  int32  str32  int64
# -- + -------  -----  -----  -----
#  0 |       1      0  A          5
#  1 |       4      0  B          4
#  2 |       1      0  C          5
#  3 |       4      4  A          4
#  4 |       1      5  B          5
#  5 |       4      6  C          4
#  6 |       1      7  A          5
#  7 |       4      8  B          4
#  8 |       1      9  C          5
# [9 rows x 4 columns]
# 
# del DF['n'] # remove column for consistency
# 
# DF
#  
#    |      V1     V2  V4   
#    | float64  int32  str32
# -- + -------  -----  -----
#  0 |       1      0  A    
#  1 |       4      0  B    
#  2 |       1      0  C    
#  3 |       4      4  A    
#  4 |       1      5  B    
#  5 |       4      6  C    
#  6 |       1      7  A    
#  7 |       4      8  B    
#  8 |       1      9  C    
# [9 rows x 3 columns]
# 
# 
# 
# ```
# 
# ````

# <p align="center"> Retrieve the First/Last/Nth Observation for each Group </p>
# 

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, data.table::first(V2), by = V4]
# 
#    V4 V1
# 1:  A  0
# 2:  B  0
# 3:  C  0
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
#    
# DF[0, 'V2', 'V4']
# 
# DF[:, dt.first(f.V2), 'V4'] # same
# 
#    | V4        V2
#    | str32  int32
# -- + -----  -----
#  0 | A          0
#  1 | B          0
#  2 | C          0
# [3 rows x 2 columns]
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > DT[, data.table::last(V2), by = V4]
# 
#    V4 V1
# 1:  A  7
# 2:  B  8
# 3:  C  9
# 
# 
# ```
# ---
# 
# 
# 
# ```python
#    
# DF[-1, 'V2', 'V4']
# 
# DF[:, dt.last(f.V2), 'V4'] # same
# 
#    | V4        V2
#    | str32  int32
# -- + -----  -----
#  0 | A          7
#  1 | B          8
#  2 | C          9
# [3 rows x 2 columns]
# 
# 
# ```
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > DT[, V2[2], by = V4]
# 
#    V4 V1
# 1:  A  4
# 2:  B  5
# 3:  C  6
# 
# 
# ```
# ---
# 
# 
# 
# ```python
#    
# DF[1, 'V2', 'V4']
#  
#    | V4        V2
#    | str32  int32
# -- + -----  -----
#  0 | A          4
#  1 | B          5
#  2 | C          6
# [3 rows x 2 columns]
# 
# ```
# 
# ````

# ## **Going Further**

# ### Advanced Columns Manipulation

# <p align="center">  Summarise all the Columns </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, lapply(.SD, max)]
# 
#    V1 V2 V4
# 1:  4  9  C
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # aggregations not currently 
# # applicable to string columns
# 
# DF[:, dt.max(f[int, float])]
#  
#    |    V2       V1
#    | int32  float64
# -- + -----  -------
#  0 |     9        4
# [1 row x 2 columns]
# 
# DF.max()
#  
#    |      V1     V2  V4   
#    | float64  int32  str32
# -- + -------  -----  -----
#  0 |       4      9  NA   
# [1 row x 3 columns]
# 
# ```
# 
# 
# ````

# <p align="center">  Summarise Several Columns </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, lapply(.SD, mean),
#        .SDcols = c("V1", "V2")]
#        
#          V1       V2
# 1: 2.333333 4.333333
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[:, dt.mean(f['V1', 'V2'])]
# 
# DF[:, ('V1', 'V2')].mean() # same
#  
#    |      V1       V2
#    | float64  float64
# -- + -------  -------
#  0 | 2.33333  4.33333
# [1 row x 2 columns]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Summarise Several Columns by Group </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, by = V4,
#        lapply(.SD, mean),
#        .SDcols = c("V1", "V2")]
#        
#    V4 V1       V2
# 1:  A  2 3.666667
# 2:  B  3 4.333333
# 3:  C  2 5.000000
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[:, dt.mean(f['V1', 'V2']), 'V4']
# 
#    | V4          V1       V2
#    | str32  float64  float64
# -- + -----  -------  -------
#  0 | A            2  3.66667
#  1 | B            3  4.33333
#  2 | C            2  5      
# [3 rows x 3 columns]
# 
# 
# ```
# 
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# ## using patterns (regex)
# > DT[, by = V4,
#        lapply(.SD, mean),
#        .SDcols = patterns("V1|V2|Z0")]
#        
#    V4 V1       V2
# 1:  A  2 3.666667
# 2:  B  3 4.333333
# 3:  C  2 5.000000
# 
# 
# ```
# ---
# 
# 
# 
# ```python
# 
# cols = [name for name in DF.names
#         if re.search("V1|V2|Z0", name)]
# 
# DF[:, dt.mean(f[cols]), 'V4']
# 
#    | V4          V1       V2
#    | str32  float64  float64
# -- + -----  -------  -------
#  0 | A            2  3.66667
#  1 | B            3  4.33333
#  2 | C            2  5      
# [3 rows x 3 columns]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Summarise with more than one Function by Group </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, by = V4,
#        c(lapply(.SD, sum),
#          lapply(.SD, mean))]
#          
#    V4 V1 V2 V1       V2
# 1:  A  6 11  2 3.666667
# 2:  B  9 13  3 4.333333
# 3:  C  6 15  2 5.000000
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[:, [dt.sum(f[:]), dt.mean(f[:])], 'V4']
# 
#    | V4          V1     V2       V3       V5
#    | str32  float64  int64  float64  float64
# -- + -----  -------  -----  -------  -------
#  0 | A            6     11        2  3.66667
#  1 | B            9     13        3  4.33333
#  2 | C            6     15        2  5      
# [3 rows x 5 columns]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Summarise using a Condition </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, lapply(.SD, mean),
#        .SDcols = is.numeric]
#        
#          V1       V2
# 1: 2.333333 4.333333
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[:, dt.mean(f[int, float])]
#  
#    |      V2       V1
#    | float64  float64
# -- + -------  -------
#  0 | 4.33333  2.33333
# [1 row x 2 columns]
# 
# ```
# 
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > foo <- function(x) {is.numeric(x) && mean(x) > 3}
# 
# > DT[, lapply(.SD, mean),
#      .SDcols = foo]
# 
#          V2
# 1: 4.333333
# 
# ```
# ---
# 
# 
# 
# ```python
# 
# columns_to_select = [name for name, ltype 
#                      in zip(DF.names, DF.ltypes) 
#                      if ltype in (ltype.real, ltype.int) 
#                      and DF[name].mean1() > 3]
# 
# DF[:, dt.mean(f[columns_to_select])]
#  
#    |      V2
#    | float64
# -- + -------
#  0 | 4.33333
# [1 row x 1 column]
# 
# 
# # another solution involving cbind
# # first solution is a bit faster
# frames = [frame.mean() for frame in DF 
#           if frame.ltypes[0] in (ltype.int, ltype.real) 
#           and frame.mean1() > 3 ]
#           
# dt.cbind(frames)
# # since only one frame is returned
# # cbind is unnecessary,
# # frames[0] is sufficient.
#  
#    |      V2
#    | float64
# -- + -------
#  0 | 4.33333
# [1 row x 1 column]
# 
# ```
# 
# 
# ````

# <p align="center">  Modify all the Columns </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, lapply(.SD, rev)]
# 
#    V1 V2 V4
# 1:  1  9  C
# 2:  4  8  B
# 3:  1  7  A
# 4:  4  6  C
# 5:  1  5  B
# 6:  4  4  A
# 7:  1  0  C
# 8:  4  0  B
# 9:  1  0  A
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[::-1, :]
#  
#    |      V1     V2  V4   
#    | float64  int32  str32
# -- + -------  -----  -----
#  0 |       1      9  C    
#  1 |       4      8  B    
#  2 |       1      7  A    
#  3 |       4      6  C    
#  4 |       1      5  B    
#  5 |       4      4  A    
#  6 |       1      0  C    
#  7 |       4      0  B    
#  8 |       1      0  A    
# [9 rows x 3 columns]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Modify Several Columns (Dropping the Others) </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, lapply(.SD, sqrt),
#        .SDcols = V1:V2]
#    V1       V2
# 1:  1 0.000000
# 2:  2 0.000000
# 3:  1 0.000000
# 4:  2 2.000000
# 5:  1 2.236068
# 6:  2 2.449490
# 7:  1 2.645751
# 8:  2 2.828427
# 9:  1 3.000000
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[:, f['V1', 'V2'] ** 0.5]
# 
# DF[:, dt.math.sqrt(f['V1', 'V2'])] # same
#  
#    |      C0       C1
#    | float64  float64
# -- + -------  -------
#  0 |       1  0      
#  1 |       2  0      
#  2 |       1  0      
#  3 |       2  2      
#  4 |       1  2.23607
#  5 |       2  2.44949
#  6 |       1  2.64575
#  7 |       2  2.82843
#  8 |       1  3      
# [9 rows x 2 columns]
# 
# 
# ```
# 
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > DT[, lapply(.SD, exp),
#        .SDcols = !"V4"]
#           V1         V2
# 1:  2.718282    1.00000
# 2: 54.598150    1.00000
# 3:  2.718282    1.00000
# 4: 54.598150   54.59815
# 5:  2.718282  148.41316
# 6: 54.598150  403.42879
# 7:  2.718282 1096.63316
# 8: 54.598150 2980.95799
# 9:  2.718282 8103.08393
# 
# 
# ```
# ---
# 
# 
# 
# ```python
# 
# DF[:, dt.exp(f[:].remove(f.V4))]
#  
#    |       V1         V2
#    |  float64    float64
# -- + --------  ---------
#  0 |  2.71828     1     
#  1 | 54.5982      1     
#  2 |  2.71828     1     
#  3 | 54.5982     54.5982
#  4 |  2.71828   148.413 
#  5 | 54.5982    403.429 
#  6 |  2.71828  1096.63  
#  7 | 54.5982   2980.96  
#  8 |  2.71828  8103.08  
# [9 rows x 2 columns]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Modify Several Columns (Keeping the Others) </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, c("V1", "V2") := lapply(.SD, sqrt),
#       .SDcols = c("V1", "V2")]
#       
# > DT
# 
#    V1       V2 V4
# 1:  1 0.000000  A
# 2:  2 0.000000  B
# 3:  1 0.000000  C
# 4:  2 2.000000  A
# 5:  1 2.236068  B
# 6:  2 2.449490  C
# 7:  1 2.645751  A
# 8:  2 2.828427  B
# 9:  1 3.000000  C
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[:, ['V1', 'V2']] = DF[:, dt.math.sqrt(f['V1', 'V2'])]
# 
# # same
# mapping = {name : dt.math.sqrt(f[name]) 
#            for name in ('V1', 'V2')}
# DF[:, update(**mapping)]
# 
# DF
# 
#    |      V1       V2  V4   
#    | float64  float64  str32
# -- + -------  -------  -----
#  0 |       1  0        A    
#  1 |       2  0        B    
#  2 |       1  0        C    
#  3 |       2  2        A    
#  4 |       1  2.23607  B    
#  5 |       2  2.44949  C    
#  6 |       1  2.64575  A    
#  7 |       2  2.82843  B    
#  8 |       1  3        C    
# [9 rows x 3 columns]
# 
# 
# ```
# 
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > cols <- setdiff(names(DT), "V4")
# 
# > DT[, (cols) := lapply(.SD, "^", 2L),
#        .SDcols = cols]
#        
# > DT
#    V1 V2 V4
# 1:  1  0  A
# 2:  4  0  B
# 3:  1  0  C
# 4:  4  4  A
# 5:  1  5  B
# 6:  4  6  C
# 7:  1  7  A
# 8:  4  8  B
# 9:  1  9  C
# 
# 
# 
# ```
# ---
# 
# 
# 
# ```python
# 
#  DF[:, ['V1', 'V2']] = DF[:, dt.math.square(f['V1', 'V2'])]
# 
# #same
# mapping = {name : f[name] ** 2 
#            for name in ('V1', 'V2')}
#            
# # alternative
# mapping = {name: f[name] ** 2
#            for name in DF.names
#            if name != "V4"}
#            
# DF[:, update(**mapping)]
# 
# DF
#  
#    |      V1       V2  V4   
#    | float64  float64  str32
# -- + -------  -------  -----
#  0 |       1        0  A    
#  1 |       4        0  B    
#  2 |       1        0  C    
#  3 |       4        4  A    
#  4 |       1        5  B    
#  5 |       4        6  C    
#  6 |       1        7  A    
#  7 |       4        8  B    
#  8 |       1        9  C    
# [9 rows x 3 columns]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Modify Columns using a Condition (Dropping the Others) </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, .SD - 1,
#        .SDcols = is.numeric]
#        
#    V1 V2
# 1:  0 -1
# 2:  3 -1
# 3:  0 -1
# 4:  3  3
# 5:  0  4
# 6:  3  5
# 7:  0  6
# 8:  3  7
# 9:  0  8
# 
# > DT
# 
#    V1 V2 V4
# 1:  1  0  A
# 2:  4  0  B
# 3:  1  0  C
# 4:  4  4  A
# 5:  1  5  B
# 6:  4  6  C
# 7:  1  7  A
# 8:  4  8  B
# 9:  1  9  C
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[:, f[int, float] - 1]
#  
#    |      C0       C1
#    | float64  float64
# -- + -------  -------
#  0 |       0       -1
#  1 |       3       -1
#  2 |       0       -1
#  3 |       3        3
#  4 |       0        4
#  5 |       3        5
#  6 |       0        6
#  7 |       3        7
#  8 |       0        8
# [9 rows x 2 columns]
# 
# DF
# 
#           V1       V2  V4   
#    | float64  float64  str32
# -- + -------  -------  -----
#  0 |       1        0  A    
#  1 |       4        0  B    
#  2 |       1        0  C    
#  3 |       4        4  A    
#  4 |       1        5  B    
#  5 |       4        6  C    
#  6 |       1        7  A    
#  7 |       4        8  B    
#  8 |       1        9  C    
# [9 rows x 3 columns]
# 
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Modify Columns using a Condition (Keeping the Others) </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, (cols) := lapply(.SD, as.integer),
#        .SDcols = is.numeric]
#        
# > DT
# 
#    V1 V2 V4
# 1:  1  0  A
# 2:  4  0  B
# 3:  1  0  C
# 4:  4  4  A
# 5:  1  5  B
# 6:  4  5  C
# 7:  1  7  A
# 8:  4  8  B
# 9:  1  9  C
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[:, ['V1', 'V2']] = DF[:, dt.as_type([f.V1, f.V2], int)]
# 
# # same
# # alternate approach, using the dtype itself
# numeric = {name : dt.int32(f[name]) 
#            for name, ltype in zip(DF.names, DF.ltypes) 
#            if ltype in (ltype.int, ltype.real)}
# 
# DF[:, update(**numeric)]
# 
# DF
#  
#    |    V1     V2  V4   
#    | int32  int32  str32
# -- + -----  -----  -----
#  0 |     1      0  A    
#  1 |     4      0  B    
#  2 |     1      0  C    
#  3 |     4      4  A    
#  4 |     1      5  B    
#  5 |     4      5  C    
#  6 |     1      7  A    
#  7 |     4      8  B    
#  8 |     1      9  C    
# [9 rows x 3 columns]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Use a Complex Expression </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, by = V4,
#       .(V1[1:2], "X")]
#       
#    V4 V1 V2
# 1:  A  1  X
# 2:  A  4  X
# 3:  B  4  X
# 4:  B  1  X
# 5:  C  1  X
# 6:  C  4  X
# 
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[:2, f.V1.extend({"V2" : "X"}), "V4"]
# 
#    | V4        V1  V2   
#    | str32  int32  str32
# -- + -----  -----  -----
#  0 | A          1  X    
#  1 | A          4  X    
#  2 | B          4  X    
#  3 | B          1  X    
#  4 | C          1  X    
#  5 | C          4  X    
# [6 rows x 3 columns]
# 
# ```
# 
# 
# ````

# <p align="center"> Use Multiple Expressions (with DT[,{j}]) </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, {print(V1) #  comments here!
#         print(summary(V1))
#         x <- V1 + sum(V2)
#        .(A = 1:.N, B = x) # last list returned as a data.table
#        }]
#        
# [1] 1 4 1 4 1 4 1 4 1
# 
#    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#   1.000   1.000   1.000   2.333   4.000   4.000 
#   
#    A  B
# 1: 1 39
# 2: 2 42
# 3: 3 39
# 4: 4 42
# 5: 5 39
# 6: 6 42
# 7: 7 39
# 8: 8 42
# 9: 9 39
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # not applicable in datatable
# 
# ```
# 
# 
# ````

# ### Chain Expressions

# <p align="center">  Expression Chaining using DT[][] </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, by = V4, 
#       .(V1sum = sum(V1)) ][
#       V1sum > 5]
#       
#    V4 V1sum
# 1:  A     6
# 2:  B     9
# 3:  C     6
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[:, dict(V1sum = dt.sum(f.V1)), 'V4'][f.V1sum > 5, :]
#  
#    | V4     V1sum
#    | str32  int64
# -- + -----  -----
#  0 | A          6
#  1 | B          9
#  2 | C          6
# [3 rows x 2 columns]
# 
# 
# ```
# 
# 
# ````

# ## **Indexing and Keys**

# Skipping this section as [datatable's](https://datatable.readthedocs.io/en/latest/) keys are primarily for joins (which are limited at the moment). Basically, there is no equivalent for the host of functions enabled with indexes in [data.table](https://rdatatable.gitlab.io/data.table/).
# 
# In keeping with the same data used on [atrebas'](https://twitter.com/atrebas/status/1287435078247813121) [guide](https://atrebas.github.io/post/2020-06-14-datatable-pandas/), the data going forward is the result of the [indexing operations](https://atrebas.github.io/post/2020-06-14-datatable-pandas/#indexing-and-keys) (I just did a copy and paste). I chose this step for readers who may be following [atrebas'](https://twitter.com/atrebas/status/1287435078247813121) [guide](https://atrebas.github.io/post/2020-06-14-datatable-pandas/) and would want to keep in sync with the results.

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# **data.table**
# ^^^
# 
# ```R
# 
#     ## Create new data table
#     DT <- data.table(
#             V1 = c(0L, 0L, 0L, 1L, 4L, 4L, 1L, 1L, 4L),
#             V2 = c(0L, 4L, 7L, 5L, 0L, 8L, 0L, 9L, 5L),
#             V4 = rep(c('A', 'B', 'C'), each = 3)
#             )
# 
#     > class(DT)
#     [1] "data.table" "data.frame"
#     
#     > DT
#        V1 V2 V4
#     1:  0  0  A
#     2:  0  4  A
#     3:  0  7  A
#     4:  1  5  B
#     5:  4  0  B
#     6:  4  8  B
#     7:  1  0  C
#     8:  1  9  C
#     9:  4  5  C
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
#     DF = dt.Frame(
#     [{'V1': 0, 'V2': 0, 'V4': 'A'},
#      {'V1': 0, 'V2': 4, 'V4': 'A'},
#      {'V1': 0, 'V2': 7, 'V4': 'A'},
#      {'V1': 1, 'V2': 5, 'V4': 'B'},
#      {'V1': 4, 'V2': 0, 'V4': 'B'},
#      {'V1': 4, 'V2': 8, 'V4': 'B'},
#      {'V1': 1, 'V2': 0, 'V4': 'C'},
#      {'V1': 1, 'V2': 9, 'V4': 'C'},
#      {'V1': 4, 'V2': 5, 'V4': 'C'}]
# 
#     type(DF)
#     datatable.Frame
# 
#     DF     
#        |    V1     V2  V4   
#        | int32  int32  str32
#     -- + -----  -----  -----
#      0 |     0      0  A    
#      1 |     0      4  A    
#      2 |     0      7  A    
#      3 |     1      5  B    
#      4 |     4      0  B    
#      5 |     4      8  B    
#      6 |     1      0  C    
#      7 |     1      9  C    
#      8 |     4      5  C    
#     [9 rows x 3 columns]
# 
# 
# ```
# 
# 
# ````

# ### Set*() Modifications

# <p align="center">  Replace Values </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > set(DT, i = 1L, j = 2L, value = 3L)
# 
# > DT
# 
#    V1 V2 V4
# 1:  0  3  A
# 2:  0  4  A
# 3:  0  7  A
# 4:  1  5  B
# 5:  4  0  B
# 6:  4  8  B
# 7:  1  0  C
# 8:  1  9  C
# 9:  4  5  C
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[0, 1] = 3
# 
# DF
# 
#    |    V1     V2  V4   
#    | int32  int32  str32
# -- + -----  -----  -----
#  0 |     0      3  A    
#  1 |     0      4  A    
#  2 |     0      7  A    
#  3 |     1      5  B    
#  4 |     4      0  B    
#  5 |     4      8  B    
#  6 |     1      0  C    
#  7 |     1      9  C    
#  8 |     4      5  C    
# [9 rows x 3 columns]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Reorder Rows </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > setorder(DT, V4, -V1)
# 
# > setorderv(DT, c("V4", "V1"), c(1, -1))
# 
# > DT
#    V1 V2 V4
# 1:  0  3  A
# 2:  0  4  A
# 3:  0  7  A
# 4:  4  0  B
# 5:  4  8  B
# 6:  1  5  B
# 7:  4  5  C
# 8:  1  0  C
# 9:  1  9  C
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF = DF.sort(f.V4, -f.V1)
# 
# DF
# 
#    |    V1     V2  V4   
#    | int32  int32  str32
# -- + -----  -----  -----
#  0 |     0      3  A    
#  1 |     0      4  A    
#  2 |     0      7  A    
#  3 |     4      0  B    
#  4 |     4      8  B    
#  5 |     1      5  B    
#  6 |     4      5  C    
#  7 |     1      0  C    
#  8 |     1      9  C    
# [9 rows x 3 columns]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Modify Colnames </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > setnames(DT, old = "V2", new = "v2")
# 
# > DT
# 
#    V1 v2 V4
# 1:  0  3  A
# 2:  0  4  A
# 3:  0  7  A
# 4:  4  0  B
# 5:  4  8  B
# 6:  1  5  B
# 7:  4  5  C
# 8:  1  0  C
# 9:  1  9  C
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF.names = {"V2" : "v2"}
# 
# DF
# 
#    |    V1     v2  V4   
#    | int32  int32  str32
# -- + -----  -----  -----
#  0 |     0      3  A    
#  1 |     0      4  A    
#  2 |     0      7  A    
#  3 |     4      0  B    
#  4 |     4      8  B    
#  5 |     1      5  B    
#  6 |     4      5  C    
#  7 |     1      0  C    
#  8 |     1      9  C    
# [9 rows x 3 columns]
# 
# 
# ```
# 
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > setnames(DT, old = -(c(1, 3)), new = "V2")
# 
# > DT
# 
#    V1 V2 V4
# 1:  0  3  A
# 2:  0  4  A
# 3:  0  7  A
# 4:  4  0  B
# 5:  4  8  B
# 6:  1  5  B
# 7:  4  5  C
# 8:  1  0  C
# 9:  1  9  C
# 
# 
# ```
# ---
# 
# ```python
# 
# DF.names = ["V2" 
#             if index not in (0, 2) 
#             else name 
#             for index, name 
#             in enumerate(DF.names)]
# 
# # same
# DF.names = ["V2" 
#             if DF.colindex(letter) not in (0, 2) 
#             else letter 
#             for letter in DF.names]
# 
# DF
# 
#    |    V1     V2  V4   
#    | int32  int32  str32
# -- + -----  -----  -----
#  0 |     0      3  A    
#  1 |     0      4  A    
#  2 |     0      7  A    
#  3 |     4      0  B    
#  4 |     4      8  B    
#  5 |     1      5  B    
#  6 |     4      5  C    
#  7 |     1      0  C    
#  8 |     1      9  C    
# [9 rows x 3 columns]
# 
# ```
# 
# 
# ````

# <p align="center">  Reorder Columns </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > setcolorder(DT, c("V4", "V1", "V2"))
# 
# > DT
# 
#    V4 V1 V2
# 1:  A  0  3
# 2:  A  0  4
# 3:  A  0  7
# 4:  B  4  0
# 5:  B  4  8
# 6:  B  1  5
# 7:  C  4  5
# 8:  C  1  0
# 9:  C  1  9
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF = DF[:, ['V4', 'V1', 'V2']]
# 
# DF
# 
#    | V4        V1     V2
#    | str32  int32  int32
# -- + -----  -----  -----
#  0 | A          0      3
#  1 | A          0      4
#  2 | A          0      7
#  3 | B          4      0
#  4 | B          4      8
#  5 | B          1      5
#  6 | C          4      5
#  7 | C          1      0
#  8 | C          1      9
# [9 rows x 3 columns]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Convert Data </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# # ?setDT # data.frame or list to data.table
# 
# # ?setDF # data.table to data.frame
# 
# # ?setattr # modify attributes
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # Wrapping pandas/numpy/dict/... 
# # with ``dt.Frame`` usually suffices.
# # when converting from other structures
# # to a datatable Frame.
# 
# # `to_pandas`/to_dict()/...
# # when converting a datatable Frame
# # to other data structures
# 
# ```
# 
# 
# ````

# ### Advanced Use of By

# <p align="center">  Select First/Last/… Row by Group </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, .SD[1], by = V4]
# 
#    V4 V1 V2
# 1:  A  0  3
# 2:  B  4  0
# 3:  C  4  5
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[0, :, 'V4']
# 
#    | V4        V1     V2
#    | str32  int32  int32
# -- + -----  -----  -----
#  0 | A          0      3
#  1 | B          4      0
#  2 | C          4      5
# [3 rows x 3 columns]
# 
# ```
# 
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > DT[, .SD[c(1, .N)], by = V4]
# 
#    V4 V1 V2
# 1:  A  0  3
# 2:  A  0  7
# 3:  B  4  0
# 4:  B  1  5
# 5:  C  4  5
# 6:  C  1  9
# 
# ```
# ---
# 
# 
# 
# ```python
# 
# # list selection in the `i` section
# # in the presence of `by`
# # is not yet implemented
# # the code below is a workaround
# # albeit not clean or scalable
# 
# DF[:, update(counter = range(DF.nrows))]
# min_rows = f.counter==dt.min(f.counter)
# max_rows = f.counter==dt.max(f.counter)
# DF[:, update(counter = min_rows|max_rows, "V4"]
# DF[f.counter==1, :-1]
# 
#    | V4        V1     V2
#    | str32  int32  int32
# -- + -----  -----  -----
#  0 | A          0      3
#  1 | A          0      7
#  2 | B          4      0
#  3 | B          1      5
#  4 | C          4      5
#  5 | C          1      9
# [6 rows x 3 columns]
# 
# DF = DF[:, :-1] #reset data
# 
# ```
# 
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > DT[, tail(.SD, 2), by = V4]
# 
#    V4 V1 V2
# 1:  A  0  4
# 2:  A  0  7
# 3:  B  4  8
# 4:  B  1  5
# 5:  C  1  0
# 6:  C  1  9
# 
# ```
# ---
# 
# 
# ```python
# 
# DF[-2:, :, 'V4']
# 
#    | V4        V1     V2
#    | str32  int32  int32
# -- + -----  -----  -----
#  0 | A          0      4
#  1 | A          0      7
#  2 | B          4      8
#  3 | B          1      5
#  4 | C          1      0
#  5 | C          1      9
# [6 rows x 3 columns]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Select Rows using a Nested Query </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, .SD[which.min(V2)], by = V4]
# 
#    V4 V1 V2
# 1:  A  0  3
# 2:  B  4  0
# 3:  C  1  0
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[:, update(counter = f.V2==dt.min(f.V2)), "V4"]
# 
# DF[f.counter == 1, :-1]
# 
#    | V4        V1     V2
#    | str32  int32  int32
# -- + -----  -----  -----
#  0 | A          0      3
#  1 | B          4      0
#  2 | C          1      0
# [3 rows x 3 columns]
# 
# DF = DF[:, :-1] # reset data
# 
# ```
# 
# 
# ````

# <p align="center">  Add a Group Counter Column </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, Grp := .GRP, by = .(V4, V1)][]
#    V4 V1 V2 Grp
# 1:  A  0  3   1
# 2:  A  0  4   1
# 3:  A  0  7   1
# 4:  B  4  0   2
# 5:  B  4  8   2
# 6:  B  1  5   3
# 7:  C  4  5   4
# 8:  C  1  0   5
# 9:  C  1  9   5
# 
# > DT[, Grp := NULL] # delete for consistency
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # no equivalent function
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Get Row Number of First (and Last) Observation by Group </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# # returns a data.table
# > DT[, .I, by = V4] 
# 
#    V4 I
# 1:  A 1
# 2:  A 2
# 3:  A 3
# 4:  B 4
# 5:  B 5
# 6:  B 6
# 7:  C 7
# 8:  C 8
# 9:  C 9
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF[:, update(I = range(DF.nrows))]
# 
# DF[:, f.I, "V4"]
#    | V4         I
#    | str32  int32
# -- + -----  -----
#  0 | A          0
#  1 | A          1
#  2 | A          2
#  3 | B          3
#  4 | B          4
#  5 | B          5
#  6 | C          6
#  7 | C          7
#  8 | C          8
# 
# 
# 
# ```
# 
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > DT[, .I[1], by = V4]
# 
#    V4 V1
# 1:  A  1
# 2:  B  4
# 3:  C  7
# 
# 
# 
# ```
# ---
# 
# 
# ```python
# 
# DF[0, f.I, 'V4']
# 
#    | V4         I
#    | str32  int32
# -- + -----  -----
#  0 | A          0
#  1 | B          3
#  2 | C          6
# 
# 
# 
# ```
# 
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > DT[, .I[c(1, .N)], by = V4]
# 
#    V4 V1
# 1:  A  1
# 2:  A  3
# 3:  B  4
# 4:  B  6
# 5:  C  7
# 6:  C  9
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # list selection in the `i` section
# # in the presence of `by`
# # is not yet implemented
# # this is a hack,
# # not efficient IMO
# dt.rbind(DF[0, f.I, "V4"], 
#          DF[-1, f.I, "V4"]).sort(f.V4])
#          
#    | V4         I
#    | str32  int32
# -- + -----  -----
#  0 | A          0
#  1 | A          2
#  2 | B          3
#  3 | B          5
#  4 | C          6
#  5 | C          8
# [6 rows x 2 columns]
# 
# DF = DF[:, :-1] # reset data
# 
# ```
# 
# 
# ````

# <p align="center">  Handle List-columns by Group </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > DT[, .(.(V1)),  by = V4]  # return V1 as a list
# 
#    V4    V1
# 1:  A 0,0,0
# 2:  B 4,4,1
# 3:  C 4,1,1
# 
# > DT[, .(.(.SD)), by = V4] # subsets of the data
# 
#    V4                V1
# 1:  A <data.table[3x2]>
# 2:  B <data.table[3x2]>
# 3:  C <data.table[3x2]>
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # datatable does not support list-columns
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Grouping Sets (Multiple By at Once) </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > rollup(DT,
#         .(SumV2 = sum(V2)),
#          by = c("V1", "V4"))
#          
#    V1   V4 SumV2
# 1:  0    A    14
# 2:  4    B     8
# 3:  1    B     5
# 4:  4    C     5
# 5:  1    C     9
# 6:  0 <NA>    14
# 7:  4 <NA>    13
# 8:  1 <NA>    14
# 9: NA <NA>    41
# 
# > rollup(DT,
#          .(SumV2 = sum(V2), .N),
#          by = c("V1", "V4"),
#          id = TRUE)
#          
#    grouping V1   V4 SumV2 N
# 1:        0  0    A    14 3
# 2:        0  4    B     8 2
# 3:        0  1    B     5 1
# 4:        0  4    C     5 1
# 5:        0  1    C     9 2
# 6:        1  0 <NA>    14 3
# 7:        1  4 <NA>    13 3
# 8:        1  1 <NA>    14 3
# 9:        3 NA <NA>    41 9
#  
# > cube(DT,
#        .(SumV2 = sum(V2), .N),
#        by = c("V1", "V4"),
#        id = TRUE)
# 
#     grouping V1   V4 SumV2 N
#  1:        0  0    A    14 3
#  2:        0  4    B     8 2
#  3:        0  1    B     5 1
#  4:        0  4    C     5 1
#  5:        0  1    C     9 2
#  6:        1  0 <NA>    14 3
#  7:        1  4 <NA>    13 3
#  8:        1  1 <NA>    14 3
#  9:        2 NA    A    14 3
# 10:        2 NA    B    13 3
# 11:        2 NA    C    14 3
# 12:        3 NA <NA>    41 9
#  
# > groupingsets(DT,
#                .(SumV2 = sum(V2), .N),
#                by   = c("V1", "V4"),
#                sets = list("V1", c("V1", "V4")),
#                id   = TRUE)
#                
#    grouping V1   V4 SumV2 N
# 1:        1  0 <NA>    14 3
# 2:        1  4 <NA>    13 3
# 3:        1  1 <NA>    14 3
# 4:        0  0    A    14 3
# 5:        0  4    B     8 2
# 6:        0  1    B     5 1
# 7:        0  4    C     5 1
# 8:        0  1    C     9 2
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # No equivalent
# 
# 
# ```
# 
# 
# ````

# ## **Miscellaneous**

# ### Read / Write Data

# <p align="center">  Write Data to a Csv File </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# fwrite(DT, "DT.csv")
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# DF.to_csv("DF.csv")
# 
# ```
# 
# 
# ````

# <p align="center"> Write Data to a Tab-delimited File </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# fwrite(DT, "DT.txt", sep = "\t")
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # no equivalent
# # text could be formatted as tab delimited
# # before exporting : DF.to_csv("tab-file.txt")
# 
# ```
# 
# 
# ````

# <p align="center">  Write List-column Data to a Csv File </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# fwrite(setDT(list(0, list(1:5))), "DT2.csv")
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # no equivalent
# 
# ```
# 
# 
# ````

# <p align="center"> Read a Csv / Tab-delimited File </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > fread("DT.csv")
# # fread("DT.csv", verbose = TRUE) # full details
# > fread("DT.txt", sep = "\t")
# 
#    V4 V1 V2
# 1:  A  0  3
# 2:  A  0  4
# 3:  A  0  7
# 4:  B  4  0
# 5:  B  4  8
# 6:  B  1  5
# 7:  C  4  5
# 8:  C  1  0
# 9:  C  1  9
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# dt.fread("DF.csv")
# dt.fread("DT.txt")
# 
#    | V4        V1     V2
#    | str32  int32  int32
# -- + -----  -----  -----
#  0 | A          0      3
#  1 | A          0      4
#  2 | A          0      7
#  3 | B          4      0
#  4 | B          4      8
#  5 | B          1      5
#  6 | C          4      5
#  7 | C          1      0
#  8 | C          1      9
# [9 rows x 3 columns]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Read a Csv File Selecting / Dropping Columns </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > fread("DT.csv", select = c("V1", "V4"))
#    V1 V4
# 1:  0  A
# 2:  0  A
# 3:  0  A
# 4:  4  B
# 5:  4  B
# 6:  1  B
# 7:  4  C
# 8:  1  C
# 9:  1  C
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# 
# dt.fread("DF.csv", columns={"V1", "V4"})
# 
# # selection/renaming possible with a dictionary
# dt.fread("DF.csv", 
#          columns = {"V1":"V1", 
#                     "V4":"V4", 
#                     ...:None})
# 
# 
#    | V4        V1
#    | str32  int32
# -- + -----  -----
#  0 | A          0
#  1 | A          0
#  2 | A          0
#  3 | B          4
#  4 | B          4
#  5 | B          1
#  6 | C          4
#  7 | C          1
#  8 | C          1
# [9 rows x 2 columns]
# 
# 
# ```
# 
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > fread("DT.csv", drop = "V4")
#    V1 V2
# 1:  0  3
# 2:  0  4
# 3:  0  7
# 4:  4  0
# 5:  4  8
# 6:  1  5
# 7:  4  5
# 8:  1  0
# 9:  1  9
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# dt.fread("DF.csv", columns = {"V4" : None})
# 
#    |    V1     V2
#    | int32  int32
# -- + -----  -----
#  0 |     0      3
#  1 |     0      4
#  2 |     0      7
#  3 |     4      0
#  4 |     4      8
#  5 |     1      5
#  6 |     4      5
#  7 |     1      0
#  8 |     1      9
# [9 rows x 2 columns]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Read and Rbind Several Files </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > rbindlist(lapply(c("DT.csv", 
#                     "DT.csv"), 
#             fread))
#             
#     V4 V1 V2
#  1:  A  0  3
#  2:  A  0  4
#  3:  A  0  7
#  4:  B  4  0
#  5:  B  4  8
#  6:  B  1  5
#  7:  C  4  5
#  8:  C  1  0
#  9:  C  1  9
# 10:  A  0  3
# 11:  A  0  4
# 12:  A  0  7
# 13:  B  4  0
# 14:  B  4  8
# 15:  B  1  5
# 16:  C  4  5
# 17:  C  1  0
# 18:  C  1  9
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# dt.rbind(dt.iread(["DT.csv", 
#                    "DT.csv"]))
# 
#    | V4        V1     V2
#    | str32  int32  int32
# -- + -----  -----  -----
#  0 | A          0      3
#  1 | A          0      4
#  2 | A          0      7
#  3 | B          4      0
#  4 | B          4      8
#  5 | B          1      5
#  6 | C          4      5
#  7 | C          1      0
#  8 | C          1      9
#  9 | A          0      3
# 10 | A          0      4
# 11 | A          0      7
# 12 | B          4      0
# 13 | B          4      8
# 14 | B          1      5
# 15 | C          4      5
# 16 | C          1      0
# 17 | C          1      9
# [18 rows x 3 columns]
# 
# 
# ```
# 
# 
# ````

# ### Reshape Data

# The reshape functions in R's [data.table](https://rdatatable.gitlab.io/data.table/) have no equivalents in Python's [datatable](https://datatable.readthedocs.io/en/latest/); they have not been implemented.

# <p align="center">  Check Package Installation </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# fwrite(DT, "DT.csv")
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # Check [tests](https://github.com/h2oai/datatable/tree/main/tests)
# 
# ```
# 
# 
# ````

# <p align="center">  List data.tables/tibbles </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# tables()
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # %whos Frame IPython
# 
# ```
# 
# 
# ````

# <p align="center">  Get/Set Number of Threads when Parallelized </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# getDTthreads() # setDTthreads()
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# dt.options.nthreads 
# # dt.options.nthreads = new_nthreads
# 
# ```
# 
# 
# ````

# <p align="center">  Lead/Lag </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > shift(1:10, n = 1,   fill = NA, type = "lag")
# 
#  [1] NA  1  2  3  4  5  6  7  8  9
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# dt.Frame(range(1,11))[:, dt.shift(f[0])]
# 
#    |    C0
#    | int32
# -- + -----
#  0 |    NA
#  1 |     1
#  2 |     2
#  3 |     3
#  4 |     4
#  5 |     5
#  6 |     6
#  7 |     7
#  8 |     8
#  9 |     9
# [10 rows x 1 column]
# 
# ```
# 
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > shift(1:10, n = 1:2, fill = NA, type = "lag") # multiple
# [[1]]
#  [1] NA  1  2  3  4  5  6  7  8  9
# 
# [[2]]
#  [1] NA NA  1  2  3  4  5  6  7  8
# 
# 
# 
# ```
# ---
# 
# 
# 
# ```python
# 
# dt.Frame([range(1,11)]*2)[:, [dt.shift(f[0], 1), 
#                               dt.shift(f[1], 2)]]
#                               
#    |    C0     C1
#    | int32  int32
# -- + -----  -----
#  0 |    NA     NA
#  1 |     1     NA
#  2 |     2      1
#  3 |     3      2
#  4 |     4      3
#  5 |     5      4
#  6 |     6      5
#  7 |     7      6
#  8 |     8      7
#  9 |     9      8
# [10 rows x 2 columns]
# 
# ```
# 
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# 
# ```R
# 
# > shift(1:10, n = 1,   fill = NA, type = "lead")
#  [1]  2  3  4  5  6  7  8  9 10 NA
# 
# 
# 
# ```
# ---
# 
# 
# ```python
# 
# dt.Frame(range(1,11))[:, dt.shift(f[0], -1)]
# 
#    |    C0
#    | int32
# -- + -----
#  0 |     2
#  1 |     3
#  2 |     4
#  3 |     5
#  4 |     6
#  5 |     7
#  6 |     8
#  7 |     9
#  8 |    10
#  9 |    NA
# [10 rows x 1 column]
# 
# ```
# 
# 
# ````

# <p align="center">  Generate Run-length Ids </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# > rleid(rep(c("a", "b", "a"), each = 3)) # see also ?rleidv
# 
# [1] 1 1 1 2 2 2 3 3 3
# 
# > rleid(rep(c("a", "b", "a"), each = 3), prefix = "G")
# 
# [1] "G1" "G1" "G1" "G2" "G2" "G2" "G3" "G3" "G3"
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # No equivalent
# 
# ```
# 
# 
# ````

# <p align="center">  Vectorised ifelse statements </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > x <- 1:10
# 
# > fcase(
#     x %% 6 == 0, "fizz buzz",
#     x %% 2 == 0, "fizz",
#     x %% 3 == 0, "buzz",
#     default = NA_character_
#   )
# 
#  [1] NA          "fizz"      "buzz"      "fizz"      NA          "fizz buzz"
#  [7] NA          "fizz"      "buzz"      "fizz" 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# from datatable import ifelse
# 
# DF = dt.Frame({"x" : range(1, 11)})
# 
# DF[:, ifelse(f.x % 6 == 0, "fizz buzz", 
#              f.x % 2 == 0, "fizz", 
#              f.x % 3 == 0, "buzz", 
#              None)]
# 
# 
#    | C0       
#    | str32    
# -- + ---------
#  0 | NA       
#  1 | fizz     
#  2 | buzz     
#  3 | fizz     
#  4 | NA       
#  5 | fizz buzz
#  6 | NA       
#  7 | fizz     
#  8 | buzz     
#  9 | fizz     
# [10 rows x 1 column]
# 
# 
# ```
# 
# 
# ````

# ## **Join/Bind Data Sets**

# ### Join

# ```{note}
# Unlike R's [data.table](https://rdatatable.gitlab.io/data.table/), which supports all join forms, including non-equi joins, python's [datatable](https://datatable.readthedocs.io/en/latest/) only supports the natural join (left-join). It also has some limitations:
# 1. There should be no duplicates in the frame on the right of the join. 
# 2. The joining columns in both frames should have the same name; 
# 3. The joining column on the right frame has to be keyed.
# 
# ```

# ### Bind

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# > x <- data.table(1:3)
# 
# > x
#    V1
# 1:  1
# 2:  2
# 3:  3
# 
# > y <- data.table(4:6)
# 
# > y
#    V1
# 1:  4
# 2:  5
# 3:  6
# 
# > z <- data.table(7:9, 0L)
# 
# > z
#    V1 V2
# 1:  7  0
# 2:  8  0
# 3:  9  0
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# x = dt.Frame({"V1" : [1, 2, 3]})
# 
# x
# 
#    |    V1
#    | int32
# -- + -----
#  0 |     1
#  1 |     2
#  2 |     3
# [3 rows x 1 column]
# 
# y = dt.Frame({"V1" : [4, 5, 6]})
# 
# y
#  
#    |    V1
#    | int32
# -- + -----
#  0 |     4
#  1 |     5
#  2 |     6
# [3 rows x 1 column]
# 
# z = dt.Frame({"V1" : [7, 8, 9], "V2" : [0, 0, 0]})
# 
# z
# 
#    |    V1    V2
#    | int32  int8
# -- + -----  ----
#  0 |     7     0
#  1 |     8     0
#  2 |     9     0
# [3 rows x 2 columns]
# 
# ```
# 
# 
# ````

# <p align="center"> Bind Rows </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# > rbind(x, y)
# 
#    V1
# 1:  1
# 2:  2
# 3:  3
# 4:  4
# 5:  5
# 6:  6
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# dt.rbind(x, y)
#  
#    |    V1
#    | int32
# -- + -----
#  0 |     1
#  1 |     2
#  2 |     3
#  3 |     4
#  4 |     5
#  5 |     6
# [6 rows x 1 column]
# 
# ```
# 
# 
# ````

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# 
# ```R
# 
# > rbind(x, z, fill = TRUE)
# 
#    V1 V2
# 1:  1 NA
# 2:  2 NA
# 3:  3 NA
# 4:  7  0
# 5:  8  0
# 6:  9  0
# 
# 
# 
# ```
# ---
# 
# 
# ```python
# 
# dt.rbind(x, z, force = True)
#  
#    |    V1    V2
#    | int32  int8
# -- + -----  ----
#  0 |     1    NA
#  1 |     2    NA
#  2 |     3    NA
#  3 |     7     0
#  4 |     8     0
#  5 |     9     0
# [6 rows x 2 columns]
# 
# ```
# 
# 
# ````

# <p align="center">  Bind Rows using a List </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# > rbindlist(list(x, y), idcol = TRUE)
# 
#    .id V1
# 1:   1  1
# 2:   1  2
# 3:   1  3
# 4:   2  4
# 5:   2  5
# 6:   2  6
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # No equivalent
# 
# ```
# 
# 
# ````

# <p align="center">  Bind Columns </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# > base::cbind(x, y)
# 
#    V1 V1
# 1:  1  4
# 2:  2  5
# 3:  3  6
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# dt.cbind(x, y)
# DatatableWarning: Duplicate column name found, 
# and was assigned a unique name: 'V1' -> 'V2'
#  
#    |    V1     V2
#    | int32  int32
# -- + -----  -----
#  0 |     1      4
#  1 |     2      5
#  2 |     3      6
# [3 rows x 2 columns]
# 
# ```
# 
# 
# ````

# ### Set Operations

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# > x <- data.table(c(1, 2, 2, 3, 3))
# 
# > x
# 
#    V1
# 1:  1
# 2:  2
# 3:  2
# 4:  3
# 5:  3
# 
# > y <- data.table(c(2, 2, 3, 4, 4))
# 
# > y
# 
#    V1
# 1:  2
# 2:  2
# 3:  3
# 4:  4
# 5:  4
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# x = dt.Frame((1, 2, 2, 3, 3))
# 
# x
#  
#    |    C0
#    | int32
# -- + -----
#  0 |     1
#  1 |     2
#  2 |     2
#  3 |     3
#  4 |     3
# [5 rows x 1 column]
# 
# y = dt.Frame((2, 2, 3, 4, 4))
# 
# y
#  
#    |    C0
#    | int32
# -- + -----
#  0 |     2
#  1 |     2
#  2 |     3
#  3 |     4
#  4 |     4
# [5 rows x 1 column]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Intersection </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > fintersect(x, y)
# 
#    V1
# 1:  2
# 2:  3
# 
# > fintersect(x, y, all = TRUE)
# 
#    V1
# 1:  2
# 2:  2
# 3:  3
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# dt.intersect(x, y)
# 
#    |    C0
#    | int32
# -- + -----
#  0 |     2
#  1 |     3
# [2 rows x 1 column]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Difference </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > fsetdiff(x, y)
# 
#    V1
# 1:  1
# 
# > fsetdiff(x, y, all = TRUE)
# 
#    V1
# 1:  1
# 2:  3
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# dt.setdiff(x, y)
#  
#    |    C0
#    | int32
# -- + -----
#  0 |     1
# [1 row x 1 column]
# 
# ```
# 
# 
# ````

# <p align="center">  Union </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > funion(x, y)
# 
#    V1
# 1:  1
# 2:  2
# 3:  3
# 4:  4
# 
# > funion(x, y, all = TRUE)
# 
#     V1
#  1:  1
#  2:  2
#  3:  2
#  4:  3
#  5:  3
#  6:  2
#  7:  2
#  8:  3
#  9:  4
# 10:  4
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# dt.union(x, y)
#  
#    |    C0
#    | int32
# -- + -----
#  0 |     1
#  1 |     2
#  2 |     3
#  3 |     4
# [4 rows x 1 column]
# 
# 
# ```
# 
# 
# ````

# <p align="center">  Equality </p>

# ````{panels}
# :header: text-center
# :card: border-0
# 
# ---
# **data.table**
# ^^^
# 
# ```R
# 
# > fsetequal(x, x[order(-V1),])
# [1] TRUE
# 
# > all.equal(x, x) # S3 method
# [1] TRUE
# 
# 
# 
# ```
# ---
# 
# **datatable**
# ^^^
# 
# ```python
# 
# # no equivalent
# 
# ```
# 
# 
# ````

# Resources: 
# 
# - [datatable docs](https://datatable.readthedocs.io/en/latest/)
# - atrebas' [data.table vs pandas](https://atrebas.github.io/post/2020-06-14-datatable-pandas/) blog post
# - Based on datatable version ``1.0.0a0+build.1615412817``
