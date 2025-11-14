import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

df_nobel = pd.read_csv('nobel_prize_data.csv')

# Challenge 1
# Preliminary data exploration.
# What is the shape of df_data? How many rows and columns?
print(f'The shape is: {df_nobel.shape}')
# What are the column names and what kind of data is inside of them?
for title in df_nobel:
    print(f'the title column is: {title}, and the type of data is: {type(df_nobel[title].loc[1])}')
# In which year was the Nobel prize first awarded?
print(f"The first awarded year is: {df_nobel['year'].min()}")

# Which year is the latest year included in the dataset?
print(f"The latest year is: {df_nobel['year'].max()}")

# Challenge 2
# Are there any duplicate values in the dataset?
print(f'There are {df_nobel.duplicated().values.sum()} duplicated values in DataFrame')
# Are there NaN values in the dataset?
print(f'There are {df_nobel.isna().values.sum()} NaN values in DataFrame')

# Which columns tend to have NaN values?
print(df_nobel.isna().sum())
# How many NaN values are there per column?
for title in df_nobel:
    print(f'the column {title} contain {df_nobel[title].isna().values.sum()} NaN values')

# Why do these columns have NaN values?
#
# Challenge 3
# Convert the birth_date column to Pandas Datetime objects
df_nobel['birth_date'] = pd.to_datetime(df_nobel['birth_date'])
print(df_nobel.info())

# Add a Column called share_pct which has the laureates' share as a percentage in the form of a floating-point number.
separated_values = df_nobel.prize_share.str.split('/', expand=True)
numerator = pd.to_numeric(separated_values[0])
denomenator = pd.to_numeric(separated_values[1])
df_nobel['share_pct'] = numerator / denomenator

# Create a donut chart using plotly which shows how many prizes went to men compared to how many prizes went to women.
# What percentage of all the prizes went to women?
nobel_prize_sex = df_nobel['sex'].value_counts()
print('The prize divided by sex')
print(nobel_prize_sex.index)
print(nobel_prize_sex.values)
# Creating a graph
donut = go.Figure(data=[go.Pie(labels=nobel_prize_sex.index, values=nobel_prize_sex.values, hole=.3)])
# donut.show()

# What are the names of the first 3 female Nobel laureates?
# What did the win the prize for?
# What do you see in their birth_country? Were they part of an organisation?
print(df_nobel[df_nobel.sex == 'Female'].head().sort_values('year', ascending=True)[:3])


# Did some people get a Nobel Prize more than once? If so, who were they?
is_winner = df_nobel.duplicated(subset=['full_name'], keep=False)
multiplo_winner =df_nobel[is_winner]
print(multiplo_winner.head())

print(is_winner.head())

# In how many categories are prizes awarded?
graph_cat = df_nobel.category.value_counts()
print(df_nobel.category.value_counts())
# Use the color scale called Aggrnyl to colour the chart, but don't show a color axis.
# Which category has the most number of prizes awarded?
# Which category has the fewest number of prizes awarded?
# Create a plotly bar chart with the number of prizes awarded by category.
cat = go.Figure(data=[go.Pie(labels=graph_cat.index, values=graph_cat.values)])
# cat.show()

# When was the first prize in the field of Economics awarded?
print('When was the first prize in the field of Economics awarded?')
# Who did the prize go to?
print(df_nobel[df_nobel.category == 'Economics'].sort_values('year', ascending=True)[:1])

# Create a plotly bar chart that shows the split between men and women by category.
category_woman_man = df_nobel.groupby(['category', 'sex'], as_index=False).agg({'prize': pd.Series.count})
category_woman_man.sort_values('prize',ascending=False ,inplace=True)
fig = px.bar( x=category_woman_man.category, y=category_woman_man.prize, color=category_woman_man.sex, title="Number of prizes")
# fig.show()

# Are more prizes awarded recently than when the prize was first created? Show the trend in awards visually.
# Count the number of prizes awarded every year.
# Create a 5 year rolling average of the number of prizes (Hint: see previous lessons analysing Google Trends).
# Using Matplotlib superimpose the rolling average on a scatter plot.
# Show a tick mark on the x-axis for every 5 years from 1900 to 2020. (Hint: you'll need to use NumPy).

prize_per_year = df_nobel.groupby(by='year').count().prize
moving_average = prize_per_year.rolling(window=5).mean()
print(prize_per_year.head())
print(moving_average)

