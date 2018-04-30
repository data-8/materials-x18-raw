
# coding: utf-8

# # Optional Lab 6: Poverty
# 
# This optional set of questions exploring world poverty is provided to give you more practice and experience if you want it. This section is *not* required and will not count toward your course progress.
# 
# First, set up the tests and imports by running the cell below.

# In[ ]:


# Run this cell to set up the notebook, but please don't change it.

# These lines import the Numpy and Datascience modules.
import numpy as np
from datascience import *

# These lines do some fancy plotting magic.
import matplotlib
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plots
plots.style.use('fivethirtyeight')

from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

from client.api.notebook import Notebook
ok = Notebook('lab06.ok')


# ## 3. Global Poverty
# 
# In 1800, 85% of the world's 1 billion people lived in *extreme poverty*, defined by the United Nations as "a condition characterized by severe deprivation of basic human needs, including food, safe drinking water, sanitation facilities, health, shelter, education and information." A common measure of extreme poverty is a person living on less than \$1.25 per day.
# 
# In 2018, the proportion of people living in extreme poverty was estimated to be 8%. Although the world rate of extreme poverty has declined consistently for hundreds of years, the number of people living in extreme poverty is still over 600 million. The United Nations recently adopted an [ambitious goal](http://www.un.org/sustainabledevelopment/poverty/): "By 2030, eradicate extreme poverty for all people everywhere."
# In this section, we will examine extreme poverty trends around the world.

# First, load the population and poverty rate by country and year and the country descriptions. While the `population` table has values for every recent year for many countries, the `poverty` table only includes certain years for each country in which a measurement of the rate of extreme poverty was available.

# In[ ]:


population = Table.read_table('population.csv')
countries = Table.read_table('countries.csv').where('country', are.contained_in(population.group('geo').column(0)))
poverty = Table.read_table('poverty.csv')
poverty.show(3)


# **Question 3.1.** <br/>Assign `latest` to a three-column table with one row for each country that appears in the `poverty` table. The first column should contain the 3-letter code for the country. The second column should contain the *most recent year* for which an extreme poverty rate is available for the country. The third column should contain the poverty rate in that year. **Do not change the last line, so that the labels of your table are set correctly.**
# 
# *Hint*: think about how ```group``` works: it does a sequential search of the table (from top to bottom) and collects values in the array in the order in which they appear, and then applies a function to that array. The `first` function may be helpful, but you are not required to use it.

# In[ ]:


def first(values):
    return values.item(0)

latest = ...

latest.relabel(0, 'geo').relabel(1, 'time').relabel(2, 'poverty_percent') # You should *not* change this line.


# In[ ]:


_ = ok.grade('q3_1')


# **Question 3.2.** <br/>Using both `latest` and `population`, create a four-column table called `recent` with one row for each country in `latest`. The four columns should have the following labels and contents:
# 1. `geo` contains the 3-letter country code,
# 1. `poverty_percent` contains the most recent poverty percent,
# 1. `population_total` contains the population of the country in 2010,
# 1. `poverty_total` contains the number of people in poverty **rounded to the nearest integer**, based on the 2010 population and most recent poverty rate.

# In[ ]:


poverty_and_pop = ...
recent = ...
recent


# In[ ]:


_ = ok.grade('q3_2')


# The `countries` table includes not only the name and region of countries, but also their positions on the globe.

# In[ ]:


countries.select('country', 'name', 'world_4region', 'latitude', 'longitude')


# **Question 3.3.** <br/>Using both `countries` and `recent`, create a five-column table called `poverty_map` with one row for every country in `recent`.  The four columns should have the following labels and contents:
# 1. `latitude` contains the country's latitude,
# 1. `longitude` contains the country's longitude,
# 1. `name` contains the country's name,
# 1. `region` contains the country's region from the `world_4region` column of `countries`,
# 1. `poverty_total` contains the country's poverty total.

# In[ ]:


poverty_map = ...
poverty_map


# In[ ]:


_ = ok.grade('q3_3')


# Run the cell below to draw a map of the world in which the areas of circles represent the number of people living in extreme poverty. Double-click on the map to zoom in.

# In[ ]:


# It may take a few seconds to generate this map.
colors = {'africa': 'blue', 'europe': 'black', 'asia': 'red', 'americas': 'green'}
scaled = poverty_map.with_column(
    'poverty_total', 2e4 * poverty_map.column('poverty_total'),
    'region', poverty_map.apply(colors.get, 'region')
)
Circle.map_table(scaled)


# Although people live in extreme poverty throughout the world (with more than 5 million in the United States), the largest numbers are in Asia and Africa.

# **Question 3.4.** <br/>Assign `largest` to a two-column table with the `name` (not the 3-letter code) and `poverty_total` of the 10 countries with the largest number of people living in extreme poverty.

# In[ ]:


largest = ...
largest


# In[ ]:


_ = ok.grade('q3_4')


# **Question 3.5.** <br/>Use the function called `poverty_timeline` that takes **the name of a country** as its argument. It should draw a line plot of the number of people living in poverty in that country with time on the horizontal axis. The line plot should have a point for each row in the `poverty` table for that country. Do you understand the code in the two functions? 
# 
# Finally, draw the timelines below to see how the world is changing. You can check your work by comparing your graphs to the ones on [gapminder.org](https://goo.gl/lPujuh).

# In[ ]:


def population_for_country_in_year(row_of_poverty_table):
    """Optional: Define a function to return the population 
    of a country in a year using a row from the poverty table."""
    return population.where('time', row_of_poverty_table.item('time')).where('geo', row_of_poverty_table.item('geo')).column('population_total').item(0)

def poverty_timeline(country):
    """Draw a timeline of people living in extreme poverty in a country."""
    geo = countries.where('name', country).column('country').item(0)
    country_poverty = poverty.where('geo', geo)
    Table().with_columns('Year', country_poverty.column(1), 'Number in poverty', country_poverty.column(2) / 100 * country_poverty.apply(population_for_country_in_year)).plot(0, 1)


# In[ ]:


poverty_timeline('India')


# In[ ]:


poverty_timeline('Nigeria') 


# In[ ]:


# Draw the poverty timeline for China
poverty_timeline(...) 


# In[ ]:


# Draw the poverty timeline for the United States
poverty_timeline(...)


# Although the number of people living in extreme poverty has been increasing in Nigeria and the United States, the massive decreases in China and India have shaped the overall trend that extreme poverty is decreasing worldwide, both in percentage and in absolute number. 
# 
# To learn more, watch [Hans Rosling in a 2015 film](https://www.gapminder.org/videos/dont-panic-end-poverty/) about the UN goal of eradicating extreme poverty from the world. 
# 
# Below, we've also added an interactive dropdown menu for you to visualize `poverty_timeline` graphs for other countries. After selecting a new country, it will take a few seconds for the chart to update.

# In[ ]:


# Just run this cell

all_countries = poverty_map.column('name')
_ = widgets.interact(poverty_timeline, country=list(all_countries))


# ## Submission
# 
# There is no way to submit this optional lab, but you are welcome to check your work with the cell below.

# In[ ]:


# For your convenience, you can run this cell to run all the tests at once!
import os
_ = [ok.grade(q[:-3]) for q in os.listdir("tests") if q.startswith('q')]

