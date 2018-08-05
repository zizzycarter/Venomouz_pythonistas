# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 11:05:32 2018

@author: verascity
"""

import pandas as pd
import numpy as np
import plotly.plotly as py

df = pd.read_csv('depressionstats.csv')

df = df[['Entity', 'Year', 'Code', 'Percentage of Female Suffering from Depression']]
df = df.rename(index=str, columns={'Entity':'Country',
           'Percentage of Female Suffering from Depression':'Fpct'})
df['Fpct'] = df['Fpct'].str.rstrip('%').astype('float')


df = df.loc[df['Year'].isin([2002, 2014])]
df = df.loc[df['Code'].str.len() == 3]

def calc_trend(df):
    
    trend = []
    
    for country in np.unique(df['Country']):
       first = df.loc[(df['Country'] == country) & (df['Year'] == 2002)]
       second = df.loc[(df['Country'] == country) & (df['Year'] == 2014)]
       trend.append(round(float(second['Fpct']) - float(first['Fpct']), 2))
     
    return pd.Series(trend)

trend = calc_trend(df)
df = df.loc[df['Year'] == 2014]
df.loc[:,'Trend'] = trend.values
print(df.head(20))

data = [ dict(
        type = 'choropleth',
        locations = df['Code'],
        z = df['Trend'],
        text = df['Country'],
        colorscale = [[0,"rgb(24, 24, 24)"],[0.35,"rgb(44, 70, 39)"],[0.5,"rgb(64, 116, 55)"],\
            [0.6,"rgb(84, 162, 70)"],[0.7,"rgb(104, 208, 86)"],[1,"rgb(124, 255, 102)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(0,0,0)',
                width = 0.75
            ) ),
        colorbar = dict(
            autotick = False,
            ticksuffix = '%',
            title = 'Change in<br>Percentage'),
      ) ]

layout = dict(
    title = 'Global Trends in Population Statistics of Depressed Women, 2002-2014<br>(As Change in Percentage of total Female Population)',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.plot(fig, validate=False, filename='d1-world-map' )