import numpy as np
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)

df = pd.read_csv('flats.csv')
df.sample(5)

print(df.shape)
print(df.info())

df.duplicated().sum()

df.isnull().sum()

df.drop(columns=['link'], inplace=True)
df.info()

df.rename(columns={'area':'price_per_sqft'}, inplace= True)

# value counts for categorical columns 
df['society'].value_counts()

df['society'].value_counts().shape

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