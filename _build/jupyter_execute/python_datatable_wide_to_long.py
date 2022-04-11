#!/usr/bin/env python
# coding: utf-8

# # Reshaping Data From Wide to Long Form

# This article highlights various ways to reshape data from wide to long form in python [datatable](https://datatable.readthedocs.io/en/latest/).

# ## **Selecting Columns**

# ### The Basics

# In[1]:


from datatable import dt, f, Type
from typing import Pattern, NamedTuple, Union
from collections import Counter, defaultdict
from itertools import compress, chain
import re
import numpy as np
import pandas as pd


# In[2]:


from datatable import dt, f
from typing import Pattern, NamedTuple, Union
from collections import Counter, defaultdict
from itertools import compress, chain
import re
import numpy as np

class measure(NamedTuple):
    """tuple for more complex reshape."""
    column_names:Union[str, list]
    sep:Union[str, Pattern] = None
    pattern:Union[str, Pattern] = None

def melt(data, id_vars=None, measure_vars=None, variable_name = 'variable', value_name = 'value'):
    "Turns Frame from wide to long form."
    if id_vars:
        if not isinstance(id_vars, (str, list, tuple)):
            raise TypeError('id_vars should be one of str, list, tuple.')
        if isinstance(id_vars, str):
            id_vars = [id_vars]
        checks = set(id_vars).difference(data.names)
        if checks:
            raise ValueError(f'Labels {checks} in id_vars do not exist in the column names.')
        if not set(data.names).difference(id_vars):
            return data
        checks = [key for key,value in Counter(id_vars).items() if value > 1]
        if checks:
            raise ValueError(f"Labels {checks} are duplicated in id_vars.")
        if not measure_vars:
            measure_vars = [name for name in data.names if name not in id_vars]
    if measure_vars:
        if not isinstance(measure_vars, (str, list, tuple)):
            raise TypeError('measure_vars should be one of str, list, tuple.')
        if isinstance(measure_vars, str):
            measure_vars = [measure_vars]
        checks = set(measure_vars).difference(data.names)
        if checks:
            raise ValueError(f'Labels {checks} in measure_vars do not exist in the column names.')
        checks = [key for key,value in Counter(measure_vars).items() if value > 1]
        if checks:
            raise ValueError(f"Labels {checks} are duplicated in measure_vars.")
        if (not id_vars) and (len(measure_vars) < data.ncols):
            id_vars = [name for name in data.names if name not in measure_vars]
    else:
        measure_vars = data.names

    def reshape_no_dot(measure_vars, output, data, id_vars=None):
        values = []
        for frame in data[:, measure_vars]:
            frame.names = [value_name]
            values.append(frame)
        values = dt.rbind(values, force=True)
        if id_vars:
            id_vars = dt.repeat(data[:, id_vars], len(measure_vars))
            return dt.cbind([id_vars, output, values], force = True)
        return dt.cbind([output, values], force = True)

    def reshape_dot(column_names, data, measure_vars, output, id_vars=None):
        "reshape if '.value' is present in the column names."
        boolean = [True if ent == '.value' else False for ent in column_names]
        dot_value = [[*compress(extract, boolean)] for extract in output]
        if len(dot_value[0]) > 1:
            dot_value = ["".join(extract) for extract in dot_value]
        else:
            dot_value = [*chain.from_iterable(dot_value)]
        checks = set(dot_value)
        if id_vars and checks.intersection(id_vars):
            raise ValueError(
                f"The new column names associated with .value -> {checks} "
                "are duplicated in id_vars."
            )
        boolean = [not true for true in boolean]
        others = [tuple(compress(extract, boolean)) for extract in output]
        headers_for_others = [extract for extract in column_names if extract != '.value']
        measure_vars = [frame for frame in data[:, measure_vars]]
        out = defaultdict(list)
        for key, value_column, frame in zip(others, dot_value, measure_vars):
            frame.names = [value_column]
            out[key].append(frame)
        headers_for_others = [dt.Frame([key], names = headers_for_others) for key, _ in out.items()]
        out = [dt.cbind(frame, force = True) for _, frame in out.items()]
        out = [dt.cbind(dt.repeat(left, right.nrows), right, force = True) for left, right in zip(headers_for_others, out)]
        out = dt.rbind(out, force = True)
        if id_vars:
            id_vars = dt.repeat(data[:, id_vars], out.nrows//data.nrows)
            return dt.cbind([id_vars, out], force = True)
        return out

    if not isinstance(variable_name, (str, tuple, dict, Pattern)):
        raise TypeError('variable_name should be one of string, tuple, dictionary, regular expression.')

    if isinstance(variable_name, str):
        if not isinstance(value_name, str):
            raise TypeError('value_name should be a string.')
        if value_name == variable_name:
            raise ValueError(
                f"{value_name} is duplicated as variable_name. "
                f"Kindly provide a unique argument for {value_name}.")
        if id_vars: 
            if variable_name in id_vars:
                raise ValueError(
                    f"{variable_name} already exists as a label "
                    "in id_vars. Kindly provide a unique argument.")
            if value_name in id_vars:
                raise ValueError(
                    f"{value_name} already exists as a label "
                    "in id_vars. Kindly provide a unique argument.")

        output = dt.Frame({variable_name:measure_vars})
        output = output[np.repeat(range(output.nrows), data.nrows),:]
        return reshape_no_dot(measure_vars=measure_vars, output = output, data = data, id_vars = id_vars)


    if isinstance(variable_name, Pattern):
        if not re.compile(variable_name).groups:
            raise ValueError("The regex should have at least one group.")
        output = [re.search(variable_name, word) for word in measure_vars]
        no_matches = [word for word, match in zip(measure_vars, output) if not match]
        if no_matches:
            raise ValueError(
                f"There was no match for labels {no_matches} "
                "for the provided regular expression.")
        output = [entry.groupdict() for entry in output]
        checks = output[0].keys()
        if id_vars and set(checks).intersection(id_vars):
            raise ValueError(
                f"Labels {checks} already exist in id_vars. "
                "Kindly provide unique names for the named groups " 
                "in the regular expression."
                )
        output = dt.Frame(output)
        output = output[np.repeat(range(output.nrows), data.nrows),:]        
        return reshape_no_dot(measure_vars=measure_vars, output = output, data = data, id_vars = id_vars)

    if isinstance(variable_name, dict) :
        checks = set(variable_name).intersection(id_vars)
        if id_vars and checks:
            raise ValueError(
                f"Labels {checks} already exist in id_vars. "
                "Kindly provide keys for the dictionary "
                "that do not exist in id_vars."
                )
        for key, regex in variable_name.items():
            if not isinstance(key, str):
                raise TypeError(f"{key} should be a string.")
            if not isinstance(regex, (str, Pattern)):
                raise TypeError(
                    f"The value for {key} should be a regular expression, "
                    "or can be compiled into one."
                    )
            if re.compile(regex).groups:
                raise ValueError("The regex should not have any groups.")
        output = []
        for key, regex in variable_name.items():
            out = [word for word in measure_vars if re.search(regex, word)]
            if not out:
                raise ValueError(
                    f"There was no match for {key} for regex => {regex}"
                )            
            
            measure_vars = [word for word in measure_vars if word not in out]
            if len(out) == 1:
                frame.names = [key]
                output.append(frame)
            else:
                values = []
                for frame in data[:, out]:
                    frame.names = [key]
                    values.append(frame)
                output.append(dt.rbind(values, force = True))
        output = dt.cbind(output, force=True)
        if id_vars:
            id_vars = dt.repeat(data[:, id_vars], output.nrows//data.nrows)
            return dt.cbind([id_vars, output])
        return output
          
    if isinstance(variable_name, tuple):
        variable_name = measure(*variable_name)
        column_names, sep, pattern = variable_name
        if not column_names:
            raise ValueError("Kindly provide argument for column_names, in the variable_name tuple.")
        if not isinstance(column_names, (str, list)):
            raise TypeError('column_names should be one of string, list.')
        if isinstance(column_names, str):
            column_names = [column_names]
        if id_vars:
            checks = set(column_names)
            checks.discard(".value")
            checks = checks.intersection(id_vars)
            if checks:
                raise ValueError(
                    f"Labels {checks} already exist in id_vars. "
                    "Kindly provide unique column_names "
                    "that do not exist in id_vars."
                    )
        if not any((sep, pattern)):
            raise ValueError("Kindly provide one of sep or pattern.")
        if sep and pattern:
            raise ValueError("only one of sep or pattern should be provided.")
        if sep:
            if not isinstance(sep, (str, Pattern)):
                raise TypeError(
                    "sep should be a regular expression, "
                    "or can be compiled into one.")
            output = [re.split(sep, word) for word in measure_vars]
            checks = max(map(len, output))
            if len(column_names) != checks:
                raise ValueError(
                    f"The maximum number of splits for sep -> {sep} is {checks} "
                    f"while the number of labels in {column_names} "
                    f"is {len(column_names)}"
                )
            if '.value' not in column_names:
                output = [*map(tuple, output)]
                output = dt.Frame(output, names=column_names)
                output = output[np.repeat(range(output.nrows), data.nrows),:]        
                return reshape_no_dot(measure_vars=measure_vars, output = output, data = data, id_vars = id_vars)

            return reshape_dot(column_names, data, measure_vars, output, id_vars=id_vars)

        if pattern:
            if not isinstance(pattern, (str, Pattern)):
                raise TypeError(
                    "pattern should be a regular expression, "
                    "or can be compiled into one.")
            checks = re.compile(pattern).groups
            if not checks:
                raise ValueError("The regex should have at least one group.")
            if checks != len(column_names):
                raise ValueError(
                    "The number of groups in the regex "
                    "should match the number of labels in column_names. "
                    f"The number of groups in the regex is {len(checks)}, "
                    f"while the length of column_names is {len(column_names)}")
            output = [re.findall(pattern, word) for word in measure_vars]
            no_matches = [word for word, match in zip(measure_vars, output) if not match]
            if no_matches:
                raise ValueError(
                    f"There was no match for labels {no_matches} "
                    "for the provided regular expression.")
            output = [*chain.from_iterable(output)]
            if '.value' not in column_names:
                output = [*map(tuple, output)]
                output = dt.Frame(output, names=column_names)
                output = output[np.repeat(range(output.nrows), data.nrows),:]        
                return reshape_no_dot(measure_vars=measure_vars, output = output, data = data, id_vars = id_vars)

            return reshape_dot(column_names, data, measure_vars, output, id_vars=id_vars)


# In[3]:


DT = dt.Frame(
            [
                {
                    "ID": 1,
                    "DateRange1Start": "1/1/90",
                    "DateRange1End": "3/1/90",
                    "Value1": 4.4,
                    "DateRange2Start": "4/5/91",
                    "DateRange2End": "6/7/91",
                    "Value2": 6.2,
                    "DateRange3Start": "5/5/95",
                    "DateRange3End": "6/6/96",
                    "Value3": 3.3,
                }
            ])

DT


# In[4]:


melt(DT, id_vars='ID', variable_name= (['.value', 'num', '.value'], None, '(.+)(\d)(.*)'))


# In[5]:


DT = dt.Frame(
        {
            "id": [1, 2, 3],
            "M_start_date_1": [201709, 201709, 201709],
            "M_end_date_1": [201905, 201905, 201905],
            "M_start_date_2": [202004, 202004, 202004],
            "M_end_date_2": [202005, 202005, 202005],
            "F_start_date_1": [201803, 201803, 201803],
            "F_end_date_1": [201904, 201904, 201904],
            "F_start_date_2": [201912, 201912, 201912],
            "F_end_date_2": [202007, 202007, 202007],
        }
    )

DT


# In[6]:


melt(DT, id_vars='id', variable_name=(["cod", ".value", "date", "num"], None, "(M|F)_(start|end)_(date)_(.+)"))


# In[7]:


DT = dt.Frame(
    {
        "off_loc": ["A", "B", "C", "D", "E", "F"],
        "pt_loc": ["G", "H", "I", "J", "K", "L"],
        "pt_lat": [
            100.07548220000001,
            75.191326,
            122.65134479999999,
            124.13553329999999,
            124.13553329999999,
            124.01028909999998,
        ],
        "off_lat": [
            121.271083,
            75.93845266,
            135.043791,
            134.51128400000002,
            134.484374,
            137.962195,
        ],
        "pt_long": [
            4.472089953,
            -144.387785,
            -40.45611048,
            -46.07156181,
            -46.07156181,
            -46.01594293,
        ],
        "off_long": [
            -7.188632000000001,
            -143.2288569,
            21.242563,
            40.937416999999996,
            40.78472,
            22.905889000000002,
        ],
    }
)

DT


# In[8]:


melt(DT, variable_name=(['set', '.value'], None, r"(.+)_(.+)"))


# In[9]:


DT = dt.Frame({'Location': ['Madrid', 'Madrid', 'Rome', 'Rome'],
 'Account': ['ABC', 'XYX', 'ABC', 'XYX'],
 'Y2019:MTD:January:Expense': [4354, 769867, 434654, 632556456],
 'Y2019:MTD:January:Income': [56456, 32556456, 5214, 46724423],
 'Y2019:MTD:February:Expense': [235423, 6785423, 235423, 46588]})

DT


# In[10]:


melt(DT, id_vars=['Location', 'Account'], variable_name=(['year','month', '.value'], None, r"Y(.+):MTD:(.{3}).+(Income|Expense)"))


# In[11]:


DT


# In[12]:


DT = dt.Frame(
            {
                "country": ["United States", "Russia", "China"],
                "vault_2012_f": [
                    48.132,
                    46.366,
                    44.266,
                ],
                "vault_2012_m": [46.632, 46.866, 48.316],
                "vault_2016_f": [
                    46.866,
                    45.733,
                    44.332,
                ],
                "vault_2016_m": [45.865, 46.033, 45.0],
                "floor_2012_f": [45.366, 41.599, 40.833],
                "floor_2012_m": [45.266, 45.308, 45.133],
                "floor_2016_f": [45.999, 42.032, 42.066],
                "floor_2016_m": [43.757, 44.766, 43.799],
            }
        )

DT


# In[13]:


melt(DT, id_vars='country', variable_name=(['event', 'year', 'gender'], '_'))


# In[14]:


measure(['event','country'], None, '_')


# In[15]:


DT = dt.Frame({'id': [0, 1],
 'Name': ['ABC', 'XYZ'],
 'code': [1, 2],
 'code1': [4, np.nan],
 'code2': [8, 5],
 'type': ['S', 'R'],
 'type1': ['E', np.nan],
 'type2': ['T', 'U']})


DT


# In[16]:


melt(DT, id_vars = ['id', 'Name'], variable_name={'code_all':'^code', 'type_all':'^type'})


# In[17]:


DT = dt.Frame(
            [
                {
                    "ID": 1,
                    "DateRange1Start": "1/1/90",
                    "DateRange1End": "3/1/90",
                    "Value1": 4.4,
                    "DateRange2Start": "4/5/91",
                    "DateRange2End": "6/7/91",
                    "Value2": 6.2,
                    "DateRange3Start": "5/5/95",
                    "DateRange3End": "6/6/96",
                    "Value3": 3.3,
                }
            ])

DT


# In[18]:


melt(DT, id_vars='ID', variable_name={"DateRangeStart":"Start$", 'DateRangeEnd':'End$', 'Value':'^Value'})


# In[19]:


DT = dt.Frame(
            {
                "country": ["United States", "Russia", "China"],
                "vault_2012_f": [
                    48.132,
                    46.366,
                    44.266,
                ],
                "vault_2012_m": [46.632, 46.866, 48.316],
                "vault_2016_f": [
                    46.866,
                    45.733,
                    44.332,
                ],
                "vault_2016_m": [45.865, 46.033, 45.0],
                "floor_2012_f": [45.366, 41.599, 40.833],
                "floor_2012_m": [45.266, 45.308, 45.133],
                "floor_2016_f": [45.999, 42.032, 42.066],
                "floor_2016_m": [43.757, 44.766, 43.799],
            }
        )

DT


# In[20]:


pat = r"(?P<event>[a-z]+)_(?P<year>\d+)_(?P<gender>.+)"
out = melt(DT, id_vars='country', variable_name=re.compile(pat))
out
#dt.Frame(out)


# In[21]:


DT = dt.Frame({'subject': [1, 2],
                   'A_target_word_gd': [1, 11],
                   'A_target_word_fd': [2, 12],
                   'B_target_word_gd': [3, 13],
                   'B_target_word_fd': [4, 14],
                   'subject_type': ['mild', 'moderate']})


DT


# In[22]:


pat = "(?P<cond>[A-Z]).*(?P<value_type>gd|fd)"
melt(DT, id_vars=["subject", "subject_type"], variable_name=re.compile(pat))


# In[23]:


DT = dt.Frame({
    'famid': [1, 1, 1, 2, 2, 2, 3, 3, 3],
    'birth': [1, 2, 3, 1, 2, 3, 1, 2, 3],
    'ht1': [2.8, 2.9, 2.2, 2, 1.8, 1.9, 2.2, 2.3, 2.1],
    'ht2': [3.4, 3.8, 2.9, 3.2, 2.8, 2.4, 3.3, 3.4, 2.9]
})

DT


# In[24]:


DT = dt.repeat(DT, 10_000)
DT


# In[25]:


melt(DT, id_vars = ['famid', 'birth'], variable_name=(['.value', 'age'], None, r"(.+)(.)"))


# In[26]:


DT = dt.Frame([(1,1,2,3,4,5,6), (2,7,8,9,10,11,12)],
                  names=['id', 'ax','ay','az','bx','by','bz'])


DT


# In[27]:


melt(DT, id_vars='id', variable_name=(['name', '.value'], None, '(.)(.)'))


# In[28]:


DT = dt.Frame([{'id': 1, 'A1g_hi': 2, 
                    'A2g_hi': 3, 'A3g_hi': 4, 
                    'A4g_hi': 5}])

DT


# In[29]:


melt(DT, id_vars='id', variable_name=(['time', '.value'], None, "A(.)g_(.+)"))


# In[30]:


DT = dt.Frame(
    [{'Sony | TV | Model | value': 'A222',
  'Sony | TV | Quantity | value': 5,
  'Sony | TV | Max-quant | value': 10,
  'Panasonic | TV | Model | value': 'T232',
  'Panasonic | TV | Quantity | value': 1,
  'Panasonic | TV | Max-quant | value': 10,
  'Sanyo | Radio | Model | value': 'S111',
  'Sanyo | Radio | Quantity | value': 4,
  'Sanyo | Radio | Max-quant | value': 9},
 {'Sony | TV | Model | value': 'A234',
  'Sony | TV | Quantity | value': 5,
  'Sony | TV | Max-quant | value': 9,
  'Panasonic | TV | Model | value': 'S3424',
  'Panasonic | TV | Quantity | value': 5,
  'Panasonic | TV | Max-quant | value': 12,
  'Sanyo | Radio | Model | value': 'S1s1',
  'Sanyo | Radio | Quantity | value': 2,
  'Sanyo | Radio | Max-quant | value': 9},
 {'Sony | TV | Model | value': 'A4345',
  'Sony | TV | Quantity | value': 4,
  'Sony | TV | Max-quant | value': 9,
  'Panasonic | TV | Model | value': 'X3421',
  'Panasonic | TV | Quantity | value': 1,
  'Panasonic | TV | Max-quant | value': 11,
  'Sanyo | Radio | Model | value': 'S1s2',
  'Sanyo | Radio | Quantity | value': 4,
  'Sanyo | Radio | Max-quant | value': 10}]
)

DT


# In[31]:


melt(DT, variable_name=(["Manufacturer", "Device", ".value"], None, r"(.+)\|(.+)\|(.+)\|.*"))


# In[32]:


DT = dt.Frame({'first': ['John', 'Mary'],
                   'last': ['Doe', 'Bo'],
                   'height': [5.5, 6.0],
                   'weight': [130, 150]})
DT


# In[33]:


melt(DT)


# In[34]:


melt(DT).stypes


# In[35]:


melt(DT, id_vars=['first', 'last'])


# In[36]:


url = 'https://raw.githubusercontent.com/tidyverse/tidyr/main/data-raw/billboard.csv'
DT = dt.fread(url)
measure_vars = [name for name in DT.names if name.startswith('wk')]
melt(DT, measure_vars=measure_vars, variable_name='week')


# In[37]:


DT = dt.Frame([{'A': 'a', 'B': 1, 'C': 2},
 {'A': 'b', 'B': 3, 'C': 4},
 {'A': 'c', 'B': 5, 'C': 6}])

DT


# In[38]:


melt(DT, id_vars='A', measure_vars='B')


# In[39]:


melt(DT, id_vars='A', measure_vars=['B', 'C'])


# In[40]:


melt(DT, id_vars='A', measure_vars='B', variable_name='myVarname', value_name='myValname')


# In[41]:


DT = dt.Frame({'Name': ['Bob', 'John', 'Foo', 'Bar', 'Alex', 'Tom'], 
                   'Math': ['A+', 'B', 'A', 'F', 'D', 'C'], 
                   'English': ['C', 'B', 'B', 'A+', 'F', 'A'],
                   'Age': [13, 16, 16, 15, 15, 13]})

DT


# In[42]:


melt(DT, id_vars = ['Name', 'Age'], measure_vars=['Math', 'English'], variable_name='Subject', value_name='Grade')


# In[43]:


DT = dt.Frame({
        'asset1':list('acacac'),
         'asset2':[4]*6,
         'A':[7,8,9,4,2,3],
         'D':[1,3,5,7,1,0],
         'E':[5,3,6,9,2,4]
})

DT


# In[44]:


melt(DT, id_vars=['asset1', 'asset2'], measure_vars = ['A', 'D'], variable_name='c_name', value_name='Value')


# In[45]:


DT = dt.Frame({'New York': [25]})

DT


# In[46]:


melt(DT)


# In[47]:


DT = dt.Frame({'New york': [25], 'Paris': [27], 'London': [30]})

melt(DT)


# In[48]:


temperatures = dt.Frame({
    'city': ['New York', 'London', 'Paris', 'Berlin', 'Amsterdam'],
    'day1': [23, 25, 27, 26, 24],
    'day2': [22, 21, 25, 26, 23],
    'day3': [26, 25, 24, 27, 23],
    'day4': [23, 21, 22, 26, 27],
    'day5': [27, 26, 27, 24, 28]
})

melt(temperatures, id_vars = 'city')


# In[49]:


melt(temperatures)


# In[50]:


DT = dt.Frame(
            {
                "country": ["United States", "Russia", "China"],
                "vault_2012_f": [
                    48.132,
                    46.366,
                    44.266,
                ],
                "vault_2012_m": [46.632, 46.866, 48.316],
                "vault_2016_f": [
                    46.866,
                    45.733,
                    44.332,
                ],
                "vault_2016_m": [45.865, 46.033, 45.0],
                "floor_2012_f": [45.366, 41.599, 40.833],
                "floor_2012_m": [45.266, 45.308, 45.133],
                "floor_2016_f": [45.999, 42.032, 42.066],
                "floor_2016_m": [43.757, 44.766, 43.799],
            }
        )

DT