# Starting the graph
# plt.scatter(x=prize_per_year.index,
#             y=prize_per_year.values,
#             c='dodgerblue',
#             alpha=0.7,
#             s=100, )
#
# plt.plot(prize_per_year.index,
#          moving_average.values,
#          c='crimson',
#          linewidth=3, )
#
# plt.show()

# Implementing the .xticks(), and .yticks() to fine-tune the chart.

plt.figure(figsize=(16, 8), dpi=200)
plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(ticks=np.arange(1900, 2021, step=5),
           fontsize=14,
           rotation=45)

ax = plt.gca()  # get current axis
ax.set_xlim(1900, 2020)

ax.scatter(x=prize_per_year.index,
           y=prize_per_year.values,
           c='dodgerblue',
           alpha=0.7,
           s=100, )

ax.plot(prize_per_year.index,
        moving_average.values,
        c='crimson',
        linewidth=3, )

# plt.show()

# Investigate if more prizes are shared than before.
# Calculate the average prize share of the winners on a year by year basis.
# Calculate the 5 year rolling average of the percentage share
# Copy-paste the cell from the chart you created above.
# Modify the code to add a secondary axis to your Matplotlib chart.
# Plot the rolling average of the prize share on this chart.
# See if you can invert the secondary y-axis to make the relationship even more clear.


yearly_avg_share = df_nobel.groupby(by='year').agg({'share_pct': pd.Series.mean})
share_moving_average = yearly_avg_share.rolling(window=5).mean()


plt.figure(figsize=(16, 8), dpi=200)
plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(ticks=np.arange(1900, 2021, step=5),
           fontsize=14,
           rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()  # create second y-axis
ax1.set_xlim(1900, 2020)

ax1.scatter(x=prize_per_year.index,
            y=prize_per_year.values,
            c='dodgerblue',
            alpha=0.7,
            s=100, )

ax1.plot(prize_per_year.index,
         moving_average.values,
         c='crimson',
         linewidth=3, )

# Adding prize share plot on second axis
ax2.plot(prize_per_year.index,
         share_moving_average.values,
         c='grey',
         linewidth=3, )

# plt.show()

# Create a Pandas DataFrame called top20_countries that has the two columns. The prize column should contain the total number of prizes won.

# top20_countries = df_nobel['organization_country'].value_counts()
# top20_code = df_nobel['ISO'].value_counts()
# print(top20_countries.values)
# print(top20_code.values)
# new = {
#     'organization_country': top20_countries.index,
#     'prize': top20_countries.values
# }
# new_code = {
#     'ISO': top20_code.index,
#     'prize': top20_code.values
# }
# # Creating DataFrame
# top20_countries = pd.DataFrame(new)
# top20_code = pd.DataFrame(new_code)
#
# print(top20_countries.head())
# print(top20_code.head())
#
# h_fig = go.Figure(go.Bar(x= top20_countries['prize'][:20], y=top20_countries['organization_country'][:20], orientation='h'))
#
# # h_fig.show()
#
# # Create this choropleth map using the plotly documentation:
#
# fig_map = go.Figure(data=go.Choropleth(
#     locations = top20_code['ISO'][:20],
#     z = top20_countries['prize'][:20],
#     text = top20_countries['organization_country'][:20],
#     colorscale = 'plasma',
#     autocolorscale=True,
#     reversescale=False,
# ))
#
# fig_map.update_layout(
#     title_text='Nobel Prize analysis',
#     geo=dict(
#         showframe=False,
#         showcoastlines=False,
#         projection_type='equirectangular'
#     ),
#     annotations = [dict(
#         x=0.55,
#         y=0.1,
#         xref='paper',
#         yref='paper',
#         text='Nobel Prize',
#         showarrow = False
#     )]
# )
#
# fig_map.show()


df_countries = df_nobel.groupby(['birth_country_current', 'ISO'],
                               as_index=False).agg({'prize': pd.Series.count})
df_countries.sort_values('prize', ascending=False)

world_map = px.choropleth(df_countries,
                          locations='ISO',
                          color='prize',
                          hover_name='birth_country_current',
                          color_continuous_scale=px.colors.sequential.matter)

world_map.update_layout(coloraxis_showscale=True, )

world_map.show()