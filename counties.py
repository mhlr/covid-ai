from pylab import *
from builtins import *
import json, sys, os, re
import pandas as pd
import janitor

from toolz.curried import *
from toolz.curried import operator as op



import geopandas as gpd
import geoplot as gpl
import geoplot.crs as gcrs

cases = pd.read_csv('./data/covid_confirmed_usafacts.csv', parse_dates=True, infer_datetime_format=True, date_parses=pd.to_datetime),low_memory=False).convert_dtypes().set_index('countyFIPS')
deaths = pd.read_csv('./data/covid_deaths_usafacts.csv', parse_dates=True, infer_datetime_format=True, low_memory=False).convert_dtypes().set_index('countyFIPS')
pop =  pd.read_csv('./data/covid_county_population_usafacts.csv', parse_dates=True, infer_datetime_format=True, low_memory=False).convert_dtypes().set_index('countyFIPS')
nyt_counties = pd.read_csv('https://github.com/nytimes/covid-19-data/raw/master/us-counties.csv', parse_dates=True, infer_datetime_format=True, date_parses=pd.to_datetime, low_memory=False).convert_dtypes(string=False)

state_geo_src = 'https://raw.githubusercontent.com/loganpowell/census-geojson/master/GeoJSON/20m/2019/state.json'
county_geo_src = 'https://github.com/loganpowell/census-geojson/raw/master/GeoJSON/20m/2019/county.json'

excluded_states = ['AK', 'HI', 'PR','VI', 'MP', 'AS', 'GU']

#@memoize
def read_geo(path):
        return gpd.read_file(path)#.convert_dtypes()

county_geo = read_geo(county_geo_src)
state_geo = read_geo(state_geo_src)

df = county_geo.merge(state_geo, on='STATEFP', suffixes=['', '_state'])
df = df[~df.STUSPS.isin(excluded_states)]
df = df.set_index(df.GEOID.astype(int))

gpl.choropleth(df,hue=log2(0.5+df.join(cases, how='inner').iloc[:, -1]), extent=df.total_bounds, projection=gpl.crs.AlbersEqualArea())
#gpl.choropleth(county_geo, hue=log2(county_geo.ALAND), extent=state_geo[~state_geo.STUSPS.isin(excluded_states)].total_bounds)

