# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 08:47:17 2024

"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import nan
from seaborn import scatterplot
from matplotlib.pyplot import subplots
from seaborn import swarmplot
from seaborn import pairplot
from seaborn import heatmap

#%% 

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#%% 
# Read the file and read the first and last five rows

df = pd.read_csv(r"exoplanets.csv")
print(df.head())

#%%

print(df.tail())

#%%
#show first row:

row_1 = df.iloc[0]
print(row_1)

#%%

#information about the DataFrame

df.info()

#%%
#Clean Data: Remove unnecessary values .Remove duplicate data .
#Fix structural errors .

def clean_distance(arg):
    if not isinstance(arg, str):
        return arg
    arg = arg.replace(',', '').replace('~', '')
    if '±' in arg:
        pieces = arg.split('±')
        if pieces[0] != '':
            return float(pieces[0])
        else:
            return float(pieces[1])
    if '+' in arg:
        return float(arg.split('+')[0])
    else:
        return float(arg)

def clean_mass(arg):
    if not isinstance(arg, str):
        return arg
    arg = arg.replace('~', '').replace('{', '').replace(',', '')
    if arg in {'10-May', 'Imaged near Alpha Centauri A'}:
        return nan
    if 'E' in arg:
        return float(arg)
    if '+' in arg:
        return float(arg.split('+')[0])
    if '-' in arg:
        return float(arg.split('-')[0])
    if '±' in arg:
        pieces = arg.split('±')
        if pieces[0] != '':
            return float(pieces[0])
        else:
            return float(pieces[1])
    if '[' in arg:
        return float(arg.split('[')[0])
    if '<' in arg:
        return float(arg.replace('<', ''))
    if '>' in arg:
        return float(arg.split('>')[1])
    if '/' in arg:
        return float(arg.split('/')[0])
    return float(arg)

distance = 'Distance (ly)'
mass = 'Mass (MJ)'
distance_clean = 'distance (clean)'
mass_clean = 'mass (clean)' 
df[distance_clean] = df[distance].apply(func=clean_distance)

df[mass_clean] = df[mass].apply(func=clean_mass)


#%%
#The number of planets discovered in different years

sns.histplot(data=df, x="Disc. Year" , hue="Discovery method",
             binwidth=1.4).set(title='Number of discovered per years with different methods')

plt.show()

#%%
# nummer pro jahr

sns.displot(data=df, x="Disc. Year", kde=True,legend=True ,
            palette="pastel").set(title='Number of discovered per years')
plt.show()

#%%
# how were they discovered?

method = 'Discovery method'
categories = ['transit', 'microlensing', 'timing', "radial vel.",
              "imaging","astrometry","orbital brightness modulation"]

x = df['Discovery method'].value_counts()
print(x)
percent = 100.*x/x.sum()
labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(categories, percent)]
patches, texts = plt.pie(x, radius=1.2 ,startangle=90)


sort_legend = True
if sort_legend:
    patches, labels, dummy =  zip(*sorted(zip(patches, labels, x),
                                          key=lambda x: x[2],
                                          reverse=True))

plt.legend(patches, labels, loc='lower left',
           fontsize=6)
plt.tight_layout()
plt.title('Percentage of discovery methods')
plt.show()


#%%

#A scatterplot categorized by year


_, ax = subplots(figsize=(14, 8))
swarmplot(data=df, x="Disc. Year", ax=ax ,legend=True ,hue=method)
plt.title('Using method in different years')
plt.show()

#%%
#we expect to see a correlation between mass and distance:

scatterplot(data=df, x=distance_clean, y=mass_clean, hue=method,)
plt.title('The relationship between Mass and Distance')
plt.show()

#%%

# how about mass vs Radius?
radius = 'Radius (RJ)'
radius_clean = 'radius (clean)'
df[radius_clean] = df[radius].apply(func=clean_mass)
scatterplot(data=df, y=mass_clean, x=radius_clean, hue=method)
plt.title('The relationship between Mass and Radius')
plt.show()

#%%
# how about mass vs Temp?

Temp = 'Temp. (K)'
Temp_clean = 'Temp (clean)'
df[Temp_clean] = df[Temp].apply(func=clean_mass)
scatterplot(data=df, y=mass_clean, x=Temp_clean, hue=method)
plt.tight_layout()
plt.title('The relationship between Mass and Temp')
plt.show()

#%%
#joinplot between two variables: mass and Temp

sns.jointplot(x=mass_clean ,y= Temp_clean ,data=df,
              kind="scatter",dropna=True, height=7, ratio=3, marginal_ticks=True)
plt.show()
 #kind=reg,hex,kde


#%%
#cleaning the rest of the data

star_mass = 'Host star mass (M☉)'
star_temp = 'Host star temp. (K)'
star_mass_clean = 'star mass (clean)'
star_temp_clean = 'star temp (clean)'

# yes we're reusing our mass cleaner here

df[star_mass_clean] = df[star_mass].apply(func=clean_mass)
df[star_temp_clean] = df[star_temp].apply(func=clean_mass)

#%%
#information about the DataFrame.After cleaning the data we have several
# new coloums.


df.info()

#%%
#whether there is a connection between the two characteristics and, if so,
# what kind it might be.
#Maybe there's some linear correlated data in there, maybe not.

scatterplot(data=df, x=star_mass_clean, y=star_temp_clean,style=method,hue=method)
plt.title('The relationship between star temp and star mass')

plt.show()

#%%
# maybe a pairplot will help

pairplot(data=df[[mass_clean, Temp_clean, distance_clean, 
                  star_mass_clean, star_temp_clean]], 
         diag_kind='kde',palette= "Spectral",dropna=True )

plt.show()

#%%
# let's look directly at the correlations

heatmap(data=df[[mass_clean, radius_clean, distance_clean, star_mass_clean,
                 star_temp_clean]].corr(),cmap="Blues" )
plt.show()
    
#%%
#Is this data really as uncorrelated as it seems? yes

df[[mass_clean, radius_clean, distance_clean, star_mass_clean, star_temp_clean]].corr()


#%%

















