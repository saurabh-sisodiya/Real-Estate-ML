import numpy as np
import pandas as pd

'''
What is data preprocessing?
It is the process of preparing data for analysis and machine learning. It involves cleaning,
tranforming and reducing data to make it usable. 

Why is data preprocessing important?
Data preprocessing is important because it ensures that data is accurate, consistent and ready for analysis.
- Improves data quality
- Prepares data for analysis
- Prevents inaccurate results

What if I do not do preprocessing?
Without preprocessing, analysis and machine learning models could produce inaccurate results.
A machine learning model's performance is directly affected by data quality.

How to do data preprocessing?
- Data cleaning - Removes errors, duplicates, and inconsistencies
- Data Integration - Combines data from multiple sources and resolves inconsistencies
- Data Transformation - Normalizes and scales data, encodes categorical variables, and aggregates information.
- Data reduction - Compresses the data while preserving its meaning
'''

# set_option -> sets the value of the specified option, if max_rows exceeded, switch to truncate view. 
# if the max_columns exceeded, switch to truncate view
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)


# read the comma sepearated values file into dataFrame
df = pd.read_csv('flats.csv')

# returns the random sample of items (axis= 0 = rows, axis =1 = columns)
df.sample(5)

# returns the shape of DataFrame(df)
print(df.shape)

# returns the information about the dataframe
'''
What type of information it returns?
It returns the essential details such as total number of non-null values, data types of each column, and memory usage.
This summary is beneficial for quickly assessing the completeness the overall data types present in the DataFrame.
'''
print(df.info())


# returns the sum of duplicated rows
df.duplicated().sum()

# returns the sum of null values
df.isnull().sum()

# drops the columns from df, and inplace=True is used for permanent changes
df.drop(columns=['link'], inplace=True)
df.info()

# for renaming the columns
df.rename(columns={'area':'price_per_sqft'}, inplace= True)

# value counts for categorical columns - returns a series containing the counts of unique values 
df['society'].value_counts()

df['society'].value_counts().shape

# re - regenerate expression 

import re
df['society'] = df['society'].apply(lambda name: re.sub(r'\d+(\.\d+)?\s?★','',str(name)).strip()).str.lower()

df['society'].value_counts().shape

print(df['price'].value_counts())

df[df['price'] == 'Price on Request']

df = df[df['price'] != 'Price on Request']
df.head()
print('yaha tak sahi hai')
def treat_price(x):
    if type(x) == float:
        return x
    
    parts = x.split(" ")
    if len(parts) < 2:
        return None

    if parts[1] == 'Lac':
        return round(float(x[0])/100,2)
    elif parts[1] == 'Crore':
        return round(float(x[0]),2)
    else:
        return None
        
df['price'] = df['price'].apply(treat_price)

df['price'].value_counts()

print(df['price_per_sqft'].value_counts())
df= df[df['price_per_sqft'] != 'area']
df['price_per_sqft'] = df['price_per_sqft'].str.split('/').str.get(0).str.replace('₹','').str.replace(',','').str.strip().astype('float')
print(df.head())