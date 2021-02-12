# "Data Wrangling with Python Datatable - Select Columns by Data Type"
> "Column Selection"

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
- metadata_key1: "python datatable"
- metadata_key2: "python"

#### [Link to Source data](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.select_dtypes.html)

from datatable import dt, f

df = dt.Frame({'a': [1, 2, 1, 2, 1, 2],
 'b': [True, False, True, False, True, False],
 'c': [1.0, 2.0, 1.0, 2.0, 1.0, 2.0]}
)

df

- Select the boolean column

df[:, f[bool]]

- Select the float column

df[:, f[float]]

- Exclude integer column

df[:, [dtype.name != "int" for dtype in df.ltypes]]

Resources: 
- [ltype](https://datatable.readthedocs.io/en/latest/api/ltype.html#)

- [stypes](https://datatable.readthedocs.io/en/latest/api/ltype/stypes.html#)

