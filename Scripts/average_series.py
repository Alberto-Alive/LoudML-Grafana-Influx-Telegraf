import pandas as pd
from os import path
import matplotlib.pyplot as plt
import numpy as np

import os, psutil
process = psutil.Process(os.getpid())
print(process.memory_info().rss)  # in bytes
columns=['column_1', 'column_2'] #List column names of your cleaned csv-file data

data_path = path.join('data', 'cleaned-last_test_alberto.csv') #Get the csv-file
df = pd.read_csv(data_path, delimiter=',', index_col=0) #Read a comma-separated values (csv) file into DataFrame.

# Get rid of columns that are flat i.e. time series where values are all 1's for example.
for col in df.columns[:-1]: #Iterate cols except time col.
    if col in columns and df[col].sum()/df.shape[0] <1:
        columns.remove(col)

df = df[columns]
df_rolling = df.rolling(50, min_periods=1, center=True).mean()
df_rolling['average'] = df_rolling.mean(numeric_only=True, axis=1)  #Calculate moving average of timeseries.

df_rolling['errors']=[0]*df.shape[0]  #Initialise error rows with zeros.
small=0.0001  #Avoid division by 0.
for col in df_rolling.columns[:-1]:  #Iterate cols except time col.
    relative_distance=np.abs((df_rolling[col]- df_rolling['average'])/(df_rolling['average'] + small))  #Calculate the relative distance fom th mean
    df_rolling['errors'] = (df_rolling['errors']) | (relative_distance>0.25).astype('int')  #Add the error to the table. Fine-tune the number relative_distance is relative to.


df_rolling.plot(logy=False)
plt.show()