# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 15:46:25 2018

@author: verascity
"""

import pandas as pd
import numpy as np
import plotly.plotly as py

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)

df = pd.read_csv('expenditurestats.csv')
df.rename(index=str, columns={'Entity':'Country',
           'Health expenditure, public (% of GDP) (% of GDP)':'Public',
           'Health expenditure, private (% of GDP) (% of GDP)':'Private'}, inplace=True)

def total_exp(row):
    return round((row['Public'] + row['Private']), 2)

df['Total'] = df.apply(total_exp, axis=1)

df = df.drop(index=['1564', '3125']) #buggy lines that were messing everything up
df['Total'] = df['Total'].astype('float')

df = df[['Country', 'Code', 'Year', 'Total']]

df = df.loc[df['Year'].isin([2002, 2014])]
df = df.loc[df['Code'].str.len() == 3]

def calc_trend(df):
    
    trend = []
    
    for country in np.unique(df['Country']):
       first = df.loc[(df['Country'] == country) & (df['Year'] == 2002)]
       second = df.loc[(df['Country'] == country) & (df['Year'] == 2014)]
       trend.append(round(float(second['Total']) - float(first['Total']), 2))
     
    return pd.Series(trend)

trend = calc_trend(df)
df = df.loc[df['Year'] == 2014]
df.loc[:,'Trend'] = trend.values

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
    title = 'Global Trends in Health Expenditures, 2002-2014<br>(As Change in % of GDP For Total Health Expenditures)',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.plot(fig, validate=False, filename='d2-world-map' )